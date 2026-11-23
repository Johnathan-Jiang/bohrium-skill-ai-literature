# 参考文献与引用管理 Skill

对稿件与文献库做引用定位、编号连锁更新、去重合并、格式转换与来源核验，交付正文—文献表一致的稿件。

## 文件结构

- `SKILL.md` — Skill 本体。
- `scripts/reference_consistency.py` — 引用一致性校验脚本。
- `references/dedup-rules.md` — 去重判据与格式映射（GB/T 7714 / APA / Vancouver / IEEE）。
- `examples/minimal-example.md` — 最小调用示例（标注为示例）。

## 用法

Agent 加载 `SKILL.md`，建"论断—引用—文献"映射，编号重排、去重、格式化、逐条核验。

## 校验脚本

```bash
python3 scripts/reference_consistency.py result.json
```

检查项：文末编号连续、引用—文献映射齐全、去重可解释。退出码 0=通过。

## 输出

`result.json` 含：`edited_manuscript`、`reference_list`、`citation_map`、`dedup`、`verification`、`sources`、`uncertainty`、`change_records`。

## 依赖

Python 3 标准库。

## 限制

字段缺失/DOI 解析失败时标 `uncertain`，不编造元数据；正文论断与文献不匹配时建议人工确认，不擅自换文献。
