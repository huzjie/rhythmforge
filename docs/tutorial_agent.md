# 教程：用 RealtimeAgent 驱动环境

```python
from rhythmforge.agents.realtime_agent import RealtimeAgent
from rhythmforge.agents.policies import PlannerPolicy
from rhythmforge.envs.snake import SnakeEnv
from rhythmforge.pipeline import RhythmForge

rf = RhythmForge()
agent = RealtimeAgent(rf, policy=PlannerPolicy(rf.planner))
state = agent.run_episode(SnakeEnv(20, 20), seed=5, max_steps=500)
print(agent.summary())
```

`RealtimeAgent` 封装了"感知 → 决策 → 行动 → 学习"完整循环，支持三种策略：
- `GreedyPolicy`：每步用引擎选最优
- `PlannerPolicy`：每步用前瞻安全规划器
- `EpsilonGreedyPolicy`：带探索率的贪心
