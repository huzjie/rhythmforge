# rhythmforge

> 实时决策引擎 + 前瞻安全规划框架（Realtime Decision Engine & Lookahead Safety Planner）
> 灵感来源：基元律动（tokenrhythm.ai）开源的 **NeoHorse-Jev-4B** 实时决策模型

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)
[![Zero deps](https://img.shields.io/badge/core-zero--dependency-brightgreen)](#零依赖)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](.github/workflows/ci.yml)

---

## 一句话说清它是干什么的

**rhythmforge 是一个"毫秒级实时决策"的完整工程框架。** 它解决的是这样一类问题：在连续、长程、每一次选择都会影响后续生存空间的场景里（贪吃蛇、实时导航、游戏 AI、交易撮合、机器人避障……），怎么让一个轻量决策模型在**每一步都快速做出判断**，同时**不把后续的路走死**。

框架把这件事拆成三个可独立替换的部件：

1. **决策模型后端（Backend）** —— 负责"给定当前状态和候选动作，给每个动作打分"；
2. **实时决策引擎（Engine）** —— 把打分变成概率分布，毫秒级选出动作；
3. **前瞻安全规划器（Planner）** —— 向前看几步，评估每个分支的"生存空间"，避免贪心短视。

三者拼起来，就是你自己的"实时决策智能体"。

---

## 为什么是这个方向

2026-09-25，基元律动（由华为诺亚方舟实验室前主任王云鹤创办）开源了 **NeoHorse-Jev-4B**——一个仅 40 亿参数的实时决策模型，主打毫秒级响应。它在贪吃蛇测试中实现了 **3000 步、89 个目标、蛇身长度 95** 的存活记录，并以 **77.70 的综合 AVG 分数**拿下开源参评模型第一。

它揭示了一个关键工程事实：**"实时决策"不等于"更快地算"，而是"每一步都算得对 + 不把自己逼进死角"。** 蛇越吃越长，留给自己的活动空间被不断压缩，任何一次错误转向都可能瞬间结束整局。这正是"前瞻安全规划"要解决的：不仅要当前最优，还要保证未来有路可走。

rhythmforge 把这套思想做成可复用的框架，让你不需要 4B 模型权重，也能在自己的业务场景里搭起同构的实时决策系统。

---

## 核心能力

| 能力 | 说明 |
|---|---|
| ⚡ 毫秒级决策引擎 | 候选动作枚举 → 打分 → softmax → 选择，一次决策亚毫秒级（mock 后端约 0.01ms） |
| 🛡️ 前瞻安全规划 | Beam Search / Monte-Carlo / Hybrid 三种规划器，向前看 N 步评估"生存空间" |
| 🔌 可插拔后端 | 确定性可训练 Mock / OpenAI 兼容 / vLLM / Transformers，写 20 行即可自定义 |
| 📊 六组基准评测 | Nimble / VitaminC / MASSIVE / Transfer / Knowledge / Semantic + AVG 综合分 |
| 🐍 参考环境 | 贪吃蛇、网格世界两个内置环境，开箱即用演示 |
| 🌐 零依赖 HTTP 服务 | 纯标准库实现，带 Bearer 鉴权 + 限流 + 客户端 |
| 🐳 完整部署 | Docker / docker-compose / Kubernetes / Helm / GitHub Actions CI |
| 🔧 零依赖内核 | 核心不依赖任何第三方库，连 YAML 解析都自带回退 |

---

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/huzjie/rhythmforge.git
cd rhythmforge

# 2. 安装（可选，零依赖内核可直接运行）
pip install -e .

# 3. 跑一个最简决策
python -m rhythmforge demo
# 输出: decision: up  confidence=0.412  latency=0.01ms

# 4. 跑六组基准评测
python -m rhythmforge bench

# 5. 贪吃蛇演示（贪心 vs 前瞻安全规划对比）
python examples/demo_snake.py
```

不需要 GPU、不需要 API Key、不需要下载模型权重，上面的命令在任意 Python 3.9+ 环境都能跑。

---

## 配置后直接接真实模型

把 `configs/config.yaml` 里的后端换成 OpenAI 兼容接口，填上 `base_url` / `model` / `api_key`，即可接真实模型：

```yaml
backend:
  kind: openai
  base_url: https://api.openai.com/v1
  model: gpt-4o-mini
  api_key: ${OPENAI_API_KEY}
```

接本地 vLLM：

```yaml
backend:
  kind: vllm
  base_url: http://127.0.0.1:8000/v1
  model: tokenrhythm/NeoHorse-Jev-4B
```

然后用 `python -m rhythmforge --config configs/openai.yaml bench` 直接开跑。

---

## 架构一览

```
                    ┌────────────────────────────┐
   决策请求 ──────▶ │   RealtimeDecisionEngine   │ ◀── DecisionModelBackend
  (context+actions) │  枚举 → 打分 → softmax → 选 │       (mock/openai/vllm/...)
                    └────────────┬───────────────┘
                                 │ 候选 + 分布
                    ┌────────────▼───────────────┐
                    │  LookaheadSafetyPlanner    │
                    │  beam / monte-carlo / hybrid│
                    │  向前看 → 生存空间评估      │
                    └────────────┬───────────────┘
                                 │ 最终动作
                    ┌────────────▼───────────────┐
                    │      DecisionEnv           │
                    │   snake / gridworld / 自定义 │
                    └────────────────────────────┘
```

完整设计见 [docs/architecture.md](docs/architecture.md)。

---

## 项目结构

```
rhythmforge/
├── rhythmforge/              # 核心包（零依赖）
│   ├── backend/              # 决策模型后端（mock/openai/vllm/transformers）
│   ├── engine/               # 实时决策引擎 + 动作空间 + 缓存
│   ├── planner/              # 前瞻安全规划器（beam/mc/hybrid + 生存空间评估）
│   ├── benchmark/            # 六组基准评测 + AVG 综合评分
│   ├── envs/                 # 贪吃蛇 / 网格世界环境
│   ├── serving/              # 零依赖 HTTP 服务 + 客户端
│   ├── cli/                  # 命令行入口
│   └── utils/                # 确定性哈希 / 熵 / YAML 回退解析 / 计时
├── examples/                 # 9 个可运行示例
├── tests/                    # 8 个单测模块（unittest，零依赖）
├── configs/                  # 多种配置示例
├── docs/                     # 架构 / 使用 / API / 设计文档
├── models/                   # 模型卡
├── deploy/                   # Docker / K8s / Helm
└── .github/workflows/        # CI / Docker / Benchmark
```

---

## 文档导航

- [docs/architecture.md](docs/architecture.md) —— 架构设计
- [docs/getting_started.md](docs/getting_started.md) —— 上手教程
- [docs/configuration.md](docs/configuration.md) —— 配置详解
- [docs/benchmarks.md](docs/benchmarks.md) —— 六组基准说明
- [docs/api.md](docs/api.md) —— HTTP API
- [docs/design.md](docs/design.md) —— 核心设计决策
- [docs/faq.md](docs/faq.md) —— 常见问题
- [models/model_card_jev4b.md](models/model_card_jev4b.md) —— 模型卡

---

## 测试

```bash
python -m unittest discover -s tests -t .
```

## 部署

```bash
# Docker
docker build -f deploy/Dockerfile -t rhythmforge .
docker run -p 8000:8000 rhythmforge

# Kubernetes
kubectl apply -f deploy/k8s/

# Helm
helm install rhythmforge deploy/helm
```

## License

[Apache-2.0](LICENSE)

> 本项目为独立实现的实时决策框架，灵感来自 NeoHorse-Jev-4B 的设计思想；未包含其模型权重，与基元律动（tokenrhythm.ai）无隶属关系。
