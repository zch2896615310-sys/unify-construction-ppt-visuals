# Unify Construction PPT Visuals

面向工程技术标、述标汇报、专项施工方案、施工部署与 BIM 应用 PPT 的视觉统一 Skill。

它会先理解页面目的、实体、关系和阅读顺序，再重新组织版式；不要求照抄原页面，但必须完整保留主要内容、数字和工程事实。默认交付透明 PNG。可见内容包围盒严格为 2:1，四边透明留白像素相等，画布比例不限。内容区省略标题栏、企业标识、页码和页脚。每页使用 ImageGen 完成整页生成或编辑。

## 一句话安装

在支持 `$skill-installer` 的 Codex 中粘贴这句话。使用此 Skill 需要可用的 ImageGen，运行透明边距验收脚本需要 Python 和 Pillow。

> 请使用 `$skill-installer`，从 GitHub 仓库 `zch2896615310-sys/unify-construction-ppt-visuals` 的路径 `skills/unify-construction-ppt-visuals` 安装 Skill。

安装完成后，新 Skill 通常会在下一轮对话中可用；如果没有出现，请重启 Codex。

## 一句话更新

> 请把已安装的 `unify-construction-ppt-visuals` 备份后替换为 `zch2896615310-sys/unify-construction-ppt-visuals` 仓库 `main` 分支中 `skills/unify-construction-ppt-visuals` 路径的最新版本，并验证 `SKILL.md`。

安装器默认不会覆盖同名目录，因此更新时需要先备份或移除旧版本，再重新安装。

## 典型用法

- “按中建蓝述标风格美化这几页 PPT，保持跨页一致。”
- “只生成表头以下的内容区，可见内容为 2:1，四边留等宽透明边距。”
- “不拘泥原排版，先理解内容，再重新排版，主要内容和数据不变。”
- “这两页内容结构相似，请使用同一个固定模板。”

也可以显式调用：

> 使用 `$unify-construction-ppt-visuals` 美化这些工程 PPT 页面。

## 设计原则

1. 先建立内容账本和语义模型，再开始排版。
2. 首次设计同类页面时允许重构旧版式；模板冻结后，同类页面只替换数据。
3. 中建蓝控制关键层级。有明确源配色时提炼核心语义色，近乎单色时辅助色至少覆盖可见内容的 20%。劳动力计划沿用固定冷色方案。
4. 重复模块、阶段、设备、施工区和班组使用统一的视觉标识。抽象概念使用线性图标，适合凭外形识别的材料和设备可以使用写实缩略图。
5. 中文文字、数字、专业逻辑和源图事实优先于装饰效果。
6. 每个输出页面必须由 ImageGen 独立完成整页生成或整页编辑；确定性工具仅用于内容提取、数据计算、尺寸检查和少量精确修正。

## 示例

二标段劳动力投入计划：

![二标段劳动力投入计划](labor-plan-section-2.png)

一标段劳动力投入计划：

![一标段劳动力投入计划](labor-plan-section-1.png)

## 仓库结构

```text
skills/unify-construction-ppt-visuals/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── icons/construction-line-icons.svg
│   ├── references/construction-zone-floor-schedule-{before,after}.png
│   └── templates/labor-workforce-plan-v1.png
├── references/
│   ├── gantt-layout-system.md
│   ├── icon-system.md
│   ├── output-geometry.md
│   ├── prompt-contract.md
│   ├── style-bible.md
│   └── template-registry.md
└── scripts/
    ├── build_prompts.py
    └── check_output_geometry.py
```

## License

[MIT License](LICENSE)
