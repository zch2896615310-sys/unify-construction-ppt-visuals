# 页面类型与确定性模板注册表

## 基本合同

把页面结果定义为：

`页面结果 = 语义模型选择的固定模板 + 固定视觉令牌 + 页面数据`

模板选择必须发生在语义理解之后。旧页面的坐标、表格外观、文本框数量和留白不是分类依据；页面目的、实体、关系和阅读顺序才是分类依据。首次建立模板时允许重构旧排版，模板冻结后同类页面只实例化数据。

先按信息结构识别 `page_type`，再绑定 `template_id`。相同 `series_key + page_type` 只允许一个模板 ID。坐标均为相对于 2:1 内容画布的百分比，原点位于左上角；渲染时换算为整数像素，禁止逐页人工微调。

统一几何令牌：安全边距 3%；卡片圆角 1.2% 画布高；卡片描边 0.08% 画布宽；卡片间距 1.2% 画布宽；阴影参数、图标库、字号三级层级由 `style-bible.md` 固定。

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
- 默认辅助色：`orange`
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
- TotalBadge 固定在 SummaryCard 右端，不得在不同页面移到热力表旁或页面角落。
- 图标只用于稳定语义：施工区、楼层、班组、并行、资源总计。不得按页随机使用工人、建筑、齿轮等不同隐喻。
- 图标不是可选装饰。两张 ZoneCard 固定使用 `zone`，FloorSpine 使用 `floors`，四类 CrewChip 使用 `crew`，ParallelConnector 使用 `parallel`，ResourceHeatmap 总计使用 `shared`；几何按 `icon-system.md` 冻结。

## labor-workforce-plan-v1

- `page_type`: `labor-workforce-plan`
- `template_id`: `labor-workforce-plan-v1`
- 默认辅助色：`none`；仅用中建蓝、浅蓝灰与唯一强调红
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
- WorkforceHeatmap 首列固定为工种，末行固定为合计。单元格蓝色强度按全矩阵统一数值域映射；0 值使用最浅底色，禁止按单行分别归一化导致跨工种不可比较。
- 工种行顺序遵循源数据，不得按人数重新排序。需要突出持续主力工种时只允许加粗工种名和高值数字，不新增第二种彩色辅助色。
- 红色仅用于 `peak_value`：PeakCard 数字、TrendChart 峰值节点/标签、合计行对应单元格。其他月份与普通热力单元格不得使用红色。
- 月份/时段槽位支持 6–12 列，工种支持 8–16 行；在固定外框内等分列宽和行高。超出容量时升级模板版本并迁移同系列全部页面，不得局部压扁字号。
- 不使用装饰性小图标。该页的精确数据图表与矩阵本身构成主要视觉语法，声明 `icon_plan: none — exact analytical matrix`。
- 渲染前计算 `monthly_totals = sum(trade_rows)`、`peak_value = max(monthly_totals)`、`peak_month = argmax(monthly_totals)`，并核对源合计行。若并列峰值，所有并列峰值节点使用红色，但 PeakCard 按时间顺序列出月份，不擅自只选一个。

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
| labor-workforce-plan | labor-workforce-plan-v1 | overview |

通用模板用于尚未建立专用坐标合同的页面。若同一结构反复出现，新增专用版本化模板，登记组件树、百分比坐标、容量和溢出规则后再使用。不要把临时生成结果反向当成模板。

所有通用模板都必须执行 `icon-system.md` 的触发判定。触发后，`icon_plan` 属于模板指纹：主要模块必须配置图标，且同一 `series_key + page_type` 的 icon_id、容器、尺寸和坐标不得漂移。
