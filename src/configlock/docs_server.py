from __future__ import annotations

import argparse
import contextlib
import http.server
import threading
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


RELOAD_SCRIPT = b"""
<script>
async function waitForReload() {
  try {
    const response = await fetch('/__reload__', { cache: 'no-store' });
    if (response.status === 204) {
      location.reload();
      return;
    }
  } catch (error) {
    console.log('reload poll failed', error);
  }
  setTimeout(waitForReload, 1000);
}
waitForReload();
</script>
"""


class ReloadState:
    def __init__(self) -> None:
        self.condition = threading.Condition()
        self.generation = 0

    def bump(self) -> None:
        with self.condition:
            self.generation += 1
            self.condition.notify_all()

    def wait_for_next(self, generation: int) -> None:
        with self.condition:
            self.condition.wait_for(lambda: self.generation > generation)


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, state: ReloadState) -> None:
        self.state = state

    def on_any_event(self, event) -> None:
        if not event.is_directory:
            self.state.bump()


class DocsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, docs_root: Path, state: ReloadState, **kwargs):
        self.docs_root = docs_root
        self.state = state
        super().__init__(*args, directory=str(docs_root), **kwargs)

    def end_headers(self) -> None:
        if self.path.endswith(".html") or self.path in {"/", ""}:
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        if self.path == "/__reload__":
            generation = self.state.generation
            self.state.wait_for_next(generation)
            self.send_response(204)
            self.end_headers()
            return
        super().do_GET()

    def copyfile(self, source, outputfile) -> None:
        content = source.read()
        if b"</html>" in content:
            content = content.replace(b"</html>", RELOAD_SCRIPT + b"</html>")
        elif self.path.endswith(".html") or self.path in {"/", ""}:
            content += RELOAD_SCRIPT
        outputfile.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve docs/ with live reload.")
    parser.add_argument("port", nargs="?", type=int, default=8000)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    docs_root = Path(__file__).resolve().parents[2] / "docs"
    state = ReloadState()

    observer = Observer()
    observer.schedule(ReloadHandler(state), str(docs_root), recursive=True)
    observer.start()

    def handler_factory(*handler_args, **handler_kwargs):
        return DocsHandler(
            *handler_args,
            docs_root=docs_root,
            state=state,
            **handler_kwargs,
        )

    try:
        with contextlib.suppress(KeyboardInterrupt):
            server = http.server.ThreadingHTTPServer(
                (args.bind, args.port), handler_factory
            )
            print(f"Serving {docs_root} at http://{args.bind}:{args.port}/")
            server.serve_forever()
    finally:
        observer.stop()
        observer.join()
