# Other Skills

这里记录值得保留的第三方 Skill，方便更换开发环境后快速恢复。

安装命令默认使用全局安装（`-g`），并跳过交互确认（`-y`）。执行前可先打开来源仓库检查最新内容。

## 已记录

| Skill | 用途 | 来源 | 安装命令 |
| --- | --- | --- | --- |
| `show-me` | 用简洁图示、伪代码或 HTML 帮助解释复杂内容 | [humanlayer/skills](https://github.com/humanlayer/skills) | `npx skills add humanlayer/skills --skill show-me -g -y` |
| `huashu-design` | 用 HTML 制作高保真原型、幻灯片、动画、可视化并进行设计评审 | [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design) | `npx skills add alchaincyf/huashu-design --skill huashu-design -g -y` |
| `teach` | 在工作区内以持续、分阶段的方式学习新概念 | [mattpocock/skills](https://github.com/mattpocock/skills) | `npx skills add mattpocock/skills --skill teach -g -y` |
| `vercel-react-best-practices` | React 和 Next.js 性能优化与代码审查 | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -g -y` |
| `typescript-advanced-types` | TypeScript 高级类型设计 | [wshobson/agents](https://github.com/wshobson/agents) | `npx skills add wshobson/agents --skill typescript-advanced-types -g -y` |
| `tailored-resume-generator` | 根据职位描述生成针对性简历 | [composiohq/awesome-claude-skills](https://github.com/composiohq/awesome-claude-skills) | `npx skills add composiohq/awesome-claude-skills --skill tailored-resume-generator -g -y` |

## 记录模板

新增条目时至少保留 Skill 名称、用途、来源仓库和可直接执行的安装命令：

```markdown
| `skill-name` | 一句话说明适用场景 | [owner/repo](https://github.com/owner/repo) | `npx skills add owner/repo --skill skill-name -g -y` |
```

安装后可运行 `npx skills list -g` 检查全局 Skill。
