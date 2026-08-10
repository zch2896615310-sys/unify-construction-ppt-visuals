#!/usr/bin/env python3
"""Compile template-locked, per-page image prompts from a UTF-8 JSON brief."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


STYLE_LOCK = """STYLE LOCK — SAME SERIES, NOT A NEW DESIGN:
Create one standalone content-area image with an exact 2:1 aspect ratio, default 2000×1000, in the same approved corporate visual system. This image will be placed below the user's own slide header. Generate content only: no page header, title band, company name or logo, project-name banner, chapter label, page number or footer. Premium Chinese state-owned construction enterprise presentation aesthetic; restrained, modern, professional and digitally enabled. China Construction blue remains dominant: #005BAC, #0068D9 and #EAF4FF with white/pale blue-gray occupy 75–90% of the visual area. The only red is #E60012, used sparingly for critical numbers, dates, risks or measures. Permit at most one semantic auxiliary color per page, covering 5–12% and never more than 15%: construction orange #F59E0B for construction stages/zones, digital teal #0F9FA8 for BIM/digital systems, acceptance green #2E9B65 for completion/acceptance, or neutral slate #64748B for secondary information. Use no auxiliary color when it has no clear semantic purpose. Modular white cards with identical subtle corner radius, pale-blue hairline borders, cool soft shadow, consistent spacing and alignment. Realistic neutral engineering photography; preserve source architecture, materials, geometry, perspective and spatial relationships. No style reinterpretation between pages.
NEGATIVE LOCK:
No page header, title bar, company branding, logo, project banner, chapter marker, page number, footer, purple, pink, burgundy, dark red, large yellow areas, undefined new colors, multiple chromatic auxiliary colors on one page, auxiliary color covering more than 15%, random color changes across pages, neon, cyberpunk, glassmorphism, cartoon icons, colored emoji, random gradients, heavy shadows, mixed icon families, floating centered headline, dense Word-table appearance, altered architecture, invented construction facts, malformed hands, duplicated equipment, floating objects, inconsistent perspective or lighting."""


LAYOUTS = {
    "cover": "Cover content only: realistic project hero image with a restrained deep-blue geometric mask; no company identity, project title or header text.",
    "overview": "Overview content only: equal-width labels at left; perfectly aligned content boundary at right; optional two to four metric cards; no top title band.",
    "deployment": "Deployment: construction zones at left; faithful model or rendering in the center; explanation at right; construction logic along the bottom.",
    "method": "Method: quality-control points above; verified process at left; equal photo cards at right; control sequence along the bottom.",
    "bim": "BIM: BIM model or application scene as the main visual; application explanation at one side; management value summary along the bottom.",
    "schedule": "Schedule: one aligned timeline or milestone system; use the only red solely for key dates or durations.",
    "risk": "Risk: map risk, measure, owner and outcome in a restrained four-column system or closed-loop process.",
}

ACCENTS = {
    "none": "No chromatic auxiliary color; use only the fixed blue system, neutrals, and the unique red when semantically required.",
    "orange": "Use construction orange #F59E0B (pale tint #FFF4D6) only for construction stages, zones, or equipment; keep it within 5–12% of the page.",
    "teal": "Use digital teal #0F9FA8 (pale tint #E6F7F7) only for BIM, digital systems, or data applications; keep it within 5–12% of the page.",
    "green": "Use acceptance green #2E9B65 (pale tint #EAF7F0) only for completion, acceptance, or compliant status; keep it within 5–12% of the page.",
    "slate": "Use neutral slate #64748B (pale tint #F1F5F9) only for secondary information and neutral states.",
}

DEFAULT_ACCENTS = {
    "cover": "none",
    "overview": "slate",
    "deployment": "orange",
    "method": "orange",
    "bim": "teal",
    "schedule": "slate",
    "risk": "none",
    "construction-zone-allocation": "orange",
}

DEFAULT_TEMPLATES = {
    "cover": "cover-hero-v1",
    "overview": "overview-cards-v1",
    "deployment": "deployment-zones-v1",
    "method": "method-control-v1",
    "bim": "bim-application-v1",
    "schedule": "schedule-milestones-v1",
    "risk": "risk-closed-loop-v1",
    "construction-zone-allocation": "construction-zone-allocation-v1",
}

TEMPLATES = {
    "construction-zone-allocation-v1": {
        "page_type": "construction-zone-allocation",
        "layout": "deployment",
        "components": [
            "Canvas",
            "SummaryCard(x=3%,y=4%,w=94%,h=12%)",
            "ZoneCardA(x=3%,y=19%,w=31%,h=48%;crew_slots=4)",
            "FloorSpine(x=35.5%,y=19%,w=29%,h=48%;floor_slots=8)",
            "ZoneCardB(x=66%,y=19%,w=31%,h=48%;crew_slots=4)",
            "ParallelConnector(x=30%,y=69%,w=40%,h=7%)",
            "ResourceHeatmap(x=3%,y=79%,w=94%,h=17%)",
        ],
        "capacity": (
            "Keep exactly 8 FloorChip slots, descending by floor. Use an excluded blue-gray "
            "state for equipment/non-construction floors and a fixed empty state for missing data. "
            "Keep CrewChip order: carpentry, MEP, masonry, coating. ResourceHeatmap outer geometry "
            "and TotalBadge position are fixed; variable columns divide the heatmap width equally. "
            "If more than 8 floor slots are required, create a new template version and migrate every "
            "page in the same series before rendering."
        ),
    },
}

for _page_type, _template_id in DEFAULT_TEMPLATES.items():
    if _template_id not in TEMPLATES:
        _layout = _page_type if _page_type in LAYOUTS else "overview"
        TEMPLATES[_template_id] = {
            "page_type": _page_type,
            "layout": _layout,
            "components": [f"Fixed {_template_id} component tree", LAYOUTS[_layout]],
            "capacity": "Preserve the fixed component tree and declared empty states. Do not relocate sibling components to fit one page.",
        }


def lines(value: object) -> str:
    if value is None or value == "":
        return "None supplied"
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def validate_semantic_model(page: dict) -> dict:
    model = page.get("semantic_model")
    if not isinstance(model, dict):
        raise ValueError(
            f"Page {page.get('page', '?')}: semantic_model is required before layout. "
            "Supply purpose, entities, relationships, and reading_order."
        )
    required = ("purpose", "entities", "relationships", "reading_order")
    missing = [key for key in required if model.get(key) in (None, "", [])]
    if missing:
        raise ValueError(
            f"Page {page.get('page', '?')}: semantic_model is incomplete; missing {', '.join(missing)}."
        )
    return model


def infer_page_type(page: dict) -> str:
    explicit = page.get("page_type")
    if explicit:
        return str(explicit)

    searchable = json.dumps(page, ensure_ascii=False)
    markers = [
        "施工区" in searchable,
        "班组" in searchable,
        "平行施工" in searchable,
        "单层合计" in searchable or "资源矩阵" in searchable,
        bool(re.search(r"L\d{2}", searchable, re.IGNORECASE)),
    ]
    if sum(markers) >= 3:
        return "construction-zone-allocation"
    return str(page.get("layout", "overview"))


def template_fingerprint(template_id: str) -> str:
    payload = json.dumps(TEMPLATES[template_id], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def resolve_page(page: dict, warnings: list[str]) -> dict:
    semantic_model = validate_semantic_model(page)
    page_type = infer_page_type(page)
    if page_type not in DEFAULT_TEMPLATES:
        warnings.append(f"Page {page.get('page', '?')}: unknown page_type '{page_type}', used 'overview'.")
        page_type = "overview"

    template_id = str(page.get("template_id", DEFAULT_TEMPLATES[page_type]))
    if template_id not in TEMPLATES:
        raise ValueError(f"Page {page.get('page', '?')}: unknown template_id '{template_id}'.")
    if TEMPLATES[template_id]["page_type"] != page_type:
        raise ValueError(
            f"Page {page.get('page', '?')}: template '{template_id}' belongs to "
            f"page_type '{TEMPLATES[template_id]['page_type']}', not '{page_type}'."
        )

    accent_name = str(page.get("accent", DEFAULT_ACCENTS[page_type]))
    if accent_name not in ACCENTS:
        fallback = DEFAULT_ACCENTS[page_type]
        warnings.append(f"Page {page.get('page', '?')}: unknown accent '{accent_name}', used '{fallback}'.")
        accent_name = fallback

    resolved = dict(page)
    resolved.update(
        {
            "page_type": page_type,
            "template_id": template_id,
            "template_fingerprint": template_fingerprint(template_id),
            "series_key": str(page.get("series_key", page_type)),
            "accent": accent_name,
            "layout": TEMPLATES[template_id]["layout"],
            "semantic_model": semantic_model,
        }
    )
    return resolved


def validate_series(pages: list[dict]) -> None:
    locks: dict[tuple[str, str], tuple[str, str, str]] = {}
    for page in pages:
        key = (page["series_key"], page["page_type"])
        value = (page["template_id"], page["template_fingerprint"], page["accent"])
        if key in locks and locks[key] != value:
            prior = locks[key]
            raise ValueError(
                f"Series '{key[0]}' / page_type '{key[1]}' drifted: expected template/fingerprint/accent "
                f"{prior}, got {value} on page {page.get('page', '?')}."
            )
        locks[key] = value


def compile_page(project: str, anchor: str, page: dict) -> str:
    spec = TEMPLATES[page["template_id"]]
    semantic_model = page["semantic_model"]
    component_contract = "\n".join(f"- {item}" for item in spec["components"])
    return f"""# Page {page.get('page', '?')} — {page.get('title', 'Untitled')}

Project: {project}
Fixed STYLE_ANCHOR: {anchor}

{STYLE_LOCK}

SEMANTIC MODEL — UNDERSTAND BEFORE LAYOUT:
Purpose:
{lines(semantic_model['purpose'])}
Entities:
{lines(semantic_model['entities'])}
Relationships:
{lines(semantic_model['relationships'])}
Reading order:
{lines(semantic_model['reading_order'])}
Evidence: every statement above must be traceable to supplied text, numbers or diagram relationships.
Original-layout policy: use the old layout only to recover content and meaning. Do not imitate it by default. After understanding the page, redesign the information architecture to communicate the same meaning more clearly. Preserve all supplied content, relationships, data definitions and engineering facts.

PAGE CONTENT:
Page: {page.get('page', '?')}
Semantic page title, context only — DO NOT render: {page.get('title', '')}
Exact text and numbers to preserve:
{lines(page.get('content'))}
Source images:
{lines(page.get('source_images'))}
Non-negotiable facts:
{lines(page.get('must_preserve'))}
Auxiliary color plan — {page['accent']}:
{ACCENTS[page['accent']]}
Allowed changes before template freeze: grouping, information architecture, hierarchy, visual form, line breaks, alignment and spacing. Allowed changes after template freeze: populate declared template slots only.
Do not omit, summarize, translate, invent or alter any supplied text, number or engineering fact.

TEMPLATE LOCK — DATA MAY CHANGE, GEOMETRY MAY NOT:
Page type: {page['page_type']}
Template ID: {page['template_id']}
Template fingerprint: {page['template_fingerprint']}
Series key: {page['series_key']}
Component tree and normalized geometry:
{component_contract}
Capacity and overflow rules:
{spec['capacity']}
Keep every component type, order, position, size, corner radius, icon meaning and text hierarchy identical on all pages with the same series key and page type. Populate the fixed slots with page data only. Render declared empty or excluded states inside their original slots. Do not add, remove, swap, resize or relocate components to fit this page.

OUTPUT:
One separate content-area image at exactly 2:1, default 2000×1000. Do not render any page header, title band, company identity, logo, project banner, page number or footer. Do not combine it with other pages. Use a deterministic PPT/SVG/HTML/canvas renderer for the template and exact Chinese text; use image generation only for bitmap assets inside declared image slots. If native 2:1 generation is unavailable, keep all important content inside a crop-safe area, then crop or extend the canvas to exact 2:1 without stretching. Verify all content text and numbers against the content ledger.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="UTF-8 JSON brief")
    parser.add_argument("-o", "--output", type=Path, help="Markdown output; stdout if omitted")
    args = parser.parse_args()

    try:
        data = json.loads(args.brief.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read brief: {exc}", file=sys.stderr)
        return 2

    pages = data.get("pages")
    if not isinstance(pages, list) or not pages or not all(isinstance(page, dict) for page in pages):
        print("error: 'pages' must be a non-empty array of objects", file=sys.stderr)
        return 2

    warnings: list[str] = []
    try:
        resolved_pages = [resolve_page(page, warnings) for page in pages]
        validate_series(resolved_pages)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    project = str(data.get("project_title", "Engineering tender presentation"))
    anchor = str(data.get("style_anchor", "Create and freeze one approved representative page before the batch"))
    output = "\n\n---\n\n".join(compile_page(project, anchor, page) for page in resolved_pages)
    if warnings:
        output += "\n\n## Compiler warnings\n\n" + "\n".join(f"- {warning}" for warning in warnings) + "\n"

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

