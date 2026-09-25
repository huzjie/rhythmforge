# Model Card: rhythmforge Mock Backend

- **类型**：确定性可训练决策后端（模拟）
- **能力建模**：`skill ∈ [0,1]`，通过奖励反馈训练
- **偏差建模**：`prefer_first` 位置偏置 + `noise` 噪声
- **确定性**：md5 种子，跨运行可复现
- **用途**：离线开发、单元测试、基准评测、演示
