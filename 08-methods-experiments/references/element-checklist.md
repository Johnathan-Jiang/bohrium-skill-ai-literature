# 方法/实验要素抽取清单与参数表模板

## 六类要素（逐类覆盖）

| 类型 | 说明 |
|---|---|
| `step` | 方法步骤（有序、可执行） |
| `setting` | 实验设置（环境、硬件、软件版本） |
| `parameter` | 参数（取值 + 来源位置） |
| `dataset` | 数据集与划分（版本、规模、train/val/test 划分） |
| `control` | 对照实验与重复次数 |
| `reproducibility` | 复现要素（随机种子、命令、依赖版本） |

## 参数表模板

| name | value | source | status |
|---|---|---|---|
| learning_rate | 1e-4 | config.yaml L12 | confirmed |
| random_seed | ? | 未记录 | missing |

- `status=confirmed`：值有来源（文件+行号）。
- `status=missing`：无来源，正文不写具体值，列入"待作者确认"。
- 配置冲突时并列两种取值，列入 `uncertainty`。

## 缺口追问清单

`{ item, missing, action }`——每个缺口指向具体缺失项，不写套话。
