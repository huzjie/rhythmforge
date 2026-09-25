# 扩展基准：Reflex 与 Safety

在默认六组之外，框架还提供两组可选基准：

| 基准 | 说明 |
|---|---|
| Reflex | 扩展的敏捷反射决策 |
| Safety | 风险感知的安全决策 |

通过 `benchmark.tracks` 配置启用：

```yaml
benchmark:
  tracks: [nimble, vitaminc, massive, transfer, knowledge, semantic, reflex, safety]
```
