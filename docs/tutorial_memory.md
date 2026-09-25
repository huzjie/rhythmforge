# 教程：决策记忆与重放

- `EpisodicMemory`：存储 `(context, action, outcome)` 三元组，支持召回与最佳动作查询。
- `ReplayBuffer`：用于训练 mock 后端的经验回放池。

```python
from rhythmforge.memory.episodic import EpisodicMemory
m = EpisodicMemory()
m.store("ctx.1", "right", 1.0)
print(m.best_action("ctx.1"))  # right
```
