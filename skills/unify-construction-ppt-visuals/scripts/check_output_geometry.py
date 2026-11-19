#!/usr/bin/env python3
"""Read-only validation of strict 2:1 visible PNG content with equal transparent margins.

Canvas aspect ratio is not constrained; content bounds use every alpha>0 pixel.

Requires Pillow. Does not inspect text fidelity or identify frame borders.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def inspect_geometry(path: Path) -> dict:
    with Image.open(path) as source:
        file_format = source.format
        width, height = source.size
        has_alpha = "A" in source.getbands() or "transparency" in source.info
        alpha = source.convert("RGBA").getchannel("A")
        bbox = alpha.getbbox()  # Every nonzero alpha pixel counts, including fringe.
        minimum_alpha, _ = alpha.getextrema()

    margins = None
    content_size = None
    if bbox is not None:
        left, top, right, bottom = bbox
        margins = [left, top, width - right, height - bottom]
        content_size = [right - left, bottom - top]
    checks = {
        "png": file_format == "PNG",
        "content_exact_2_to_1": content_size is not None
        and content_size[0] == 2 * content_size[1],
        "has_alpha": has_alpha,
        "has_fully_transparent_pixels": minimum_alpha == 0,
        "nonempty_content": bbox is not None,
        "equal_positive_margins": margins is not None
        and min(margins) > 0
        and len(set(margins)) == 1,
    }
    return {
        "file": str(path.resolve()),
        "canvas": [width, height],
        "content_bbox": list(bbox) if bbox is not None else None,
        "content_size": content_size,
        "margins_LTRB": margins,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Final PNG to inspect; never modified")
    args = parser.parse_args()
    try:
        report = inspect_geometry(args.image)
    except (OSError, ValueError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
