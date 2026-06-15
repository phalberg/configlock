from pathlib import Path


README_PATH = Path(__file__).resolve().parents[1] / "README.md"
CLI_DOCS_PATH = Path(__file__).resolve().parents[1] / "CLI.md"
START_MARKER = "<!-- CLI_DOCS_START -->"
END_MARKER = "<!-- CLI_DOCS_END -->"


def main() -> None:
    readme_text = README_PATH.read_text(encoding="utf-8")
    cli_docs = CLI_DOCS_PATH.read_text(encoding="utf-8").strip()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        raise SystemExit("README.md must contain the CLI docs markers.")

    replacement = f"{START_MARKER}\n\n{cli_docs}\n\n{END_MARKER}"
    before, remainder = readme_text.split(START_MARKER, maxsplit=1)
    _, after = remainder.split(END_MARKER, maxsplit=1)

    updated = f"{before}{replacement}{after}"
    README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
