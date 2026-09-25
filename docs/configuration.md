# 配置详解

配置文件支持 YAML 与 JSON，通过 `load_config(path)` 加载（无 PyYAML 时自动回退内置解析器）。

## 字段

| 字段 | 默认 | 说明 |
|---|---|---|
| `backend.kind` | mock | 后端类型：mock / openai / vllm / transformers |
| `backend.skill` | 0.62 | mock 后端的能力值（0~1） |
| `backend.noise` | 0.3 | mock 后端噪声幅度 |
| `backend.base_url` | "" | OpenAI 兼容接口地址 |
| `backend.model` | jev-4b-mock | 模型名 |
| `engine.mode` | argmax | 选择策略：argmax / sample / topk |
| `engine.temperature` | 1.0 | softmax 温度 |
| `engine.min_confidence` | 0.0 | 置信度门槛 |
| `planner.kind` | hybrid | 规划器：hybrid / beam / monte_carlo |
| `planner.beam_width` | 4 | 束宽 |
| `planner.depth` | 4 | 前瞻深度 |
| `planner.rollouts` | 32 | MC rollout 次数 |
| `planner.survival_weight` | 0.4 | 生存空间权重 |
| `serving.host/port` | 127.0.0.1:8000 | HTTP 服务地址 |
| `serving.token` | "" | Bearer 鉴权 token（空则不鉴权） |
| `serving.rate_limit` | 60 | 每分钟请求上限 |

## 示例

见 `configs/` 目录下的 `config.yaml` / `config.json` / `openai.yaml` / `vllm.yaml` / `highskill.yaml`。
