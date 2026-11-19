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
OUTPUT GEOMETRY LOCK — BOTH CONDITIONS ARE REQUIRED:
Deliver a real alpha-transparent PNG whose ACTUAL VISIBLE CONTENT bounding box has integer dimensions w=2*h, default w=2000 and h=1000. Measure the union of ALL alpha>0 pixels, including visible borders, shadows and antialiasing; a declared content box is not a substitute. Add exactly equal positive transparent pixel margins m on all four sides. Reuse the approved series margin; otherwise default m=round(w*0.03)=60 at the default content size. Derive canvas W=w+2*m and H=h+2*m, default 2120x1120, with exclusive-right/bottom bbox=(m,m,m+w,m+h), default (60,60,2060,1060). The final canvas is NOT required to be 2:1. These are equal pixel distances, not equal percentages of width and height. Explicit user output choices take precedence.
Reflow row heights, spacing and line breaks into this extent before freezing the template; preserve text/icon/photo proportions and all content relationships. Do not stretch the finished image, crop content, or add large empty bands just to reach 2:1. Existing template percentages are legacy composition baselines, not final-canvas coordinates. Reflow the complete content to the strict 2:1 content bounds before adding margins; freeze the resulting pixel coordinates. Do not retain legacy 3%/97% final-canvas rails or add a measurement frame to fake the content bounds. This output contract takes precedence over legacy canvas/background and outer-coordinate rules, including labor and risk templates. Their geometry locks apply after the initial equal-margin adaptation; preserve their internal content structure and approved visual style. Keep the outside genuinely transparent, with no fake white/black/checkerboard background or alpha specks. After ImageGen, verify actual pixel dimensions and all nonzero-alpha content bounds; both exact actual-content ratio w=2*h and equal margins must pass; canvas ratio is not a pass condition. Only content-preserving final cropping, translation and transparent padding may be used for export; if the composition must change, use ImageGen again. Call ImageGen with transparent_background=true unless the user explicitly requests an opaque output.
Create one standalone image with an actual visible content bounding box at exactly 2:1, default content 2000×1000 plus 60px equal transparent margins on a 2120×1120 canvas, in the same approved corporate visual system. This image will be placed below the user's own slide header. Generate content only: no page header, title band, company name or logo, project-name banner, chapter label, page number or footer. The bottom canvas must be genuinely transparent; white #FFFFFF or an approved source color belongs only inside content panels/cards. No gradient, blueprint line art, grid, coordinates, noise, paper grain, watermark or other texture may enter the transparent margins. Texture, low-contrast line art and semantic color fills are permitted only inside cards and must be clipped cleanly to card boundaries. Every top-level PrimaryFrame must share the same vertical alignment rails: left=m and right=W-m (default left=60px and right=2060px; do not reuse final-canvas 3%/97%). The first and last content edges must also meet top=m and bottom=H-m. Different internal column counts may not change those outer edges. Premium Chinese state-owned construction enterprise presentation aesthetic; restrained, modern, professional and digitally enabled. Do not add warm ivory, warm gray, warm surfaces or warm/cool mixing merely to create temperature contrast. Apply the declared palette_mode exactly. In source-led mode, first distill semantic_core_colors: preserve and strengthen colors directly bound to major entities, zones, states and relationships, with no hue or area limits. Decorative, redundant or competing source colors may be removed, merged or remapped only when every change is recorded in remapped_or_dropped_colors. Do not mechanically copy every source hue, and do not recolor a core entity blue/gray or desaturate it merely because it falls outside a corporate palette. Build a cross_region_color_map so the same entity keeps one color across source-photo/model overlays, labels, arrows, badges, list rows, dates and data states. Give color visible mass at three scales: large semantic regions or tinted overlays, medium headers/badges/row fills, and small labels/arrows/nodes; tiny accents alone are insufficient. Use China Construction blue only for newly added key hierarchy where it does not overwrite source color. In expanded-auxiliary mode, when the source is essentially monochrome or lacks a clear palette, create 2–4 coordinated auxiliary hues whose combined visible coverage is at least 20%. Put substantial color on bullet numbers and markers, keyword labels, causal nodes and arrows, relationship groups and connectors, process stages, parallel modules and data categories; thin rules, tiny icons and decorative dots do not satisfy the 20% minimum. This mode is not limited to one main accent, one micro accent, or the former 6–10%, 3% and 12% caps. In labor-cool-lock mode, preserve the existing cool white, China Construction blue, pale cool gray and unique peak red treatment and the original labor template geometry; do not apply the 20% auxiliary expansion and do not add warm color. The only newly assigned emphasis red remains #E60012 and is used sparingly for verbatim critical content registered in critical_phrases; source-led colors already present in source imagery remain unrestricted. Preserve source photography, materials, equipment and renderings in their real colors and never apply a global blue or warm filter. A source photo may be moderately de-emphasized with lower contrast or an 8–20% semantic zone tint when architecture and factual annotations remain readable. Modular cards use white, pale cool gray, pale blue or a registered pale auxiliary color according to hierarchy, with identical subtle corner radius, pale blue-gray hairline borders, neutral soft shadow, consistent spacing and alignment. Avoid three or more consecutive PrimaryFrames with the same pale-blue fill. No style reinterpretation between pages.
CONTENT FIDELITY AND DIAGRAM LOCK:
Render each source fact, sentence or complete semantic unit exactly once. Never repeat the same paragraph in a summary, body card, caption or flow node to fill space. A diagram may use only the shortest labels needed to identify objects and relationships. When one source paragraph contains two or more independently understandable causes, conditions, actions, steps, results or recommendations, split it into faithful ordered bullet points without inventing headings, conclusions or hierarchy and without changing wording, causality or sequence. Build source_content_slots and visual_reasoning_plan before layout. Do not use a fixed visual priority order; combine retained source imagery, faithful bullet points and diagrams according to the page's communication task and evidence. Generate measures visuals only when the source explicitly contains measures. Absence of measures forbids invented solutions but does not forbid diagrams about existing analysis, thinking, questions, causes, conditions, mechanisms, effects, object relationships, processes, data or evidence. If two or more explicit relationships are difficult to scan as prose, diagram_opportunity is required. Unconnected icons, numbered cards or repeated text do not satisfy a required relationship or mechanism diagram. Use non-photorealistic engineering information graphics for added diagrams, not invented realistic project scenes. If technical detail is uncertain, verify it; research may clarify general depiction but may not add project facts. If uncertainty remains, downgrade to an abstract source-traceable relationship rather than assuming the whole page cannot contain a diagram. Never guess a construction detail, dimension, material layer, routing, cause or solution.
NEGATIVE LOCK:
No page header, title bar, company branding, logo, project banner, chapter marker, page number, footer, opaque or fake-transparent outer margins, full-canvas texture, blueprint background, grid background, watermark, gradient background, top-level frames with different left/right edges, texture bleeding outside cards, unregistered new color roles, mechanical retention of source noise colors, unlogged source-color removal/merging/remapping, core entity colors recolored blue/gray or desaturated, one entity changing color across regions, color confined to thin rules/tiny icons/decorative dots, expanded-auxiliary coverage below 20%, warm-color additions or unapproved changes to the frozen internal labor-cool-lock layout, large uninterrupted pale-blue fields, source photos or materials globally tinted blue or warm, random semantic color changes across pages, newly introduced full red sentences or paragraphs, neon, cyberpunk, glassmorphism, cartoon icons, colored emoji, random gradients, heavy shadows, mixed icon families, floating centered headline, dense Word-table appearance, altered architecture, invented construction facts, repeated source paragraphs, duplicate text cards, unsupported schematics, inferred measures absent from the source, malformed hands, duplicated equipment, floating objects, inconsistent perspective or lighting."""


LAYOUTS = {
    "cover": "Cover content only: realistic project hero image with a restrained deep-blue geometric mask; no company identity, project title or header text.",
    "overview": "Overview content only: equal-width labels at left; perfectly aligned content boundary at right; optional two to four metric cards; no top title band.",
    "deployment": "Deployment: construction zones at left; faithful model or rendering in the center; explanation at right; construction logic along the bottom.",
    "method": "Method: quality-control points above; verified process at left; equal photo cards at right; control sequence along the bottom.",
    "bim": "BIM: BIM model or application scene as the main visual; application explanation at one side; management value summary along the bottom.",
    "schedule": "Schedule: one aligned timeline or milestone system; use the only red solely for key dates or durations.",
    "risk": "Risk: map risk, measure, owner and outcome in a restrained four-column system or closed-loop process.",
    "risk-analysis-measures-series": "Risk series: keep the fixed AnalysisHeader and MeasuresHeader unchanged; vary only the registered ContentBody density state.",
    "construction-zone-floor-schedule": "Construction zone floor schedule: lead line at top, source building with semantic zone overlays at left, equal-row floor start/finish schedule at right, and one conclusion strip at bottom; keep zone identity colors continuous across every region.",
    "labor-workforce-plan": "Labor workforce plan: management insight and peak card at top, monthly total trend in the middle, exact trade-by-period heatmap and totals at the bottom.",
}

PALETTE_MODES = {"source-led", "expanded-auxiliary", "labor-cool-lock"}

DEFAULT_AUXILIARY_PALETTES = {
    "cover": ["#0F9FA8", "#38BDF8", "#2E9B65"],
    "overview": ["#0F9FA8", "#F59E0B", "#2E9B65"],
    "deployment": ["#F59E0B", "#0F9FA8", "#2E9B65"],
    "method": ["#F59E0B", "#2E9B65", "#38BDF8"],
    "bim": ["#0F9FA8", "#38BDF8", "#84CC16"],
    "schedule": ["#F59E0B", "#0F9FA8", "#2E9B65"],
    "risk": ["#F59E0B", "#0F9FA8", "#2E9B65"],
    "risk-analysis-measures-series": ["#F59E0B", "#0F9FA8", "#2E9B65"],
    "construction-zone-allocation": ["#F59E0B", "#0F9FA8", "#2E9B65"],
    "construction-zone-floor-schedule": ["#0068D9", "#E60012", "#0F9FA8"],
    "labor-workforce-plan": [],
}

DEFAULT_COLOR_ROLE_MAPS = {
    "cover": {"#0F9FA8": "secondary visual group", "#38BDF8": "spatial layer", "#2E9B65": "verified state"},
    "overview": {"#0F9FA8": "information group", "#F59E0B": "key category", "#2E9B65": "verified state"},
    "deployment": {"#F59E0B": "construction zone or stage", "#0F9FA8": "resource relationship", "#2E9B65": "verified state"},
    "method": {"#F59E0B": "construction step", "#2E9B65": "control or acceptance state", "#38BDF8": "supporting relationship"},
    "bim": {"#0F9FA8": "digital system", "#38BDF8": "data path", "#84CC16": "validated output"},
    "schedule": {"#F59E0B": "active stage", "#0F9FA8": "dependency", "#2E9B65": "completed milestone"},
    "risk": {"#F59E0B": "cause or condition", "#0F9FA8": "relationship path", "#2E9B65": "verified control state"},
    "risk-analysis-measures-series": {"#F59E0B": "measure or cause marker", "#0F9FA8": "causal relationship", "#2E9B65": "verified state"},
    "construction-zone-allocation": {"#F59E0B": "construction zone or stage", "#0F9FA8": "shared resource relationship", "#2E9B65": "verified state"},
    "construction-zone-floor-schedule": {"#0068D9": "upper construction zone", "#E60012": "lower construction zone", "#0F9FA8": "optional shared relationship when source has no palette"},
    "labor-workforce-plan": {"#005BAC": "trend and heatmap", "#E60012": "exact peak only"},
}

DEFAULT_ACCENTS = {
    "cover": "none",
    "overview": "slate",
    "deployment": "orange",
    "method": "orange",
    "bim": "teal",
    "schedule": "slate",
    "risk": "none",
    "risk-analysis-measures-series": "none",
    "construction-zone-allocation": "orange",
    "construction-zone-floor-schedule": "blue",
    "labor-workforce-plan": "none",
}

DEFAULT_MICRO_ACCENTS = {
    page_type: ("orange" if page_type == "risk-analysis-measures-series" else "none")
    for page_type in DEFAULT_ACCENTS
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
    "construction-zone-floor-schedule": "construction-zone-floor-schedule-v1",
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
            "a full sentence or paragraph red. The fixed orange MeasuresHeader marker is only a template cue. "
            "If the source has a clear palette, distill and strengthen its semantic core colors, log every "
            "removed/merged/remapped noise color, and preserve major entity color identities without hue or area limits. Otherwise use 2–4 "
            "coordinated auxiliary hues across ContentBody bullets, causal/relationship nodes, connectors and "
            "parallel modules, with combined visible coverage at least 20%. Upgrade the template and migrate the whole "
            "series if content exceeds these states."
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
            "assets/templates/labor-workforce-plan-v1.png. Force palette_mode labor-cool-lock: preserve the existing "
            "cool colors and initial component geometry; do not add warm colors or the general 20% auxiliary expansion. "
            "icon_plan: none — exact analytical matrix."
        ),
    },
    "construction-zone-floor-schedule-v1": {
        "page_type": "construction-zone-floor-schedule",
        "layout": "construction-zone-floor-schedule",
        "components": [
            "Canvas",
            "LeadLine(x=3%,y=2%,w=94%,h=6%)",
            "BuildingZoneMap(x=3%,y=10%,w=47%,h=78%;source-building;zone-overlays=8–20%)",
            "FloorScheduleCard(x=51%,y=10%,w=46%,h=78%;row=floor-badge+start-date+finish-date)",
            "SummaryStrip(x=3%,y=91%,w=94%,h=6%)",
        ],
        "capacity": (
            "Support 2–3 construction zones and 6–12 floors or floor groups. Preserve the source building, "
            "floor order, dates and upward-flow relationships. Use the same semantic core color for each zone "
            "across the building tint, zone label, flow arrow, floor badge, schedule-row fill and date emphasis. "
            "Use large zone overlays, medium headers/badges/row fills and small arrows/labels; small accents alone "
            "are insufficient. Decorative or redundant source colors may be merged or remapped only when logged. "
            "Type anchor: assets/references/construction-zone-floor-schedule-after.png. Noise comparison only: "
            "assets/references/construction-zone-floor-schedule-before.png. If capacity is exceeded, create a new "
            "template version and migrate the whole series."
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
    if isinstance(value, dict):
        return "\n".join(f"- {key}: {item}" for key, item in value.items())
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
    zone_schedule_markers = [
        "施工区" in searchable,
        bool(re.search(r"(?:B?\d+|\d+[&、]\d+)层", searchable, re.IGNORECASE)),
        "开工" in searchable,
        "完工" in searchable or "完成日期" in searchable,
        "自下而上" in searchable or "流水施工" in searchable,
        "同步开工" in searchable or "平行施工" in searchable,
    ]
    if sum(zone_schedule_markers) >= 4:
        return "construction-zone-floor-schedule"
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

    # Legacy fields remain accepted for old briefs but no longer constrain the palette.
    accent_name = str(page.get("accent", DEFAULT_ACCENTS[page_type]))
    micro_accent_name = str(page.get("micro_accent", DEFAULT_MICRO_ACCENTS[page_type]))

    source_palette = page.get("source_palette", [])
    if source_palette in (None, ""):
        source_palette = []
    palette_mode = str(page.get("palette_mode", "")).strip()
    if page_type == "labor-workforce-plan":
        palette_mode = "labor-cool-lock"
    elif not palette_mode:
        palette_mode = "source-led" if source_palette else "expanded-auxiliary"
    if palette_mode not in PALETTE_MODES:
        raise ValueError(
            f"Page {page.get('page', '?')}: unknown palette_mode '{palette_mode}'. "
            f"Use source-led, expanded-auxiliary, or labor-cool-lock."
        )
    if palette_mode == "source-led" and not source_palette:
        warnings.append(
            f"Page {page.get('page', '?')}: source-led requires a documented source_palette; "
            "used expanded-auxiliary instead."
        )
        palette_mode = "expanded-auxiliary"

    auxiliary_palette = page.get("auxiliary_palette", DEFAULT_AUXILIARY_PALETTES[page_type])
    color_role_map = page.get("color_role_map", DEFAULT_COLOR_ROLE_MAPS[page_type])
    if palette_mode == "labor-cool-lock":
        auxiliary_palette = []
        auxiliary_ratio: float | str = "0% — fixed labor cool palette"
        color_role_map = DEFAULT_COLOR_ROLE_MAPS["labor-workforce-plan"]
    elif palette_mode == "source-led":
        auxiliary_ratio = page.get("auxiliary_ratio", "source-defined; no limit")
    else:
        try:
            auxiliary_ratio = float(page.get("auxiliary_ratio", 20))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Page {page.get('page', '?')}: auxiliary_ratio must be numeric in expanded-auxiliary mode."
            ) from exc
        if auxiliary_ratio < 20:
            warnings.append(
                f"Page {page.get('page', '?')}: auxiliary_ratio {auxiliary_ratio:g}% is below the required 20%; used 20%."
            )
            auxiliary_ratio = 20
        if not isinstance(auxiliary_palette, list) or not 2 <= len(auxiliary_palette) <= 4:
            raise ValueError(
                f"Page {page.get('page', '?')}: expanded-auxiliary mode requires 2–4 auxiliary colors."
            )
        if not isinstance(color_role_map, dict) or not color_role_map:
            raise ValueError(
                f"Page {page.get('page', '?')}: expanded-auxiliary mode requires a non-empty color_role_map."
            )
        auxiliary_ratio = f"{auxiliary_ratio:g}% minimum"

    semantic_core_colors = page.get("semantic_core_colors")
    if semantic_core_colors in (None, "", []):
        if palette_mode == "source-led":
            semantic_core_colors = source_palette
        elif palette_mode == "labor-cool-lock":
            semantic_core_colors = ["#005BAC", "#E60012"]
        else:
            semantic_core_colors = auxiliary_palette
    remapped_or_dropped_colors = page.get("remapped_or_dropped_colors", [])
    color_mass_plan = page.get("color_mass_plan")
    if not color_mass_plan:
        if palette_mode == "labor-cool-lock":
            color_mass_plan = {
                "large": "fixed pale-blue analytical areas from the initial labor template",
                "medium": "China Construction blue chart and matrix headers",
                "small": "exact peak red only",
            }
        else:
            color_mass_plan = {
                "large": "semantic region fills, transparent source-image overlays, or major category fields",
                "medium": "headers, badges, row fills, parallel modules, or relationship groups",
                "small": "labels, arrows, nodes, dates, and critical values",
            }
    cross_region_color_map = page.get("cross_region_color_map", {})
    if page_type == "construction-zone-floor-schedule" and not cross_region_color_map:
        cross_region_color_map = {
            "each construction zone": (
                "repeat its semantic core color across the building overlay, zone label, upward arrow, "
                "floor badge, schedule-row tint, and matching dates"
            )
        }

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
            "micro_accent": micro_accent_name,
            "palette_mode": palette_mode,
            "source_palette": source_palette,
            "semantic_core_colors": semantic_core_colors,
            "remapped_or_dropped_colors": remapped_or_dropped_colors,
            "auxiliary_palette": auxiliary_palette,
            "auxiliary_ratio": auxiliary_ratio,
            "color_role_map": color_role_map,
            "color_mass_plan": color_mass_plan,
            "cross_region_color_map": cross_region_color_map,
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
        palette_signature = page["palette_mode"]
        if page["palette_mode"] == "expanded-auxiliary":
            palette_signature += ":" + json.dumps(
                {
                    "auxiliary_palette": page["auxiliary_palette"],
                    "color_role_map": page["color_role_map"],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        value = (
            page["template_id"],
            page["template_fingerprint"],
            palette_signature,
        )
        if key in locks and locks[key] != value:
            prior = locks[key]
            raise ValueError(
                f"Series '{key[0]}' / page_type '{key[1]}' drifted: expected "
                "template/fingerprint/palette contract "
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
Palette mode:
{lines(page['palette_mode'])}
Source palette and source regions to preserve:
{lines(page['source_palette'])}
Semantic core colors:
{lines(page['semantic_core_colors'])}
Remapped or dropped colors, with source role, destination and reason:
{lines(page['remapped_or_dropped_colors'])}
Auxiliary palette:
{lines(page['auxiliary_palette'])}
Auxiliary visible-area ratio:
{lines(page['auxiliary_ratio'])}
Color-role map:
{lines(page['color_role_map'])}
Color-mass plan — large, medium and small scales:
{lines(page['color_mass_plan'])}
Cross-region color map — entity to photo/model overlay, label, arrow, badge, row/date/data state:
{lines(page['cross_region_color_map'])}
Palette execution plan:
In source-led mode, distill and strengthen the semantic core colors rather than copying every source hue. Preserve the color identity of major entities, zones, states and relationships without hue or area limits; log every decorative/noise color that is removed, merged or remapped. Repeat one entity color across all declared regions and give the palette visible mass at large, medium and small scales. In expanded-auxiliary mode, place the registered 2–4 colors substantially across bullet markers, keyword labels, causal nodes/arrows, relationship groups/connectors, process stages, parallel modules and data categories until their combined visible coverage reaches at least 20%; thin rules and tiny icons do not count as sufficient coverage. Do not add warm-neutral surfaces merely for temperature contrast. In labor-cool-lock mode, preserve the existing white/China Construction blue/pale cool gray/peak-red treatment and the initial labor template geometry; do not apply the 20% expansion or add warm color. Preserve real source photography and material colors and never invent imagery merely to reach a ratio.
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
Component tree and legacy normalized composition baseline (adapt to strict 2:1 actual-content bounds and equal margins before freezing pixel coordinates):
{component_contract}
Capacity and overflow rules:
{spec['capacity']}
Keep every component type, order, position, size, corner radius, icon meaning and text hierarchy identical on all pages with the same series key and page type. Populate the fixed slots with page data only. Render declared empty or excluded states inside their original slots. Do not add, remove or swap components to fit this page. First establish the strict 2:1 actual-content bounds and equal transparent margins as specified by OUTPUT GEOMETRY LOCK, then freeze and reuse the adapted component coordinates; later explicit user geometry changes require one coherent series update.

{('RISK SERIES LOCK — ANALYSIS AND MEASURES MAY NOT DRIFT:\nUse this template only because source_content_slots confirms that the source page explicitly contains both analysis and measures. If either slot is absent, stop and select another compatible page type; never invent the missing section. Keep AnalysisHeader and MeasuresHeader identical on every page in this series. Within each page and across all pages, render the exact labels “分析” and “措施” with exactly the same Chinese font family and exactly the same font size; keep their font weight equal by default. The two labels are peers: never make one larger, smaller, or use a different typeface. Preserve the fixed icon family, icon container, baseline, padding, x/y coordinates, and spacing. AnalysisHeader always uses the measure icon and China Construction blue treatment. MeasuresHeader always uses the plan icon, China Construction blue text, and the same short construction-orange marker. The marker alone does not satisfy expanded-auxiliary coverage: when the source has no clear palette, apply the registered 2–4 color palette across ContentBody bullets, causal/relationship nodes, connectors and parallel modules until combined visible coverage reaches at least 20%. When the source has a clear palette, distill and strengthen its core semantic colors, log any deletion/merge/remapping, and keep each entity color consistent across regions. Vary only the registered ContentBody density state. Never remove, rename, relocate, resize, recolor, or restyle either header.\nRED EMPHASIS LOCK:\nFor newly introduced text emphasis, render only the 1–3 verbatim entries listed in critical_phrases in #E60012. Never introduce a new full red sentence or paragraph and never invent a red phrase. Preserve existing source-led red content.' if page['page_type'] == 'risk-analysis-measures-series' else '')}

OUTPUT:
One separate PNG with actual visible content bounds at exactly w=2*h, default content 2000×1000 with 60px transparent margins on all four sides, yielding a 2120×1120 canvas. The final canvas itself is not required to be 2:1. Do not render any page header, title band, company identity, logo, project banner, page number or footer. Do not combine it with other pages. MANDATORY: call ImageGen independently for this page and use its full-page bitmap as the final visual composition. ImageGen must control the complete layout, spatial hierarchy, image integration, card system, icons and visual finish; generating only a background or small bitmap asset does not qualify. Never substitute an HTML/CSS webpage, SVG, Canvas, PPT shapes, frontend components or dashboard screenshot for the final page. Deterministic tools may only extract data, validate dimensions, perform content-preserving final crop/translation/transparent padding, or apply small exact text/number/icon corrections over the ImageGen full-page composition; they may not rebuild the overall layout. If ImageGen is unavailable, stop without falling back. Validate BOTH actual nonzero-alpha content width w=2*h and exactly equal positive transparent margins; do not require canvas W=2*H using scripts/check_output_geometry.py. Use actual nonzero-alpha bounds, not a threshold that hides stray pixels. Content-preserving final crop/padding is allowed only when it satisfies both conditions without excessive empty space; otherwise reflow with ImageGen. Never stretch or crop important content. Verify all content text and numbers against the content ledger.
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
