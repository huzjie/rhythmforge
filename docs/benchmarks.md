# 六组基准评测

| 基准 | 全称/含义 | 考察能力 |
|---|---|---|
| Nimble | Reflex | 敏捷反射决策 |
| VitaminC | Commonsense | 常识判断 |
| MASSIVE | Intent (SLU) | 意图分类 |
| Transfer | Generalization | 规则迁移 |
| Knowledge | Factual recall | 知识召回 |
| Semantic | Entailment | 语义判断 |

每组包含若干 `(context_key, actions, correct)` 三元组，引擎逐条决策后按命中率计分，最后取六组平均得到 AVG 综合分。

```bash
python -m rhythmforge bench
# AVG = 91.67
#   nimble       100.00
#   vitaminc     100.00
#   ...
```
