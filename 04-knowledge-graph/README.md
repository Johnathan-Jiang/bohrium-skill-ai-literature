# 文献知识图谱构建 Skill

从一批论文抽取真实出现的实体与有证据支撑的关系，绑定原文位置，交付可查询的图谱（节点+边+证据）。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/validate_graph.py` — 图谱结构校验脚本。
- `references/graph-schema.md` — 实体/关系类型、导出 Schema、对齐与证据规则。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，抽实体 → 抽关系 → 别名归一 → 绑证据 → 导出 nodes/edges/evidence → 回答查询。

## 校验脚本

```bash
python3 scripts/validate_graph.py result.json
```

检查项：节点带位置、边端点存在、每条边有证据。退出码 0=通过。

## 输出

`result.json` 含：`nodes`、`edges`、`query_results`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库。

## 限制

只建立有证据支撑的关系；共现/转述/推测不当直接证据；同名实体无法确定时保留多节点并说明；查询无结果如实返回。
