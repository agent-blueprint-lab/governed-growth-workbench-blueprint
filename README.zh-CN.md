# 可治理增长工作台蓝图

这是一个小而完整的开源参考实现，用来演示如何以规则优先、隐私保护、失败关闭和人工审核的方式生成增长机会，而不是让模型直接读取敏感数据或自动触达。

**项目状态：** 早期开源参考实现。当前不声称已有生产部署、外部用户、下载量或广泛采用。

## 快速开始

需要 Python 3.11 或更高版本。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
make verify
```

`make verify` 会依次完成 Python 编译检查、公开内容敏感信息扫描、可执行测试，以及合成样例回放。输出位于 `build/`。

也可以直接运行：

```bash
ggw run \
  --profiles examples/profiles.synthetic.json \
  --rules config/rules.synthetic.json \
  --output build/opportunities.json \
  --audit-output build/audit-events.json
```

## 安全边界

- 本项目不连接真实数据库、模型 API、CRM、消息渠道或支付系统。
- 所有公开示例 ID 都必须以 `SYN-` 开头。
- 规则配置必须声明 `synthetic_demo_only: true`；示例数字只是测试夹具，不是生产阈值建议。
- 数据状态不是 `ready` 时不生成机会，只记录阻断审计事件。
- 联系限制、待核验关系和对照组状态优先于价值层级与任务优先级。
- 任何可执行结果都必须经过人工审核；引擎本身不能发送消息或写入外部系统。

## 四类执行状态

| 状态 | 含义 |
| --- | --- |
| `READY` | 数据和联系门禁通过，可以进入人工审核。 |
| `REVIEW` | 身份、关系或联系许可尚未核实。 |
| `HOLD` | 存在联系限制，不得执行。 |
| `CONTROL` | 属于稳定对照组，不生成主动执行动作。 |

## 参与贡献

请先创建 Bug 或规则提案 Issue，再通过 Pull Request 提交改动，并运行 `make verify`。安全漏洞或误提交敏感信息应通过 GitHub Security Advisory 私下报告，不要发布到公开 Issue。

详细说明见 [贡献指南](CONTRIBUTING.md)、[治理规则](GOVERNANCE.md)、[路线图](ROADMAP.md)、[变更记录](CHANGELOG.md) 和 [安全策略](SECURITY.md)。
