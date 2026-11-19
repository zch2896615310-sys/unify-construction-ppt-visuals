# 提示词合同与一致性质检

## 1. STYLE LOCK

以下段落在同一项目的每次生成中逐字复用：

```text
STYLE LOCK — SAME SERIES, NOT A NEW DESIGN:
OUTPUT GEOMETRY LOCK — BOTH CONDITIONS ARE REQUIRED:
Deliver a real alpha-transparent PNG whose ACTUAL VISIBLE CONTENT bounding box has integer dimensions w=2*h, default w=2000 and h=1000. Measure the union of ALL alpha>0 pixels, including visible borders, shadows and antialiasing; a declared content box is not a substitute. Add exactly equal positive transparent pixel margins m on all four sides. Reuse the approved series margin; otherwise default m=round(w*0.03)=60 at the default content size. Derive canvas W=w+2*m and H=h+2*m, default 2120x1120, with exclusive-right/bottom bbox=(m,m,m+w,m+h), default (60,60,2060,1060). The final canvas is NOT required to be 2:1. These are equal pixel distances, not equal percentages of width and height. Explicit user output choices take precedence.
Reflow row heights, spacing and line breaks into this extent before freezing the template; preserve text/icon/photo proportions and all content relationships. Do not stretch the finished image, crop content, or add large empty bands just to reach 2:1. Existing template percentages are legacy composition baselines, not final-canvas coordinates. Reflow the complete content to the strict 2:1 content bounds before adding margins; freeze the resulting pixel coordinates. Do not retain legacy 3%/97% final-canvas rails or add a measurement frame to fake the content bounds. This output contract takes precedence over legacy canvas/background and outer-coordinate rules, including labor and risk templates. Their geometry locks apply after the initial equal-margin adaptation; preserve their internal content structure and approved visual style. Keep the outside genuinely transparent, with no fake white/black/checkerboard background or alpha specks. After ImageGen, verify actual pixel dimensions and all nonzero-alpha content bounds; both exact actual-content ratio w=2*h and equal margins must pass; canvas ratio is not a pass condition. Only content-preserving final cropping, translation and transparent padding may be used for export; if the composition must change, use ImageGen again. Call ImageGen with transparent_background=true unless the user explicitly requests an opaque output.
IMAGEGEN EXECUTION LOCK — MANDATORY FOR EVERY PAGE:
Use ImageGen to generate or edit this complete full-page 2:1 content-area bitmap. This is a per-page requirement: the ImageGen result must control the overall composition, spatial hierarchy, imagery integration, card system, icon treatment and visual finish. Do not satisfy this requirement by generating only a background, photo or small asset. Do not use an HTML/CSS webpage, SVG, Canvas, PPT shapes, frontend components or a dashboard screenshot as the final page image. Deterministic tools may only extract content, calculate data, verify dimensions, perform content-preserving final crop/translation/transparent padding, or apply small exact text/number/icon corrections on top of the ImageGen full-page composition; they may not replace or rebuild the overall layout. If ImageGen is unavailable, stop instead of falling back.
Create one standalone image with an actual visible content bounding box at exactly 2:1, default content 2000×1000 plus 60px equal transparent margins on a 2120×1120 canvas, in the same approved corporate visual system. This image will be placed below the user's own slide header. Generate content only: no page header, title band, company name or logo, project-name banner, chapter label, page number or footer. The bottom canvas must be genuinely transparent; white #FFFFFF or an approved source color belongs only inside content panels/cards. No gradient, blueprint line art, grid, coordinates, noise, paper grain, watermark or other texture may enter the transparent margins. Texture, low-contrast line art and semantic color fills are permitted only inside cards and must be clipped cleanly to card boundaries. Every top-level PrimaryFrame must share the same vertical alignment rails: left=m and right=W-m (default left=60px and right=2060px; do not reuse final-canvas 3%/97%). The first and last content edges must also meet top=m and bottom=H-m. Measure alignment from the straight segment of each outermost visible border, not from shadows, rounded corners, text, padding or inner cards. The top, middle and bottom PrimaryFrames must place their left outer borders on one identical pixel column and their right outer borders on one identical pixel column. Different internal column counts may not change those outer edges. At 2000px actual content width, more than 2px same-side deviation is a hard failure requiring a local ImageGen correction. Premium Chinese state-owned construction enterprise presentation aesthetic; restrained, modern, professional and digitally enabled. Do not add warm ivory, warm gray, warm surfaces or warm/cool mixing merely to create temperature contrast. Apply the declared palette_mode exactly. In source-led mode, first distill semantic_core_colors: preserve and strengthen colors directly bound to major entities, zones, states and relationships, with no hue or area limits. Decorative, redundant or competing source colors may be removed, merged or remapped to a semantic core color only when every change is recorded in remapped_or_dropped_colors. Do not mechanically copy every source hue, and do not recolor a core entity blue/gray or desaturate it merely because it falls outside a corporate palette. Build a cross_region_color_map so the same entity keeps one color across source-photo/model overlays, labels, arrows, badges, list rows, dates and data states. Give color visible mass at three scales: large semantic regions or tinted overlays, medium headers/badges/row fills, and small labels/arrows/nodes; tiny accents alone are not bold color use. Use China Construction blue only for newly added key hierarchy where it does not overwrite source color. In expanded-auxiliary mode, when the source is essentially monochrome or lacks a clear palette, create 2–4 coordinated auxiliary hues whose combined visible coverage is at least 20%. Put substantial color on bullet numbers and markers, keyword labels, causal nodes and arrows, relationship groups and connectors, process stages, parallel modules and data categories; thin rules, tiny icons and decorative dots do not satisfy the 20% minimum. This mode is not limited to one main accent, one micro accent, or the former 6–10%, 3% and 12% caps. In labor-cool-lock mode, preserve the existing cool white, China Construction blue, pale cool gray and unique peak red treatment and the original labor template geometry; do not apply the 20% auxiliary expansion and do not add warm color. The only newly assigned emphasis red remains #E60012 and is used sparingly for verbatim critical content registered in critical_phrases; source-led colors already present in source imagery remain unrestricted. Preserve source photography, materials, equipment and renderings in their real colors and never apply a global blue or warm filter. A source photo may be moderately de-emphasized with lower contrast or an 8–20% semantic zone tint when architecture and factual annotations remain readable. Modular cards use white, pale cool gray, pale blue or a registered pale auxiliary color according to hierarchy, with identical subtle corner radius, pale blue-gray hairline borders, neutral soft shadow, consistent spacing and alignment. Avoid three or more consecutive PrimaryFrames with the same pale-blue fill. No style reinterpretation between pages.
ICON LOCK:
Declare icon_mode before layout and build icon_plan separately for every PrimaryModule. Use semantic-line for abstract processes, stages, organizations, construction zones, floors, crews and management concepts. Use realistic-thumbnail for materials, equipment, samples, components and product categories when physical appearance improves recognition. Semantic-line uses only the bundled construction icon family: identical 24×24 viewBox, rounded 1.8px equivalent stroke, fixed container, size and position. Realistic-thumbnail uses isolated neutral product/material cutouts with one consistent 3/4 camera, scale, natural studio lighting, soft contact shadow, white or transparent-looking background, no text, no trademarks and no invented branding. Preserve natural object colors; when they form a clear source palette, use source-led mode without hue or area limits. A page may use a semantic line icon for a section header and realistic thumbnails for item cards because the roles differ, but never mix line, cartoon, 3D-toy and realistic styles within one peer group. A continuous-text, exact-matrix or source-photo module may individually use none, but the presence of that module never exempts other measure cards, repeated steps, stages, material/equipment lists or parallel semantic modules. Page-level icon_plan: none is permitted only when every PrimaryModule independently qualifies for none. Use mixed plans when needed, for example: measure cards -> semantic-line; exact table -> none; source photos -> none. Number badges, colored indices, photo captions and table headers do not substitute for semantic icons on a triggered module. Never omit all visual identifiers on a triggering page and never reuse one identifier for unrelated meanings.
CONTENT FIDELITY AND DIAGRAM LOCK:
Render each source fact, sentence or complete semantic unit exactly once. Never duplicate the same paragraph in a summary, body card, caption or flow node to fill space. A diagram may use only the shortest labels needed to identify objects and relationships; it may not restate the paragraph. When one source paragraph contains two or more independently understandable causes, conditions, actions, steps, results or recommendations, split it into faithful ordered bullet points without inventing headings, conclusions or hierarchy and without changing wording, causality or sequence. Build source_content_slots and a visual_reasoning_plan before layout. Do not use a fixed visual priority order; choose text, retained source imagery and diagrams together according to the page's communication task and evidence. Generate a measures diagram, measures process or MeasuresHeader only when the source page explicitly contains a measure, recommendation, solution, optimization action or handling step. Absence of measures forbids only invented measures and solutions; it never by itself forbids a diagram. For analysis, thinking, questions, causes, conditions, mechanisms, effects, object relationships, processes, data or evidence already present on the page, use a source-grounded causal chain, mechanism diagram, question/factor map, relationship map, process, matrix, timeline or evidence map when it improves comprehension. If a question has no supplied answer, visualize only the question and supplied factors, never an answer. If two or more explicit relationships are difficult to scan as prose, set diagram_opportunity to required. Unconnected icons, numbered cards or repeated text do not satisfy a required relationship/mechanism diagram; show the existing relationships with connectors, hierarchy, containment, mapping, comparison or state change. Use non-photorealistic engineering information graphics for added diagrams, not invented realistic project scenes. Apply the same source-slot rule to results, owners, dates, acceptance states and value conclusions. Every technical schematic must be traceable to the source page or verified authoritative standards, official technical material, or manufacturer documentation. If construction geometry, equipment mechanism, sequence or causality is uncertain, verify it before generation; research may clarify general professional depiction but may not add project-specific facts. If still uncertain, downgrade to an abstract source-traceable relationship rather than assuming the whole page cannot contain a diagram. Never guess a construction detail, dimension, material layer, routing, cause or solution.
SOURCE IMAGE RETENTION LOCK:
Identify every original image in the source page's main content area that carries information, evidence or project facts, including site photos, engineering drawings, renderings, screenshots, diagrams and charts, and retain every one in the final page. Never omit, replace, cover or reduce an original content image until its key subject or annotation becomes unreadable merely to improve layout or make room for new visuals. You may crop, resize, color-correct, unify corner radius, add decorative frames or reposition an original image only when its factual content, key subject and essential annotations remain intact. New images and decorative graphics may supplement the page but may not substitute for an original content image. Header/footer logos, company marks and purely decorative background images are excluded and remain removable under the no-header/no-footer rule. Replace an original content image only when the user explicitly asks for that specific replacement.
NEGATIVE LOCK:
No page header, title bar, company branding, logo, project banner, chapter marker, page number, footer, opaque or fake-transparent outer margins, full-canvas texture, blueprint background, grid background, watermark, gradient background, top-level frames with different left/right edges, texture bleeding outside cards, unregistered new color roles, mechanical retention of source noise colors, unlogged source-color removal/merging/remapping, core entity colors recolored blue/gray or desaturated, one entity changing color across regions, color confined to thin rules/tiny icons/decorative dots, expanded-auxiliary coverage below 20%, warm-color additions or unapproved changes to the frozen internal labor-cool-lock layout, large uninterrupted pale-blue fields, source photos or materials globally tinted blue or warm, random semantic color changes across pages, neon, cyberpunk, glassmorphism, colored emoji, random gradients, heavy shadows, mixed visual-identifier modes within one peer group, branded or text-bearing realistic thumbnails, floating centered headline, dense Word-table appearance, altered architecture, invented construction facts, repeated source paragraphs, duplicate text cards, unsupported schematics, inferred measures absent from the source, malformed hands, duplicated equipment, floating objects, inconsistent perspective or lighting.
```

不要为“更高级”加入新的风格词。抽象形容词越多，模型越容易重新解释风格。

## 2. SEMANTIC MODEL 与 PAGE CONTENT 模板

```text
SEMANTIC MODEL — UNDERSTAND BEFORE LAYOUT:
Purpose: {purpose}
Entities: {entities}
Relationships: {relationships}
Reading order: {reading_order}
Evidence: every statement above must be traceable to supplied text, numbers or diagram relationships.
Original-layout policy: use the old layout only to recover content and meaning. Do not imitate it by default. After understanding the page, redesign the information architecture to communicate the same meaning more clearly. Preserve all supplied content, relationships, data definitions and engineering facts.

PAGE CONTENT:
Page: {page}
Semantic page title, context only — DO NOT render: {title}
Exact text and numbers to preserve: {content}
Source images: {source_images}
Non-negotiable facts: {must_preserve}
Source content slots actually present: {source_content_slots}
Icon plan by primary module — module, icon_mode, icon_id/thumbnail_subject, semantic and color role: {icon_plan}
Visual reasoning plan — communication task, source relationships, diagram opportunity required/useful/none, chosen form, evidence mapping, and omission reason when none: {visual_reasoning_plan}
Diagram plan, with source or verification evidence for every diagram: {diagram_plan}
Palette mode: {palette_mode}
Source palette and source regions to preserve: {source_palette}
Semantic core colors: {semantic_core_colors}
Remapped or dropped colors, with source role, destination and reason: {remapped_or_dropped_colors}
Auxiliary palette: {auxiliary_palette}
Auxiliary visible-area ratio: {auxiliary_ratio}
Color-role map: {color_role_map}
Color-mass plan — large, medium and small scales: {color_mass_plan}
Cross-region color map — entity to photo/model overlay, label, arrow, badge, row/date/data state: {cross_region_color_map}
Allowed changes before template freeze: grouping, information architecture, hierarchy, visual form, line breaks, alignment and spacing.
Allowed changes after template freeze: populate fixed slots only.
Do not omit, summarize, translate, invent or alter any supplied text, number or engineering fact.
Do not render any content slot absent from source_content_slots. Each source statement appears once; use faithful bullets and evidence-based diagrams instead of repeated copy. Do not set diagram_opportunity to none merely because measures are absent.
Critical phrases copied verbatim from the source: {critical_phrases}
```

`critical_phrases` 不限于数字或日期。对连续正文，优先登记 1–3 个能够独立表达页面重点的原文关键词组、关键动作、施工方法、约束或结果；必须是原文中的连续字符，按完整词组登记，不拆词、不改写。渲染时只将该短语本身设为 `#E60012`，同句其余文字与标点保持深蓝灰。专用模板若定义了更严格的红色语义（例如劳动力页仅标精确峰值），专用规则优先。

若 `purpose`、`entities`、`relationships` 或 `reading_order` 为空，停止排版。不要以“原页面看起来像表格/流程图”为理由直接复刻，也不要为了显得不同而改变原意。

若使用图像生成模型直接绘制中文文字，在末尾增加：

```text
Render the Chinese text exactly as supplied. After generation, verify every character and number against the content ledger; if exact rendering cannot be guaranteed, keep the ImageGen full-page composition and apply only small deterministic text/number corrections over it. Do not rebuild the page layout with a deterministic renderer. If the correction changes the overall visual composition, send the corrected page back through ImageGen for final full-page editing.
```

## 3. TEMPLATE LOCK 模板

从 `template-registry.md` 选择模板，逐字写入以下合同：

```text
TEMPLATE LOCK — DATA MAY CHANGE, GEOMETRY MAY NOT:
Page type: {page_type}
Template ID: {template_id}
Template fingerprint: {template_fingerprint}
Series key: {series_key}
Component tree and normalized geometry: {component_contract}
Capacity and overflow rules: {capacity_rules}
Keep every component type, order, position, size, corner radius, icon meaning and text hierarchy identical on all pages with the same series key and page type. Populate the fixed slots with page data only. Render declared empty or excluded states inside their original slots. Do not add, remove or swap components to fit this page. First establish the strict 2:1 actual-content bounds and equal transparent margins as specified by OUTPUT GEOMETRY LOCK, then freeze and reuse the adapted component coordinates; later explicit user geometry changes require one coherent series update.
```

相同 `series_key + page_type` 必须产生相同 `template_id` 和 `template_fingerprint`。若不相同，停止生成并修正输入，不能靠提示词“尽量统一”。

对 `risk-analysis-measures-series-v1` 追加以下段落并逐页原样复用：

```text
RISK SERIES LOCK — ANALYSIS AND MEASURES MAY NOT DRIFT:
Use this template only after source_content_slots confirms that the source page explicitly contains both analysis and measures. If either slot is absent, stop and select another compatible page type; never invent the missing section.
Keep AnalysisHeader and MeasuresHeader identical on every page in this series. Within each page and across all pages, render the exact labels “分析” and “措施” with exactly the same Chinese font family and exactly the same font size; keep their font weight equal by default. The two labels are peers, so never make one larger, smaller, or use a different typeface. Also preserve the fixed icon family, icon container, baseline, padding, x/y coordinates, and spacing. AnalysisHeader always uses the measure icon and China Construction blue treatment. MeasuresHeader always uses the plan icon, China Construction blue text, and the same short construction-orange marker. The marker alone does not satisfy expanded-auxiliary coverage: when the source has no clear palette, apply the registered 2–4 color auxiliary palette across ContentBody bullet groups, causal/relationship nodes, connectors and parallel modules until combined visible coverage reaches at least 20%. When the source has a clear palette, distill and strengthen its core semantic colors, log any deletion/merge/remapping, and keep each entity color consistent across regions. Vary only the registered ContentBody density state to accommodate different photo and text quantities. Never remove, rename, relocate, resize, recolor, or restyle either header because this page has more photos or less text.
RED EMPHASIS LOCK:
For newly introduced text emphasis, render only the 1–3 verbatim entries listed in critical_phrases in #E60012. A critical entry may be a number, date, key word, phrase, risk, action, result, or core measure. Keep surrounding punctuation and all noncritical text dark blue-gray. Never introduce a new full red sentence or paragraph and never invent a red phrase. Existing source-led red content remains preserved.
```

## 4. 锚点策略

优先级从高到低：

1. 用户明确批准的页面图片。
2. 同项目既有高质量页面。
3. 本轮先生成并自检通过的代表页。

每一页都引用固定锚点。若工具允许多个参考，同时引用“固定锚点 + 当前页原图”；必要时再加上一张相邻合格页。不要只串联上一页，因为连续的小变化会导致整套最后一页偏离第一页。

当工具无法持续携带固定锚点时，停止批量生成并恢复锚点引用能力；不得退回到确定性 PPT/SVG/HTML/Canvas 分层合成。可以先缩小批次或逐页调用 ImageGen，但每个最终页面仍必须由 ImageGen 整页生成或整页编辑。

劳动力计划类页面固定使用 `labor-cool-lock`，并引用 `assets/templates/labor-workforce-plan-v1.png` 作为类型级视觉锚点；项目级锚点仍用于控制整套品牌风格。类型级锚点锁定“结论 + 峰值卡 + 趋势 + 热力矩阵”的初始构图、冷色配色和组件几何。当前页原图只用于提取文字与数据；不得套用普通页面至少 20% 的辅助色扩展，不得增加暖色，也不得借本次配色调整改变该模板版式。

## 5. 100 分验收表

| 维度 | 分值 | 检查项 |
|---|---:|---|
| 语义与内容准确 | 25 | 页面目的、实体、关系、阅读顺序正确；文字、数字和施工顺序完整 |
| 原图保真 | 20 | 建筑、材质、比例、空间、BIM 关系未变 |
| 色彩一致 | 15 | `source-led` 提炼并强化核心语义色，删并/重映射均有记录；同一实体跨图片、箭头、标签与数据行保持同色，并形成大中小三档色彩体量；`expanded-auxiliary` 辅助色合计至少 20%；劳动力页保持冷色与初始版式 |
| 构图一致 | 15 | 内容网格、边距、卡片系统稳定，无页面标题区；应触发时主要模块视觉标识完整且模式统一 |
| 模板一致 | 10 | 同类页面模板 ID、指纹、组件树、坐标、槽位顺序完全相同 |
| 图片一致 | 10 | 色温、曝光、裁切、设备融合真实 |
| 输出合规 | 5 | 一页一图、实际内容包围盒像素 w=2h 与四边等像素透明留白同时通过，画布不强求 2:1、真实 alpha、仅内容区、无表头页脚、无拼图 |

未建立语义模型、`source_content_slots`、逐模块 `icon_plan` 或 `visual_reasoning_plan`、因没有措施而直接把其他已有分析/思考/原因/机制/影响/关系内容判为不可图示、存在两个及以上清晰关系且段落难以扫描却无可信理由地声明 `diagram_opportunity: none`、`diagram_opportunity: required` 时只放互不连接的图标/编号卡/重复文字而未表达关系、任一页面未独立调用 ImageGen 完成整页生成/编辑、ImageGen 只生成局部素材、最终整页由 HTML/CSS/SVG/Canvas/PPT/前端组件截图生成、同一原文事实或段落重复出现、长段落存在多个独立要点却未合理分点、分点改变原文逻辑、源页主要内容区的原有照片、工程图纸、效果图、截图、示意图或图表被遗漏、替换、遮挡、裁掉关键主体/标注或缩小到无法辨认、新增配图取代原图、示意图错误或无来源依据、对不确定专业内容未经核验便生成、源页没有措施却生成措施栏/措施图/解决方案、源页没有结果/责任/时间/验收/价值却生成对应内容、语义关系表达错误、任一内容错误、原图结构改变、同类页面模板 ID/指纹不一致、组件坐标漂移、一级框架左右边界不共线、默认2000px宽实际内容区域上任意两个 `PrimaryFrame` 的同侧可见外边框偏差超过2px、默认透明输出缺少真实 alpha 或四边留白不等距、卡片外出现纹理/渐变/蓝图线稿/网格/水印、应触发视觉标识却整页无标识或主要模块缺标识、未声明 `icon_mode`、因局部照片/表格存在而把整页误写为 `icon_plan: none`、用编号徽章/彩色序号/照片图注/表头冒充语义图标、标识语义错误或同层级混用线性/卡通/3D/写实模式、写实缩略图含商标/文字/水印、`source-led` 机械保留噪声色、删除/合并/重映射颜色却未登记、主要实体颜色身份被改写、同一实体跨区域换色、只有小色点而缺少大中型色块、`expanded-auxiliary` 辅助色覆盖低于20%或仅用细线小图标凑比例、颜色角色未登记或跨页语义漂移、劳动力页加入暖色/执行20%扩展/改变初始版式、连续大面积浅蓝铺底、源照片或材料被统一染蓝或暖化、实际内容包围盒非严格2:1比例或任何表头/页脚元素出现都算硬失败，不因总分较高而放行。`risk-analysis-measures-series-v1` 只允许用于源页明确同时含分析和措施的页面；若符合条件但“分析/措施”任一标题的文字、字体、字号、图标、底板、坐标、间距或对齐线不同，或缺少任一标题，同样为硬失败；同一页内“分析”和“措施”字体家族或字号不相等也直接判为硬失败。本次新增的文字红色强调若不对应 `critical_phrases` 原文、超过3处或整句整段铺红，也为硬失败；源图既有红色按 `source-led` 保留。合格线为90分。

对 `labor-workforce-plan` 追加硬校验：矩阵逐列求和必须等于合计行；折线节点必须等于合计行；PeakCard 的精确峰值与月份必须等于合计行最大值及其列；红色只能落在全部并列最大值上。任一不一致均为硬失败。

最终尺寸和透明边距按 [output-geometry.md](output-geometry.md) 验收，并运行 `scripts/check_output_geometry.py`。框内配色和多框架左右对齐检查不能替代最终比例及四边等距检查。

## 6. 定向返工语句

```text
LOCAL CORRECTION ONLY, USING IMAGEGEN EDITING. Keep every approved element unchanged. Correct only: {failed_items}. Preserve the fixed STYLE LOCK, page composition, source architecture, all correct text, colors, spacing and approved imagery. Do not redesign the page. The corrected final page must remain an ImageGen full-page output.
```
