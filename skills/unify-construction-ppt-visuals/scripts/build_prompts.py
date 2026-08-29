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
Create one standalone content-area image with an exact 2:1 aspect ratio, default 2000×1000, in the same approved corporate visual system. This image will be placed below the user's own slide header. Generate content only: no page header, title band, company name or logo, project-name banner, chapter label, page number or footer. The bottom canvas must be pure white #FFFFFF with no gradient, blueprint line art, grid, coordinates, noise, paper grain, watermark or any other texture. Texture, low-contrast line art and semantic color fills are permitted only inside cards and must be clipped cleanly to card boundaries. Every top-level PrimaryFrame must share the same vertical alignment rails: left edge x=3% and right edge x=97% (w=94%). Different internal column counts may not change those outer edges. Premium Chinese state-owned construction enterprise presentation aesthetic; restrained, modern, professional and digitally enabled. China Construction blue remains dominant: #005BAC, #0068D9 and #EAF4FF with white/pale blue-gray occupy 75–90% of the visual area. The only red is #E60012, used sparingly for verbatim critical numbers, dates, risks, key words or phrases, key actions, results or measures registered in critical_phrases; never color a whole sentence or paragraph red. Permit at most one semantic auxiliary color per page, covering 5–12% and never more than 15%: construction orange #F59E0B for construction stages/zones, digital teal #0F9FA8 for BIM/digital systems, acceptance green #2E9B65 for completion/acceptance, or neutral slate #64748B for secondary information. Use no auxiliary color when it has no clear semantic purpose. Exception only for risk-analysis-measures-series-v1: the fixed orange MeasuresHeader micro-marker may coexist at no more than 1% of the canvas with one additional semantic accent at no more than 3%; total chromatic auxiliary coverage still must not exceed 15%. Modular white cards with identical subtle corner radius, pale-blue hairline borders, cool soft shadow, consistent spacing and alignment. Realistic neutral engineering photography; preserve source architecture, materials, geometry, perspective and spatial relationships. No style reinterpretation between pages.
CONTENT FIDELITY AND DIAGRAM LOCK:
Render each source fact, sentence or complete semantic unit exactly once. Never repeat the same paragraph in a summary, body card, caption or flow node to fill space. A diagram may use only the shortest labels needed to identify objects and relationships. When one source paragraph contains two or more independently understandable causes, conditions, actions, steps, results or recommendations, split it into faithful ordered bullet points without inventing headings, conclusions or hierarchy and without changing wording, causality or sequence. Build source_content_slots and visual_reasoning_plan before layout. Do not use a fixed visual priority order; combine retained source imagery, faithful bullet points and diagrams according to the page's communication task and evidence. Generate measures visuals only when the source explicitly contains measures. Absence of measures forbids invented solutions but does not forbid diagrams about existing analysis, thinking, questions, causes, conditions, mechanisms, effects, object relationships, processes, data or evidence. If two or more explicit relationships are difficult to scan as prose, diagram_opportunity is required. Unconnected icons, numbered cards or repeated text do not satisfy a required relationship or mechanism diagram. Use non-photorealistic engineering information graphics for added diagrams, not invented realistic project scenes. If technical detail is uncertain, verify it; research may clarify general depiction but may not add project facts. If uncertainty remains, downgrade to an abstract source-traceable relationship rather than assuming the whole page cannot contain a diagram. Never guess a construction detail, dimension, material layer, routing, cause or solution.
NEGATIVE LOCK:
No page header, title bar, company branding, logo, project banner, chapter marker, page number, footer, non-white bottom canvas, full-canvas texture, blueprint background, grid background, watermark, gradient background, top-level frames with different left/right edges, texture bleeding outside cards, purple, pink, burgundy, dark red, large yellow areas, undefined new colors, auxiliary color covering more than 15%, random color changes across pages, full red sentences or paragraphs, neon, cyberpunk, glassmorphism, cartoon icons, colored emoji, random gradients, heavy shadows, mixed icon families, floating centered headline, dense Word-table appearance, altered architecture, invented construction facts, repeated source paragraphs, duplicate text cards, unsupported schematics, inferred measures absent from the source, malformed hands, duplicated equipment, floating objects, inconsistent perspective or lighting."""


LAYOUTS = {
    "cover": "Cover content only: realistic project hero image with a restrained deep-blue geometric mask; no company identity, project title or header text.",
    "overview": "Overview content only: equal-width labels at left; perfectly aligned content boundary at right; optional two to four metric cards; no top title band.",
    "deployment": "Deployment: construction zones at left; faithful model or rendering in the center; explanation at right; construction logic along the bottom.",
    "method": "Method: quality-control points above; verified process at left; equal photo cards at right; control sequence along the bottom.",
    "bim": "BIM: BIM model or application scene as the main visual; application explanation at one side; management value summary along the bottom.",
    "schedule": "Schedule: one aligned timeline or milestone system; use the only red solely for key dates or durations.",
    "risk": "Risk: map risk, measure, owner and outcome in a restrained four-column system or closed-loop process.",
    "risk-analysis-measures-series": "Risk series: keep the fixed AnalysisHeader and MeasuresHeader unchanged; vary only the registered ContentBody density state.",
    "labor-workforce-plan": "Labor workforce plan: management insight and peak card at top, monthly total trend in the middle, exact trade-by-period heatmap and totals at the bottom.",
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
    "risk-analysis-measures-series": "orange",
    "construction-zone-allocation": "orange",
    "labor-workforce-plan": "none",
}

DEFAULT_TEMPLATES = {
    "cover": "cover-hero-v1",
    "overview": "overview-cards-v1",
    "deployment": "deployment-zones-v1",
    "method": "method-control-v1",
    "bim": "bim-application-v1",
    "schedule": "schedule-milestones-v1",
    "risk": "risk-closed-loop-v1",
    "risk-analysis-measures-series": "risk-analysis-measures-series-v1",
    "construction-zone-allocation": "construction-zone-allocation-v1",
    "labor-workforce-plan": "labor-workforce-plan-v1",
}

TEMPLATES = {
    "risk-analysis-measures-series-v1": {
        "page_type": "risk-analysis-measures-series",
        "layout": "risk-analysis-measures-series",
        "components": [
            "Canvas",
            "AnalysisHeader(x=3%,y=4%,w=94%,h=13%;label=分析;icon=measure)",
            "MeasuresHeader(x=3%,y=19%,w=94%,h=7%;label=措施;icon=plan)",
            "ContentBody(x=3%,y=28%,w=94%,h=69%;state=text-photo|four-card|photo-gallery|before-after|three-stage)",
        ],
        "capacity": (
            "Never move or restyle AnalysisHeader or MeasuresHeader. The exact labels 分析 and 措施 must use "
            "the same font family and the same font size within each page and across the whole series; keep "
            "their font weight equal by default. Choose only a registered ContentBody "
            "density state based on the supplied entities and image count. Keep the body outer frame and "
            "top/bottom baselines fixed. Render only 1–3 verbatim critical_phrases in #E60012; never color "
            "a full sentence or paragraph red. The fixed orange MeasuresHeader micro-marker may use at most "
            "1% of the canvas; one additional semantic accent may use at most 3%; total auxiliary color remains "
            "below 15%. Upgrade the template and migrate the whole series if content exceeds these states."
        ),
    },
    "labor-workforce-plan-v1": {
        "page_type": "labor-workforce-plan",
        "layout": "labor-workforce-plan",
        "components": [
            "Canvas",
            "InsightBlock(x=3%,y=4%,w=77%,h=13%)",
            "PeakCard(x=82%,y=4%,w=15%,h=13%)",
            "TrendChart(x=3%,y=20%,w=94%,h=29%)",
            "WorkforceHeatmap(x=3%,y=54%,w=94%,h=43%)",
        ],
        "capacity": (
            "Support 6–12 ordered period columns and 8–16 trade rows inside fixed geometry. "
            "Compute every period total from the trade matrix; use the same totals for the chart "
            "and total row. PeakCard must equal max(period totals), with every tied peak declared. "
            "Use red only for exact peak values. Preserve source trade order. Use one global heatmap "
            "scale, with zero as the palest state. If the supplied totals conflict with computed sums, "
            "stop and report the conflict instead of rendering. Type anchor: "
            "assets/templates/labor-workforce-plan-v1.png. icon_plan: none — exact analytical matrix."
        ),
    },
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


def infer_source_content_slots(page: dict) -> list[str]:
    """Conservatively detect only content types supported by source-page fields."""
    supplied = page.get("source_content_slots")
    if isinstance(supplied, dict):
        slots = [str(key) for key, present in supplied.items() if present]
        if slots:
            return slots
    if isinstance(supplied, list) and supplied:
        return [str(item) for item in supplied]

    source_payload = {
        "title": page.get("title"),
        "content": page.get("content"),
        "source_images": page.get("source_images"),
        "must_preserve": page.get("must_preserve"),
    }
    text = json.dumps(source_payload, ensure_ascii=False)
    slots: list[str] = []
    markers = {
        "analysis": ("分析", "原因", "问题", "现象", "风险"),
        "thinking": ("思考", "如何", "选择", "考虑", "判断", "权衡"),
        "mechanism": ("机理", "机制", "由于", "导致", "引发", "影响", "形成", "造成"),
        "relationships": ("对应", "组成", "包括", "分为", "连接", "并行", "对比", "之间"),
        "measures": (
            "措施", "整改", "建议", "方案", "优化", "应对", "处理步骤", "改进",
            "重新", "增加", "安装", "设置", "采用", "要求", "确保", "完善", "封堵", "更换", "调整",
        ),
        "process": ("流程", "步骤", "工序", "顺序", "阶段"),
        "results": ("结果", "效果", "成果", "完成", "验收", "达成"),
        "owners": ("责任人", "责任单位", "负责人", "责任主体"),
        "dates": ("日期", "工期", "时间", "年月", "节点"),
        "data": ("合计", "数量", "比例", "金额", "面积", "人数", "峰值"),
    }
    for slot, keywords in markers.items():
        if any(keyword in text for keyword in keywords):
            slots.append(slot)
    if page.get("source_images"):
        slots.append("photo_evidence")
    return slots or ["main_subject_only"]


def has_slot(slots: list[str], expected: str) -> bool:
    normalized = " ".join(slots).lower()
    aliases = {
        "analysis": ("analysis", "分析", "原因", "问题", "现象", "风险"),
        "measures": ("measures", "measure", "措施", "整改", "建议", "方案", "优化", "应对"),
    }
    return any(alias in normalized for alias in aliases[expected])


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
    if "分析" in searchable and "措施" in searchable:
        return "risk-analysis-measures-series"
    labor_markers = [
        "劳动力" in searchable or "用工计划" in searchable,
        "工种" in searchable,
        "投入" in searchable or "人数" in searchable,
        "合计" in searchable,
        "峰值" in searchable or bool(re.search(r"\d+月", searchable)),
    ]
    if sum(labor_markers) >= 3:
        return "labor-workforce-plan"

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
    source_content_slots = infer_source_content_slots(page)
    page_type = infer_page_type(page)
    if page_type not in DEFAULT_TEMPLATES:
        warnings.append(f"Page {page.get('page', '?')}: unknown page_type '{page_type}', used 'overview'.")
        page_type = "overview"

    if page_type == "risk-analysis-measures-series" and not (
        has_slot(source_content_slots, "analysis") and has_slot(source_content_slots, "measures")
    ):
        raise ValueError(
            f"Page {page.get('page', '?')}: risk-analysis-measures-series requires source-page evidence "
            "for both analysis and measures. Select a compatible page_type instead of inventing the missing slot."
        )

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
    visual_reasoning_plan = page.get("visual_reasoning_plan")
    if not visual_reasoning_plan:
        visual_reasoning_plan = {
            "communication_task": semantic_model["purpose"],
            "source_relationships": semantic_model["relationships"],
            "diagram_opportunity": "useful",
            "diagram_form": (
                "Choose a source-grounded non-photorealistic relationship, mechanism, process, data or "
                "evidence diagram appropriate to the supplied relationships; do not assume measures are required."
            ),
            "evidence_mapping": (
                "Map every node and connector to source text, data, source images or verified general technical material."
            ),
            "omission_reason": "Required only when diagram_opportunity is none.",
        }
    resolved.update(
        {
            "page_type": page_type,
            "template_id": template_id,
            "template_fingerprint": template_fingerprint(template_id),
            "series_key": str(page.get("series_key", page_type)),
            "accent": accent_name,
            "layout": TEMPLATES[template_id]["layout"],
            "semantic_model": semantic_model,
            "source_content_slots": source_content_slots,
            "visual_reasoning_plan": visual_reasoning_plan,
            "diagram_plan": page.get(
                "diagram_plan",
                "Select a diagram from the page's existing analysis, thinking, causes, mechanisms, effects, object relationships, processes, data or evidence. Measures visuals require an explicit measures slot. Verify uncertain technical details; if uncertainty remains, use an abstract source-traceable relationship instead of inventing details.",
            ),
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
Source content slots actually present:
{lines(page['source_content_slots'])}
Visual reasoning plan:
{lines(page['visual_reasoning_plan'])}
Diagram plan and evidence boundary:
{lines(page['diagram_plan'])}
Auxiliary color plan — {page['accent']}:
{ACCENTS[page['accent']]}
Allowed changes before template freeze: grouping, information architecture, hierarchy, visual form, line breaks, alignment and spacing. Allowed changes after template freeze: populate declared template slots only.
Do not omit, summarize, translate, invent or alter any supplied text, number or engineering fact.
Do not render any content slot absent from source_content_slots. Each source statement appears once. Split multi-point paragraphs faithfully and use evidence-based diagrams instead of repeated copy. Do not set diagram_opportunity to none merely because measures are absent. If diagram_opportunity is required, unconnected icons or numbered cards are not an acceptable substitute for a relationship or mechanism diagram.
Critical phrases copied verbatim from the source:
{lines(page.get('critical_phrases'))}

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

{('RISK SERIES LOCK — ANALYSIS AND MEASURES MAY NOT DRIFT:\nUse this template only because source_content_slots confirms that the source page explicitly contains both analysis and measures. If either slot is absent, stop and select another compatible page type; never invent the missing section. Keep AnalysisHeader and MeasuresHeader identical on every page in this series. Within each page and across all pages, render the exact labels “分析” and “措施” with exactly the same Chinese font family and exactly the same font size; keep their font weight equal by default. The two labels are peers: never make one larger, smaller, or use a different typeface. Preserve the fixed icon family, icon container, baseline, padding, x/y coordinates, and spacing. AnalysisHeader always uses the measure icon and China Construction blue treatment. MeasuresHeader always uses the plan icon, China Construction blue text, and the same short construction-orange micro-marker. Vary only the registered ContentBody density state. Never remove, rename, relocate, resize, recolor, or restyle either header.\nRED EMPHASIS LOCK:\nRender only the 1–3 verbatim entries listed in critical_phrases in #E60012. Never turn a full sentence or paragraph red and never invent a red phrase.' if page['page_type'] == 'risk-analysis-measures-series' else '')}

OUTPUT:
One separate content-area image at exactly 2:1, default 2000×1000. Do not render any page header, title band, company identity, logo, project banner, page number or footer. Do not combine it with other pages. MANDATORY: call ImageGen independently for this page and use its full-page bitmap as the final visual composition. ImageGen must control the complete layout, spatial hierarchy, image integration, card system, icons and visual finish; generating only a background or small bitmap asset does not qualify. Never substitute an HTML/CSS webpage, SVG, Canvas, PPT shapes, frontend components or dashboard screenshot for the final page. Deterministic tools may only extract data, validate dimensions, or apply small exact text/number/icon corrections over the ImageGen full-page composition; they may not rebuild the overall layout. If ImageGen is unavailable, stop without falling back. If native 2:1 generation is unavailable, keep all important content inside a crop-safe area, then crop or extend the canvas to exact 2:1 without stretching. Verify all content text and numbers against the content ledger.
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
