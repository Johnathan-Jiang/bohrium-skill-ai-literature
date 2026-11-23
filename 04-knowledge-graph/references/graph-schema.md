# 知识图谱实体/关系定义与导出 Schema

## 实体类型（受控，可扩展须声明）

| 类型 | 说明 |
|---|---|
| `researcher` | 研究者/团队 |
| `material` | 材料/对象/数据集 |
| `method` | 方法/算法/模型 |
| `task` | 任务/问题 |
| `metric` | 指标/评价标准 |
| `conclusion` | 结论/发现 |

## 关系类型（受控，方向显式）

| 关系 | 含义 | 方向示例 |
|---|---|---|
| `improves` | 提升/优于 | 方法 → 指标 |
| `uses` | 使用/采用 | 方法 → 材料/数据 |
| `compares_to` | 与…比较 | 方法 → 方法 |
| `applies_to` | 适用于 | 方法 → 任务 |
| `produces` | 产生/得到 | 方法/材料 → 结论 |
| `contradicts` | 与…矛盾 | 结论 → 结论 |

## 导出 Schema（JSON）

```json
{
  "nodes": [{"id": "N1", "type": "method", "label": "...", "mentions": ["p2 ¶1"], "quote": "...", "voice": "author|cited"}],
  "edges": [{"id": "E1", "source": "N1", "target": "N2", "relation": "improves", "condition": "...", "evidence": {"quote": "...", "locator": "p4 ¶2"}, "evidence_level": "direct|paraphrase|inferred"}]
}
```

## 对齐与证据规则

1. 别名归一：缩写/全称/大小写合并，记录合并依据；无法确定是否同一对象时保留多节点并列入 `uncertainty`。
2. 同名不同对象：不合并，用 `note` 区分。
3. `voice`：`author`=作者自述，`cited`=引用他人转述，二者不混。
4. 每条边必须有 `evidence.quote` + `evidence.locator`；共现/转述/推测不能当直接证据。
5. 查询无结果时如实返回，不编造答案。
