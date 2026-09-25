# 教程：可观测性

`DecisionStats` 记录每次决策的延迟、置信度、熵，`prometheus.py` 可导出 Prometheus 文本格式：

```python
from rhythmforge.observability.stats import DecisionStats
stats = DecisionStats()
# ... record decisions ...
print(stats.summary())
```
