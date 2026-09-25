# 架构设计

## 分层

rhythmforge 采用四层架构，层与层之间通过最小接口解耦：

1. **Backend 层**：`DecisionModelBackend.score_actions(context_key, actions, state, history) -> List[float]`，只负责"打分"。
2. **Engine 层**：`RealtimeDecisionEngine.decide(context) -> DecisionResult`，负责"打分 → 分布 → 选择"。
3. **Planner 层**：`LookaheadPlanner.plan(env, state) -> Plan`，负责"向前看 + 生存空间评估"。
4. **Env 层**：`DecisionEnv`，负责"状态推进 + 奖励 + 终止"，供规划器做 rollout。

## 关键设计：能力与偏差分离

Mock 后端把"能力"与"偏差"拆成两个正交信号：

```
score = skill * truth(动作) + prefer_first * 位置偏置 + noise
```

- `truth` 是稳定隐藏的"正确答案"信号；
- `prefer_first` 是"倾向于选靠前选项"的位置偏差；
- 二者**加法分离**，让规划器/基准能测量到真实决策质量，而非被偏差污染。

这样，`skill` 的升降能真实反映在基准准确率上。

## 生存空间评估

`SafetyEvaluator.survival(state)` 用 flood-fill 从蛇头开始统计可达自由格子数，作为"还有多少回旋余地"的度量。规划器在分支评分里加上 `survival_weight * survival`，从而倾向选择"保命空间更大"的路径——这正是贪吃蛇活到 3000 步的关键。

## 为什么是零依赖

实时决策场景常常跑在边缘/受限环境里，第三方依赖（尤其 YAML 解析、HTTP 客户端）可能不可用。因此核心只用标准库，YAML 解析器（`utils/yamlish.py`）为内置回退，HTTP 服务基于 `http.server`。
