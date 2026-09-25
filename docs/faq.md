# FAQ

**Q: 一定要下载模型权重吗？**
不用。内置 mock 后端零依赖即可运行，接真实模型只需改配置。

**Q: 没有 PyYAML 怎么办？**
内置 `utils/yamlish.py` 回退解析器，无第三方依赖也能读 YAML。

**Q: 怎么自定义环境？**
实现 `DecisionEnv` 接口的 `reset` / `available_actions` / `step` / `clone` 即可交给规划器。

**Q: 决策能多快？**
mock 后端约 0.01ms/次；接真实模型时延迟取决于模型推理速度。
