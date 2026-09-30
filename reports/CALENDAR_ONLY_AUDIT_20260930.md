# EXP045 / EXP054 日历模型纠正实验

## 结论

**MODEL_CORRECTION_ONLY_NO_BEHAVIORAL_GAIN。** 已验证未来第七家商店的日期应为第 21 天，原模型写为第 22 天。修正后，24 个新种子、双座位、两份冻结基线共 96 局中，番茄投资资格没有一次变化，同座位动作轨迹全部相同。因此保留为已验证的模型纠正与实验记录，不能称为胜率提升，也不升级正式包。

## 唯一改动及来源

- 基础提交：`a1d81080538d33f9cbd0646eb8dd845f360e353b`
- 两份源文件的 `_cxtb_expected_revenue` 第 6749 行：`pending = {22: 0.25, 24: 0.25}` 改为 `{21: 0.25, 24: 0.25}`；同步更正一处注释
- 官方固定引擎 `_end_of_day` 在 `next_day % 3 == 0` 且商店数小于 8 时开店，因此第 18 天为 6 家、第 21 天为 7 家、第 24 天为 8 家
- 实际资格入口：第 1422 行在 `step == 432` 调用 `_v219_qualifies`，后者使用这一收入模型
- 没有改动需求概率 0.25、收入门槛 9000、资金门槛、生产路线、报价/订单层、`_HD2_FUTURE=0.0` 或其他策略参数

这不是针对某个失败种子调整现金阈值，也没有使用真实未来商店信息。原模型仍然以平均未来需求估值，其风险和其他近似项未在本轮修正。

## 冻结身份

| 对象 | SHA-256 |
|---|---|
| EXP045 基线 | `6744b67f9491a65404b70b200bd61a0fd588de513db4f11b119ca0213493686b` |
| EXP045 日历候选 | `26055dd62aa231af41552b62d6776e8441d85736a9d9a3cc7734fcbd3818b50b` |
| EXP054 基线 | `3d0002923d42add183e88f912c52b5015639e4386c9a78d7eb3dba91310c33f7` |
| EXP054 日历候选 | `2f374edf443ba58fd5e1e7ad5b9375890984f1cd9cd9bfc3a8f1e040ed1468e1` |
| 官方引擎源 | `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e` |

环境包为 `kaggle-environments==1.32.7`。机器可读身份、精确 diff、runner 与 specification 哈希都已记录。

## 预先确定的评测方法

见 `configs/calendar_protocol_20260930.json`，在第一局运行之前冻结。

- 种子 `260930501`–`260930524`，未出现在当时可见的既有报告种子列表
- 各候选仅对自己的原始基线测试，每种子两个座位，每个候选 48 局，共 96 局
- 官方真实状态机和未修改的商店 RNG；对手实时响应，不使用冻结动作带
- 隐藏 seed 不进入 agent 输入
- 所有对局须为 `DONE/DONE`、双方 719 次回调、720 个记录状态、最后状态 step 719
- 主指标为配对世界的胜平负积分、真实投资资格变化；钱差和运行时间为辅助
- 若没有资格翻转且相同物理座位的动作轨迹一致，记录无行为证据，不把全局得分噪声当提升，也不消耗额外推广留出集

## 合约测试

`tests/test_calendar_contract.py`：4 项通过，完整命令结果在 `calendar_contract_results.json`。

1. 候选字节只能等于冻结源的一个日期字面量和注释替换；HD2 和收入阈值保持不变
2. 官方解释器真实完整 PASS 对局检查第 18、21、24 天的商店数量
3. 不同市场库存、商店和对手番茄种植日下，估值等于独立逐日参考计算，且不修改输入
4. 合成边界验证日期确实可以改变资格，同时保留资金、种子和目标土地限制

合成例子：六家 BAKERY、对手无番茄时，库存 9700 的估值为 8983→9086，库存 9701 为 8925→9028。此处临时隔离了原生路线门控，仅是单元合约，**不是实际比赛样本或泛化收益**。

## 官方完整对局结果

| 候选 | 有效局数 | 胜-平-负 | 配对积分 | 配对平均钱差 | 投资资格翻转 | 同座位轨迹一致 |
|---|---:|---:|---:|---:|---:|---:|
| Calendar045 vs EXP045 | 48 | 4-40-4 | 0.500 | 0 | 0/48 | 48/48 |
| Calendar054 vs EXP054 | 48 | 4-40-4 | 0.500 | 0 | 0/48 | 48/48 |

- 两组所有局均满足完整状态检查，无运行错误
- 修正后估值增加 15–195，但原估值距离 9000 门槛最近仍有 767，故没有资格翻转
- 每个种子交换候选/基线座位后，对同一物理座位比较完整 719 步动作 SHA；全部相同，最终商店也相同
- 4 胜和 4 负来自已有的座位/农场差异，而不是修改产生的收益。不能把结果写成“48 局全平”，也不能只挑胜局报告

完整结果：

- `calendar_045_vs045_fresh24.json`
- `calendar_054_vs054_fresh24.json`
- `calendar_decision_20260930.json`：逐种子、逐座位的轨迹校验、收入变化和资格比较

## 边界与下一步

本轮证明了日历语义和实现正确性，并确认这批样本没有行为改变。它没有证明对其他对手或临界需求世界更强。按照预先确定的无触发规则，本轮没有运行额外 V38 或推广留出测试，没有改参数寻找“更好看的”结果。已有的平均需求、2.4 日消耗修正、对手补种假设和 9000 阈值均保留。

正式基线保持原 EXP045 / EXP054。后续若其他独立样本出现资格翻转，应作为新实验比较响应式异构对手，并使用此前未参与筛选的种子验证。

## 复现

在含原始 `submissions/` 包与当前引擎的仓库中，先安装环境包 1.32.7 和 pytest，然后运行：

```bash
python scripts/build_calendar_candidates.py
python -m pytest -q tests/test_calendar_contract.py
SEEDS=$(python -c 'import json;print(",".join(map(str,json.load(open("configs/calendar_protocol_20260930.json"))["development_seeds"])))')
python scripts/evaluate_calendar_agents.py agents/candidates/exp20260930_calendar_045/main.py benchmark_packages/EXP-045-masterv4-step1002/main.py --seeds "$SEEDS" --workers 2 --output reports/calendar_045_vs045_fresh24.json
python scripts/evaluate_calendar_agents.py agents/candidates/exp20260930_calendar_054/main.py benchmark_packages/EXP-054-highquote-150/main.py --seeds "$SEEDS" --workers 2 --output reports/calendar_054_vs054_fresh24.json
python scripts/summarize_calendar_results.py
```

评测器拒绝覆盖已有结果；复跑时使用干净输出目录或另一个结果文件名。builder 会验证原包 SHA，只在本地还没有冻结解包文件时物化它。各命令不会进行 Kaggle 提交。
