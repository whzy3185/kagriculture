# Kaggriculture 提交时机策略（2026-09-22）

## 结论

**不建议压到最后几分钟提交。** 对这种持续撮合的 agent competition，强候选应尽早提交以获得更多对局、暴露失败模式并降低 rating 不确定性；最终只需在截止前把“最新两版”锁定为最可信且互补的两个 agent。

官方 Evaluation 明确说明：

- 每队每天最多提交 5 个 agent；
- 只有最新 2 个 submission 被持续追踪，并用于最终评估；
- 每个 agent 持续参加对局，但新 agent 会更高频获得对局；
- 胜负和平局决定 rating，资金差不影响 rating 变化；
- 截止后约两周仍继续运行对局，最后用 Bradley–Terry tournament 生成最终榜单。

官方 Timeline 给出的最终提交截止为 2026-09-30 23:59 UTC，即北京时间 2026-10-01 07:59；随后约运行至 10 月 15 日以收敛。

来源：

- https://www.kaggle.com/competitions/kaggriculture/overview/evaluation
- https://www.kaggle.com/competitions/kaggriculture/overview/timeline

## 推荐节奏

1. 现在到 9 月 27–28 日：只提交通过新世界盲测的结构性版本，让每版积累至少 50–100 场并下载回放复盘。
2. 最后 48 小时：停止小参数噪声提交，确认最新两版分别覆盖主要元策略，而不是两个几乎相同的阈值变体。
3. 最终锁定：建议至少在截止前 6–12 小时完成，最好提前 12–24 小时，留出 validation 失败、打包错误或网络故障的恢复时间。
4. 不为了用满每天 5 次而提交；每次新提交都会改变“最新两版”集合，低质量试验可能把已验证 agent 挤出最终活跃席位。

## 当前状态

- EXP015 submission：`56460311`
- validation episode：`111966853`，已完成
- 初始 public score：600.0；这是新 agent 的默认初始化 rating，不代表实战强度
- 当前最新两版：EXP014 + EXP015
- 2026-09-22 已使用 1/5 次提交额度

当前组合适合作为观察起点：EXP015 负责新元策略，EXP014 保留为旧基线和回滚。下一次提交必须明显补足 OrderBook/shiiin 型尾部风险，才值得把 EXP014 挤出最新两版。
