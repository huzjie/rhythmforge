# 教程：自定义决策环境

实现 `DecisionEnv` 接口的 4 个方法，即可交给规划器做前瞻：

```python
from rhythmforge.envs.base import DecisionEnv

class MyEnv(DecisionEnv):
    def reset(self, seed=None): ...
    def available_actions(self, state=None): ...
    def step(self, action): ...
    def clone(self): ...
```

参考 `rhythmforge/envs/snake.py`、`gridworld.py`、`tictactoe.py`、`bandit.py`。
