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

通用模板用于尚未建立专用坐标合同的页面。若同一结构反复出现，新增专用版本化模板，登记组件树、百分比坐标、容量和溢出规则后再使用。不要把临时生成结果反向当成模板。

