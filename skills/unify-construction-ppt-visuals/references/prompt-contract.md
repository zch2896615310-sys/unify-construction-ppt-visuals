# 提示词合同与一致性质检

## 1. STYLE LOCK

以下段落在同一项目的每次生成中逐字复用：

```text
STYLE LOCK — SAME SERIES, NOT A NEW DESIGN:
Create one standalone content-area image with an exact 2:1 aspect ratio, default 2000×1000, in the same approved corporate visual system. This image will be placed below the user's own slide header. Generate content only: no page header, title band, company name or logo, project-name banner, chapter label, page number or footer. Premium Chinese state-owned construction enterprise presentation aesthetic; restrained, modern, professional and digitally enabled. China Construction blue remains dominant: #005BAC, #0068D9 and #EAF4FF with white/pale blue-gray occupy 75–90% of the visual area. The only red is #E60012, used sparingly for critical numbers, dates, risks or measures. Permit at most one semantic auxiliary color per page, covering 5–12% and never more than 15%: construction orange #F59E0B for construction stages/zones, digital teal #0F9FA8 for BIM/digital systems, acceptance green #2E9B65 for completion/acceptance, or neutral slate #64748B for secondary information. Use no auxiliary color when it has no clear semantic purpose. Modular white cards with identical subtle corner radius, pale-blue hairline borders, cool soft shadow, consistent spacing and alignment. Realistic neutral engineering photography; preserve source architecture, materials, geometry, perspective and spatial relationships. No style reinterpretation between pages.
ICON LOCK:
When the page contains three or more repeated modules/stages, an equipment or measure list, or mappings among construction zones, floors, crews or shared resources, render one semantic line icon for every major module. Use only the bundled construction icon family: identical 24×24 viewBox, rounded 1.8px equivalent stroke, fixed icon container, size and position. Default icon color is China Construction blue; construction-zone or machinery icons may use the single permitted orange accent, and completion icons may use acceptance green. Never omit all icons on an icon-triggering page. Never mix icon families, use emoji, or reuse one icon for unrelated meanings.
NEGATIVE LOCK:
No page header, title bar, company branding, logo, project banner, chapter marker, page number, footer, purple, pink, burgundy, dark red, large yellow areas, undefined new colors, multiple chromatic auxiliary colors on one page, auxiliary color covering more than 15%, random color changes across pages, neon, cyberpunk, glassmorphism, cartoon icons, colored emoji, random gradients, heavy shadows, mixed icon families, floating centered headline, dense Word-table appearance, altered architecture, invented construction facts, malformed hands, duplicated equipment, floating objects, inconsistent perspective or lighting.
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
Auxiliary color plan: {accent_plan}
Allowed changes before template freeze: grouping, information architecture, hierarchy, visual form, line breaks, alignment and spacing.
Allowed changes after template freeze: populate fixed slots only.
Do not omit, summarize, translate, invent or alter any supplied text, number or engineering fact.
```

若 `purpose`、`entities`、`relationships` 或 `reading_order` 为空，停止排版。不要以“原页面看起来像表格/流程图”为理由直接复刻，也不要为了显得不同而改变原意。

若使用图像生成模型直接绘制中文文字，在末尾增加：

```text
Render the Chinese text exactly as supplied. After generation, verify every character and number against the content ledger; if exact rendering cannot be guaranteed, generate the visual without text and overlay the text deterministically in the slide layer.
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
Keep every component type, order, position, size, corner radius, icon meaning and text hierarchy identical on all pages with the same series key and page type. Populate the fixed slots with page data only. Render declared empty or excluded states inside their original slots. Do not add, remove, swap, resize or relocate components to fit this page.
```

相同 `series_key + page_type` 必须产生相同 `template_id` 和 `template_fingerprint`。若不相同，停止生成并修正输入，不能靠提示词“尽量统一”。

## 4. 锚点策略

优先级从高到低：

1. 用户明确批准的页面图片。
2. 同项目既有高质量页面。
3. 本轮先生成并自检通过的代表页。

每一页都引用固定锚点。若工具允许多个参考，同时引用“固定锚点 + 当前页原图”；必要时再加上一张相邻合格页。不要只串联上一页，因为连续的小变化会导致整套最后一页偏离第一页。

当工具无法持续携带固定锚点时，优先使用分层合成：生成统一照片/背景，在确定性 PPT 组件中排版；不要假装纯提示词可以可靠锁定整套风格。

## 5. 100 分验收表

| 维度 | 分值 | 检查项 |
|---|---:|---|
| 语义与内容准确 | 25 | 页面目的、实体、关系、阅读顺序正确；文字、数字和施工顺序完整 |
| 原图保真 | 20 | 建筑、材质、比例、空间、BIM 关系未变 |
| 色彩一致 | 15 | 中建蓝占主导；辅助色语义与占比合规；唯一红；无禁用色 |
| 构图一致 | 15 | 内容网格、边距、卡片系统稳定，无页面标题区；应触发时主要模块图标完整 |
| 模板一致 | 10 | 同类页面模板 ID、指纹、组件树、坐标、槽位顺序完全相同 |
| 图片一致 | 10 | 色温、曝光、裁切、设备融合真实 |
| 输出合规 | 5 | 一页一图、严格 2:1、仅内容区、无表头页脚、无拼图 |

未建立语义模型、语义关系表达错误、任一内容错误、原图结构改变、同类页面模板 ID/指纹不一致、组件坐标漂移、应触发图标却整页无图标或主要模块缺图标、图标语义错误或混用图标库、禁用色、辅助色超过 15%、单页出现多种彩色辅助色、非 2:1 比例或任何表头/页脚元素出现都算硬失败，不因总分较高而放行。合格线为 90 分。

## 6. 定向返工语句

```text
LOCAL CORRECTION ONLY. Keep every approved element unchanged. Correct only: {failed_items}. Preserve the fixed STYLE LOCK, page composition, source architecture, all correct text, colors, spacing and approved imagery. Do not redesign the page.
```
