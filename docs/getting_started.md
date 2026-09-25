# 上手教程

## 环境

- Python 3.9+
- 无需 GPU、无需外部 API（使用内置 mock 后端时）

## 三步跑通

```bash
python -m rhythmforge demo      # 一次决策
python -m rhythmforge bench     # 六组基准
python examples/demo_snake.py   # 贪吃蛇（贪心 vs 前瞻）
```

## 用自己的后端

```python
from rhythmforge.backend.base import DecisionModelBackend
from rhythmforge.engine.decision_engine import RealtimeDecisionEngine
from rhythmforge.types import DecisionContext

class MyBackend(DecisionModelBackend):
    kind = "my"

    def score_actions(self, context_key, actions, state=None, history=None):
        # 返回每个动作的打分（越高越好）
        return [len(a) for a in actions]

engine = RealtimeDecisionEngine(MyBackend(), {"mode": "argmax"})
print(engine.decide(DecisionContext(key="x", actions=["a", "bb", "ccc"])).chosen_action)
```

## 接真实模型

编辑 `configs/openai.yaml` 填好 `base_url` / `model` / `api_key`，然后：

```bash
python -m rhythmforge --config configs/openai.yaml bench
```
