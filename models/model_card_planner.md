# Model Card: Lookahead Safety Planner

- **类型**：前瞻规划器（非神经网络）
- **算法**：Beam Search / Monte-Carlo rollouts / Hybrid
- **输入**：环境状态
- **输出**：动作序列 + 生存空间估计
- **用途**：避免长程决策中的"走死"问题
