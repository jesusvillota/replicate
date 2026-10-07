#!/usr/bin/env python3
"""Extract text from PDF files with PaddleOCR's default OCR pipeline."""

from __future__ import annotations

import argparse
import socket
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pdfs = sorted(args.input_dir.glob("*.pdf"))
    if len(pdfs) != 3:
        raise SystemExit(f"Expected 3 PDF files in {args.input_dir}, found {len(pdfs)}")

    from paddleocr import PaddleOCR

    ocr = PaddleOCR()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdfs:
        page_blocks: list[str] = []
        page_count = 0
        for page_count, prediction in enumerate(ocr.predict(str(pdf_path)), start=1):
            payload = prediction.json
            page_result = payload.get("res", payload)
            texts = page_result.get("rec_texts", [])
            lines = [str(text).strip() for text in texts if str(text).strip()]
            if lines:
                page_blocks.append(f"[Page {page_count}]\n" + "\n".join(lines))

        extracted_text = "\n\n".join(page_blocks).strip()
        if not extracted_text:
            raise RuntimeError(f"PaddleOCR returned no text for {pdf_path.name}")

        output_path = args.output_dir / f"{pdf_path.stem}.txt"
        temporary_path = output_path.with_suffix(".txt.tmp")
        temporary_path.write_text(extracted_text + "\n", encoding="utf-8")
        temporary_path.replace(output_path)
        print(
            f"Wrote {output_path.name}: {page_count} pages, "
            f"{len(extracted_text)} characters"
        )

    print(f"Completed OCR for {len(pdfs)} PDFs on {socket.gethostname()}")


if __name__ == "__main__":
    main()
