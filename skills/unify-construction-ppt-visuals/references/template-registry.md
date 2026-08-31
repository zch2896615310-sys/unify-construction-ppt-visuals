# 页面类型与确定性模板注册表

## 基本合同

把页面结果定义为：

`页面结果 = 语义模型选择的固定模板 + 固定视觉令牌 + 页面数据`

模板选择必须发生在语义理解之后。旧页面的坐标、表格外观、文本框数量和留白不是分类依据；页面目的、实体、关系和阅读顺序才是分类依据。首次建立模板时允许重构旧排版，模板冻结后同类页面只实例化数据。

先按信息结构识别 `page_type`，再绑定 `template_id`。相同 `series_key + page_type` 只允许一个模板 ID。坐标均为相对于 2:1 内容画布的百分比，原点位于左上角；渲染时换算为整数像素，禁止逐页人工微调。

统一几何令牌：安全边距 3%；卡片圆角 1.2% 画布高；卡片描边 0.08% 画布宽；卡片间距 1.2% 画布宽；阴影参数、图标库、字号三级层级由 `style-bible.md` 固定。

全局一级框架合同：所有 `PrimaryFrame` 必须使用统一外边界 `x=3%`、`w=94%`，从而共享 `left=3%` 与 `right=97%` 两条贯通页面的竖向对齐线。边界坐标指最外层可见描边的直线段，不是阴影、圆角端点或框内内容。不同框架内部可以采用不同列数，但不得改变外边界；首列左缘和末列右缘必须分别回到全局对齐线。禁止因顶部内容较少而缩窄顶部框、因中部流程较宽而外扩中部框、或让底部矩阵单独使用另一组左右边距。默认 2000px 宽输出的同侧外边框像素偏差不得超过 2px，超过即判模板几何失败。画布底层固定为纯白 `#FFFFFF`，纹理或语义填充只能出现在组件卡片内部并受圆角蒙版裁切。

## 类型判定

以字段和关系为准，不以旧页面长相为准。满足下列多数特征时归为 `construction-zone-allocation`：

- 标段或楼层范围摘要；
- 两个施工区及各自楼层范围；
- 木工、水电、泥水、涂料等班组配置；
- L19、L20 等楼层序列；
- 户型/资源数量矩阵、单层合计或总计；
- “平行施工”关系。

楼层号、是否存在设备层、户型列数和总量不同只是数据差异，不得改变类型。

满足下列多数特征时归为 `labor-workforce-plan`：

- 出现“劳动力计划”“劳动力投入”“用工计划”“高峰期人数”等语义；
- 行是测量、电焊、防水、木工、水电、泥水、涂料、安装、搬运等工种；
- 列是月份、周次或施工时段；
- 存在各时段合计、峰值投入或可从矩阵求得这些数据；
- 阅读任务是先判断投入规模与峰值，再查看变化趋势，最后核查工种明细。

原页是否只有表格、是否已有折线图、月份数量和工种数量不同，都不改变该类型。

## construction-zone-allocation-v1

- `page_type`: `construction-zone-allocation`
- `template_id`: `construction-zone-allocation-v1`
- 默认主辅助色：`orange`；默认微辅助色：`none`
- 固定组件树：`Canvas > SummaryCard + ZoneCardA + FloorSpine + ZoneCardB + ParallelConnector + ResourceHeatmap`

| 组件 | x | y | w | h | 固定规则 |
|---|---:|---:|---:|---:|---|
| SummaryCard | 3 | 4 | 94 | 12 | 左侧摘要，右侧 TotalBadge；不显示页面标题 |
| ZoneCardA | 3 | 19 | 31 | 48 | 第一施工区；固定 4 个 CrewChip 槽位 |
| FloorSpine | 35.5 | 19 | 29 | 48 | 固定 8 个等高 FloorChip；自上而下楼层降序 |
| ZoneCardB | 66 | 19 | 31 | 48 | 第二施工区；固定 4 个 CrewChip 槽位 |
| ParallelConnector | 30 | 69 | 40 | 7 | 固定双向/并行关系，不更换图形语法 |
| ResourceHeatmap | 3 | 79 | 94 | 17 | 外框固定；列数按数据等分，行高固定 |

组件内部规则：

- 两张 ZoneCard 使用完全相同的标题带、图标、内边距和班组顺序；只替换区名、楼层范围和人数。
- FloorSpine 始终保留 8 个位置。设备层或不施工层使用蓝灰斜纹 `excluded` 状态；数据不足使用 `empty` 状态，不删除槽位。超过 8 个楼层时升级为新模板版本并让同组页面全部迁移。
- CrewChip 顺序固定为木工、水电、泥水、涂料；缺项显示 0 或“未配置”，不改变顺序，不换图标。
- ResourceHeatmap 外框和总计位置固定。户型/资源列数可变，但在外框内等分；相同字段沿用同一颜色强度映射。
- 工程橙控制在 6%–10%，只落在施工区、阶段和机械语义；非施工状态使用暖象牙或蓝灰中性表面，禁止把三大主体区全部铺成浅蓝。
- TotalBadge 固定在 SummaryCard 右端，不得在不同页面移到热力表旁或页面角落。
- 图标只用于稳定语义：施工区、楼层、班组、并行、资源总计。不得按页随机使用工人、建筑、齿轮等不同隐喻。
- 图标不是可选装饰。两张 ZoneCard 固定使用 `zone`，FloorSpine 使用 `floors`，四类 CrewChip 使用 `crew`，ParallelConnector 使用 `parallel`，ResourceHeatmap 总计使用 `shared`；几何按 `icon-system.md` 冻结。

## labor-workforce-plan-v1

- `page_type`: `labor-workforce-plan`
- `template_id`: `labor-workforce-plan-v1`
- 默认主辅助色：`none`；默认微辅助色：`none`；使用中建蓝、白、暖象牙、浅中性灰与唯一强调红
- 默认视觉锚点：`assets/templates/labor-workforce-plan-v1.png`
- 固定组件树：`Canvas > InsightBlock + PeakCard + TrendChart + WorkforceHeatmap`

| 组件 | x | y | w | h | 固定规则 |
|---|---:|---:|---:|---:|---|
| InsightBlock | 3 | 4 | 77 | 13 | 上方放内容标签和管理结论；不绘制 PPT 页面表头 |
| PeakCard | 82 | 4 | 15 | 13 | 峰值人数、单位和峰值月份固定右对齐 |
| TrendChart | 3 | 20 | 94 | 29 | 蓝色折线与浅蓝面积；所有节点显示数值，唯一峰值节点为红色实心 |
| WorkforceHeatmap | 3 | 54 | 94 | 43 | 工种 × 时段矩阵；顶部深蓝表头，底部深蓝合计行，峰值合计单元格为红色 |

组件内部规则：

- 阅读顺序固定为 InsightBlock → PeakCard → TrendChart → WorkforceHeatmap。结论先行、趋势解释、明细验证，四块不得换序。
- InsightBlock 的内容标签优先使用“{标段/区域}｜施工劳动力投入”；管理结论逐字使用源文。源文缺失时仅使用数据派生固定句式，不补写原因。
- PeakCard 显示精确最大合计 `peak_value` 和 `peak_month`；“约 230 人”等近似描述只能留在源文结论中，不得替代精确峰值。
- TrendChart 的横轴时段顺序与矩阵列顺序完全相同。纵轴从 0 起，刻度上限取不小于峰值的整洁档位；禁止截断纵轴制造夸张变化。折线、面积、节点、数值标签坐标固定由数据计算。
- WorkforceHeatmap 首列固定为工种，末行固定为合计。单元格蓝色强度按全矩阵统一数值域映射；0 值使用暖象牙 `#F7F4EE` 或近白中性灰，低值才进入浅蓝，高值使用中蓝，禁止按单行分别归一化导致跨工种不可比较。
- 本模板默认 `accent: none`、`micro_accent: none` 且不依赖源图，因此白色与浅中性色可占 68%–82%；中建蓝目标仍为 18%–25%、硬上限 30%。不得为了补足通用配色比例添加橙、青、绿或其他无数据语义的色块。
- 工种行顺序遵循源数据，不得按人数重新排序。需要突出持续主力工种时只允许加粗工种名和高值数字，不新增主辅助色或微辅助色。
- 红色仅用于 `peak_value`：PeakCard 数字、TrendChart 峰值节点/标签、合计行对应单元格。其他月份与普通热力单元格不得使用红色。
- 月份/时段槽位支持 6–12 列，工种支持 8–16 行；在固定外框内等分列宽和行高。超出容量时升级模板版本并迁移同系列全部页面，不得局部压扁字号。
- 不使用装饰性小图标。该页的精确数据图表与矩阵本身构成主要视觉语法，声明 `icon_plan: none — exact analytical matrix`。
- 该页蓝色系目标占 18%–25%，复杂矩阵不得超过 30%；图表外的非数据表面优先使用白、暖象牙和暖灰细描边，禁止用浅蓝填满所有留白。红色只承担峰值，不为了达到面积比例扩大红色。
- 渲染前计算 `monthly_totals = sum(trade_rows)`、`peak_value = max(monthly_totals)`、`peak_month = argmax(monthly_totals)`，并核对源合计行。若并列峰值，所有并列峰值节点使用红色，但 PeakCard 按时间顺序列出月份，不擅自只选一个。

## labor-workforce-plan-long-v1

- `page_type`: `labor-workforce-plan`
- `template_id`: `labor-workforce-plan-long-v1`
- 适用容量：13–30 个连续月份、8–16 个工种
- 默认主辅助色：`none`；默认微辅助色：`none`；使用中建蓝、白、暖象牙、浅中性灰与唯一强调红
- 类型级视觉锚点：`assets/templates/labor-workforce-plan-v1.png`
- 固定组件树：`Canvas > PhaseInsightA + PhaseInsightB + PeakCard + LongTrendChart + LongWorkforceHeatmap`

| 组件 | x | y | w | h | 固定规则 |
|---|---:|---:|---:|---:|---|
| PhaseInsightA | 3 | 4 | 36 | 13 | 第一阶段原文结论；阶段近似人数保持正文色，不与全周期精确峰值争夺红色 |
| PhaseInsightB | 40.5 | 4 | 39.5 | 13 | 第二阶段原文结论；只有数值等于全周期精确峰值时才允许标红 |
| PeakCard | 82 | 4 | 15 | 13 | 全矩阵精确峰值、单位与峰值月份；不得用阶段近似描述替代 |
| LongTrendChart | 3 | 20 | 94 | 28 | 13–30 个连续时段的蓝色折线与浅蓝面积；全部节点对应合计行，唯一峰值为红色 |
| LongWorkforceHeatmap | 3 | 52 | 94 | 45 | 完整工种 × 时段矩阵；按年份分组表头、深蓝合计行、精确峰值单元格为红色 |

组件内部规则：

- 阅读顺序固定为 PhaseInsightA → PhaseInsightB → PeakCard → LongTrendChart → LongWorkforceHeatmap，不得把长周期页退化为单独一张普通表格。
- 两个阶段结论逐字保留源文，不用精确峰值反向改写原文中的“约”“高峰期范围”等管理表达；PeakCard 单独显示由矩阵计算得到的全周期精确峰值。
- LongTrendChart 和 LongWorkforceHeatmap 共享同一 13–30 列等分时段网格，并按年份增加固定分组表头。横轴不得抽样、合并月份或省略零值月份。
- 趋势图节点、合计行和 PeakCard 必须引用同一 `monthly_totals`。红色只落在全部并列最大值对应的 PeakCard 数字、趋势节点/标签与合计单元格。
- 热力矩阵首列固定为工种，末行固定为合计；工种顺序与源表一致。全矩阵采用统一中建蓝强度域，0 值使用暖象牙或近白中性灰，低值才进入浅蓝。
- 26–30 列时允许矩阵数字使用该模板登记的小号数据字级，但阶段结论、峰值卡和趋势标签不得缩小；不得为单页改变框架坐标、列间距或年份分组高度。
- `icon_plan: none — exact analytical matrix`。该类型不添加装饰性图标，数据图表和热力矩阵本身构成视觉语法。
- 长周期页同样控制蓝色系不超过 30%，并用白/暖中性非数据表面分隔年份与阶段，不允许用第二业务色区分年份。
- 本模板同样适用分析页比例例外：默认主、微辅助色均为 `none` 且无源图时，白色与浅中性色可占 68%–82%，不得为了凑色增加无语义的业务色。
- 所有 PrimaryFrame 继续使用全局 `x=3%`、`right=97%` 对齐线；默认 2000px 宽画布同侧边界误差不得超过 2px。

## risk-analysis-measures-series-v1

- `page_type`: `risk-analysis-measures-series`
- `template_id`: `risk-analysis-measures-series-v1`
- 固定微辅助色：`orange`，只用于“措施”短线微标识且不超过 1%；页面主辅助色按语义选择，目标 6%–10%、硬上限 10%，主/微合计不得超过 12%
- 固定组件树：`Canvas > AnalysisHeader + MeasuresHeader + ContentBody`

| 组件 | x | y | w | h | 固定规则 |
|---|---:|---:|---:|---:|---|
| AnalysisHeader | 3 | 4 | 94 | 13 | 固定“分析”文字、`measure` 图标、图标底板、字体、字号、内边距和基线；关键原文可在正文行内标红 |
| MeasuresHeader | 3 | 19 | 94 | 7 | 固定“措施”文字、`plan` 图标、中建蓝字体和工程橙短线；不得移动、换色或改字号 |
| ContentBody | 3 | 28 | 94 | 69 | 只允许选择下列已登记密度状态；外框、顶部基线和底部基线固定 |

标签排版等式属于模板指纹：`AnalysisLabel.font_family = MeasuresLabel.font_family`，`AnalysisLabel.font_size = MeasuresLabel.font_size`，默认 `font_weight` 也相等。组件框高度不同不构成改变字号的理由；两个标签必须在视觉上同级、等大。

`ContentBody` 密度状态：

- `text-photo`：左侧 58% 为 2–4 张措施卡，右侧 40% 为 1 张主照片；卡片与照片顶底对齐。
- `four-card`：2×2 等分措施卡；每卡一个同系列线性图标，卡片几何一致。
- `photo-gallery`：3–4 张等高照片卡，标题带和图标位置一致；文字只放在固定说明槽位。
- `before-after`：左右 1:1 对比卡，中间固定箭头；“前/后”状态标签位置一致。
- `three-stage`：三列等宽阶段卡，箭头和阶段标签位于固定基线。

状态选择只由实体关系和照片/文字数量决定，不改变 `AnalysisHeader`、`MeasuresHeader` 或 `ContentBody` 外框。若容量超出，升级模板版本并迁移整个系列，不得只为一页临时移动组件。

关键强调规则：每页在内容账本填写 `critical_phrases`，只允许把其中 1–3 个原文数字、关键词组、风险、动作或结果逐字渲染为 `#E60012`；其余文字保持深蓝灰。禁止整段红色、同义改写后标红或无来源的营销式强调。

## material-quantity-top10-v1

- `page_type`: `overview`
- `template_id`: `material-quantity-top10-v1`
- 适用内容：6–10 类主要材料/设备的工程量对比，同时需要保留逐项详细说明
- 默认主辅助色：`none`；默认微辅助色：`none`；界面使用中建蓝、白、暖象牙、浅中性灰与唯一强调红，材料缩略图的自然色不计入辅助色
- 固定组件树：`Canvas > InsightLine + QuantityRanking + MaterialDetailGrid`
- 固定 `icon_plan`: `section-header -> semantic-line`; `QuantityRanking -> none — exact bar chart`; `MaterialDetailGrid items -> realistic-thumbnail`

| 组件 | x | y | w | h | 固定规则 |
|---|---:|---:|---:|---:|---|
| InsightLine | 3 | 3 | 94 | 8 | 原文管理结论；只标登记过的关键短语，不绘制页面标题栏 |
| QuantityRanking | 3 | 13 | 94 | 29 | 横向 6–10 个等宽材料工程量柱；每柱只显示材料名称与工程量，不放序号、图标或缩略图 |
| MaterialDetailGrid | 3 | 45 | 94 | 52 | 2×3、2×4 或 2×5 等宽卡片；顺序与上方排名一致，每卡固定序号、缩略图、名称、红色数量和完整说明 |

组件内部规则：

- `QuantityRanking` 和 `MaterialDetailGrid` 的材料顺序必须一致；不得为了构图把上、下两区重新排序。上方柱状图仅保留名称与工程量，禁止重复放置材料缩略图、序号徽章、图例或说明文字。
- 工程量单位逐字保留。不同量纲可以同页比较展示，但不得伪装为可直接相加的统一统计口径；柱高只表达源页登记的排名或采用注明的视觉缩放。
- `MaterialDetailGrid` 容量为 6–10 项；6 项使用 2×3，7–8 项使用 2×4，9–10 项使用 2×5。两行卡片高度相等，同列边界对齐。
- 写实缩略图遵循 `icon-system.md` 的 `realistic-thumbnail`：统一约 3/4 视角、白底抠图、中性棚拍光、柔和接触阴影、无品牌、无文字。材料自然色只用于物体本身，UI 仍由中建蓝主导。
- 材料自然色在有真实来源时优先承担约 8%–18% 的页面色彩层次；禁止给木材、石材、金属和玻璃统一套蓝色滤镜。无材料图时不得为配色丰富虚构材料缩略图。
- 栏目级小图标可使用 `semantic-line`，下方材料明细卡使用 `realistic-thumbnail`；不得在上方工程量柱中放图标或缩略图，也不得在下方材料条目中混入线性或卡通图标。
- 红色默认只用于登记过的关键结论短语与逐项数量；当页面的分析任务就是工程量排名时，10 个数量属于一个“分析数据系列”，允许整组使用唯一强调红，不受通常 1–3 个短语上限约束，但红色面积仍不得超过画布 5%。
- 所有文字和工程说明逐字保留；密度不足时先缩短行宽、压缩段间距，再使用模板登记的小号注释字级，不能删项或概括。

## 通用模板映射

| page_type | template_id | 旧 layout |
|---|---|---|
| cover | cover-hero-v1 | cover |
| overview | overview-cards-v1 | overview |
| deployment | deployment-zones-v1 | deployment |
| method | method-control-v1 | method |
| bim | bim-application-v1 | bim |
| schedule | schedule-milestones-v1 | schedule |
| risk | risk-closed-loop-v1 | risk |
| risk-analysis-measures-series | risk-analysis-measures-series-v1 | risk |
| labor-workforce-plan | labor-workforce-plan-v1 | overview |

通用模板用于尚未建立专用坐标合同的页面。若同一结构反复出现，新增专用版本化模板，登记组件树、百分比坐标、容量和溢出规则后再使用。不要把临时生成结果反向当成模板。

所有通用模板都必须执行 `icon-system.md` 的触发判定。触发后，`icon_plan` 属于模板指纹：主要模块必须配置图标，且同一 `series_key + page_type` 的 icon_id、容器、尺寸和坐标不得漂移。
