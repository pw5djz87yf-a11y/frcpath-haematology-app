#!/usr/bin/env python3
"""Build a self-contained FRCPath Haematology test release."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import shutil
from pathlib import Path

APP_FILENAME = "index.html"
BANK_GLOB = "frcpath_gs_aml_*.json"
MANIFEST_FILENAME = "aml-question-bank-manifest.json"
PACKAGE_NAME = "frcpath-haematology-release"
AML_CODE_PATTERN = re.compile(r"^AML\d{3,}$", re.IGNORECASE)


def read_cases(path: Path) -> list[dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path.name}: invalid JSON ({error})") from error

    cases = payload if isinstance(payload, list) else payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f'{path.name}: expected a non-empty array or a non-empty "cases" array')
    if not all(isinstance(question, dict) for question in cases):
        raise ValueError(f"{path.name}: every question must be a JSON object")
    return cases


def build_release(source_root: Path, output_root: Path) -> tuple[Path, int, int]:
    app_path = source_root / APP_FILENAME
    if not app_path.is_file():
        raise FileNotFoundError(f"App HTML not found: {app_path}")

    bank_paths = sorted(source_root.glob(BANK_GLOB), key=lambda path: path.name.casefold())
    if not bank_paths:
        raise FileNotFoundError(f"No question banks matched {BANK_GLOB}")

    codes: list[str] = []
    for bank_path in bank_paths:
        for question in read_cases(bank_path):
            code = str(question.get("code", "")).upper()
            if not AML_CODE_PATTERN.fullmatch(code):
                raise ValueError(f"{bank_path.name}: invalid AML code {code or '(missing)'}")
            codes.append(code)

    duplicate_codes = sorted(code for code, count in Counter(codes).items() if count > 1)
    if duplicate_codes:
        raise ValueError(f"Duplicate AML codes: {', '.join(duplicate_codes)}")

    package_dir = output_root / PACKAGE_NAME
    archive_path = output_root / f"{PACKAGE_NAME}.zip"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    package_dir.mkdir()

    shutil.copy2(app_path, package_dir / "index.html")
    for bank_path in bank_paths:
        shutil.copy2(bank_path, package_dir / bank_path.name)

    filenames = [path.name for path in bank_paths]
    (package_dir / MANIFEST_FILENAME).write_text(
        json.dumps(filenames, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    ordered_codes = sorted(codes, key=lambda code: int(code[3:]))
    release_info = {
        "bank_file_count": len(bank_paths),
        "question_count": len(codes),
        "first_question_code": ordered_codes[0],
        "last_question_code": ordered_codes[-1],
        "source_html": APP_FILENAME,
    }
    (package_dir / "release-info.json").write_text(
        json.dumps(release_info, indent=2) + "\n",
        encoding="utf-8",
    )

    (package_dir / "README.txt").write_text(
        "FRCPath Haematology test release\n"
        "================================\n\n"
        "Do not open index.html directly from the filesystem.\n"
        "From this folder, run:\n\n"
        "    python -m http.server 8000\n\n"
        "Then open http://localhost:8000 in your browser.\n",
        encoding="utf-8",
    )

    if archive_path.exists():
        archive_path.unlink()
    shutil.make_archive(
        str(output_root / PACKAGE_NAME),
        "zip",
        root_dir=output_root,
        base_dir=PACKAGE_NAME,
    )
    return archive_path, len(bank_paths), len(codes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing the app and AML JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="Directory for the release folder and ZIP.",
    )
    args = parser.parse_args()

    archive_path, bank_count, question_count = build_release(
        args.source_root.resolve(),
        args.output_dir.resolve(),
    )
    print(f"Created {archive_path}")
    print(f"Included {bank_count} bank files and {question_count} questions")


if __name__ == "__main__":
    main()
