---
name: literature-knowledge-graph
description: 从一批论文抽取实体与关系、绑定证据并支持查询的可运行知识图谱工作流。用于实体关系抽取、别名归一、来源绑定、图谱导出、关系查询、增量更新等任务；需要"抽得准、连得对、对得齐、查得到回得去"时触发。
---

# 文献知识图谱构建：带证据的节点与边

从论文抽取真实出现的科研对象（实体）与有证据支撑的关系，绑定原文位置，交付可查询的图谱（节点+边+证据）。

## 运行契约

- 输入：`/input/task.md`、`/input/case.json`、`resources.yaml` 及实际论文文件。
- 工作目录 `/app/work`；最终结果写入 `/app/output/`。
- 先读真实文件；文献缺失、PDF 无法解析、实体同名、关系证据冲突、查询无结果等情况如实记录。
- `/app/output/result.json` 必须包含：`case_id`、`status`、`output_contract` 全部字段、`sources`、`uncertainty`、`change_records`。
- 预算 64 次模型请求 / 900 秒：先抽实体，再抽关系并归一，最后绑证据、导出、回答查询。
- 图谱导出用 JSON（节点/边/证据分离），保证可机器解析；可附查询结果。

## 工作流

1. **识别边界**：读 `task.md`/`case.json`，确认主题、要抽取的实体/关系类型、别名归一口径、查询问题、导出格式。
2. **抽实体**：抽取论文里真实出现的科研对象（研究者、材料、方法、任务、指标、结论），保留原文表述与原文位置，区分作者自述与他人转述。**不凭常识补概念**。
3. **关系抽取**：只建**有证据支持**的关系；关系类型、方向、适用条件与原文一致。不把共现、综述转述或推测当直接证据。
4. **实体对齐/归一**：处理别名、缩写、大小写、全称与简称、同名实体；合并给依据，不产生重复节点，也不把不同对象错误合并。
5. **绑证据**：每个节点、每条边都指向论文具体位置（页码/段落/图表）+ 原文片段。
6. **导出与查询**：生成 `references/graph-schema.md` 定义的 nodes/edges/evidence 结构，并回答 `task.md` 的查询问题（查得到且能回到原文）。
7. **输出**：nodes + edges + evidence + query_results，写入 `result.json`，并运行 `python3 scripts/validate_graph.py result.json` 校验节点/边/证据。

## 四条硬规则

### 抽得准
- 实体必须对应论文里真实出现的对象，不把模型常识补全的概念当实体。
- 标注每个实体的来源表述与证据定位，区分作者自述/他人转述。

### 连得对
- 关系类型、方向、适用条件与原文一致；共现≠因果关系，综述转述≠作者结论，推测≠直接证据。

### 对得齐
- 别名/缩写/大小写/同名冲突正确处理；合并或保留不同节点都要给依据。

### 查得到、回得去
- 图谱能回答真实查询；每个节点和每条边能回到论文具体位置和原文片段。

## 输出结构

`/app/output/result.json`（合并 task.md 的 `output_contract`）：

```json
{
  "case_id": "...",
  "status": "success|partial|unable",
  "nodes": [
    {"id": "N1", "type": "method", "label": "...", "mentions": ["p2 ¶1"], "quote": "...", "voice": "author|cited"}
  ],
  "edges": [
    {"id": "E1", "source": "N1", "target": "N2", "relation": "improves", "condition": "...", "evidence": {"quote": "...", "locator": "p4 ¶2"}, "evidence_level": "direct|paraphrase|inferred"}
  ],
  "query_results": [{"query": "...", "answer": "...", "nodes": ["N1"], "evidence_locators": ["p4 ¶2"]}],
  "sources": [...],
  "uncertainty": [{"item": "N3/N4 同名", "issue": "...", "action": "保留为两节点并记录依据"}],
  "change_records": [...]
}
```

## 异常处理

- 文献缺失/PDF 无法解析：`status="unable"` 或 `partial`，说明缺什么。
- 实体同名：无法确定是否同一对象时保留为多个节点，列入 `uncertainty`，不武断合并。
- 关系证据冲突：保留双方证据，标注冲突，不下单一结论。
- 查询无结果：如实返回"无结果"并说明原因，不编造答案。
- 增量更新：已有图谱时给出新增/修改/合并的差异记录。

## 自查清单

1. 实体是否都真实出现在论文里，且有原文位置？
2. 关系是否有证据支撑，类型/方向/条件是否与原文一致？
3. 别名/同名是否处理正确，合并或保留是否给了依据？
4. 每个节点和每条边能否回到原文？
5. 查询是否真实可回答且回得去？
6. `result.json` 是否字段齐全、状态诚实？

最小调用示例见 `examples/minimal-example.md`（标注为示例）。
