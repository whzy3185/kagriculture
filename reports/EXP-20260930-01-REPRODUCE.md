# 复现说明

本包中的候选已经被本轮开发评测拒绝。首先阅读 `reports/EXP-20260930-01-REJECTED.md`。

## 环境

验证机器使用 Python 3.12.14、kaggle-environments 1.32.7。这里只需要 Kaggriculture 通用 runner；不使用 API key、Kaggle 登录、GPU 或付费计算。原始环境源码位于 `data/reference/master/`，没有修改其商店 RNG。

常规安装可使用完整官方包：

```sh
python3 -m venv .venv
.venv/bin/pip install kaggle-environments==1.32.7 pytest
```

本次为避免安装无关环境的大型依赖，使用了官方 wheel 的 `--no-deps` 安装，并安装通用核心所需模块。所用最小核心路径已通过本包测试；其他游戏环境的可选依赖不在本轮验收范围内。完整依赖版本清单见 `reports/diagnostic_python_versions.json`。

## 准备与检查

```sh
python3 scripts/materialize_benchmark_baselines.py
python3 scripts/build_exp20260930_expected_demand.py
.venv/bin/python -m pytest tests/test_expected_demand_candidate.py tests/test_diagnostic_summary.py -q
```

045/054 原始 tar.gz 与 manifest 原样保留。物化脚本仅在校验 archive/source hash、唯一根成员 `main.py` 且非链接后写入，不会覆盖不一致的文件。V38 V2 的完整公开许可注释随 `external/ahmed_v38_v2/main.py` 保留。

## 完整对战复现

每次必须使用新的输出文件名。脚本禁止恢复旧输出，以免混入不同源码版本的结果。

```sh
.venv/bin/python scripts/diagnose_frozen_agents.py \
  agents/candidates/exp20260930_expected_demand/main.py \
  benchmark_packages/EXP-054-highquote-150/main.py \
  --seeds "$(seq -s, 260930201 260930224)" --workers 4 \
  --output reports/reproduced_candidate_vs054.json

.venv/bin/python scripts/diagnose_frozen_agents.py \
  agents/candidates/exp20260930_expected_demand/main.py \
  external/ahmed_v38_v2/main.py \
  --seeds "$(seq -s, 260930201 260930224)" --workers 4 \
  --output reports/reproduced_candidate_vsV38.json

.venv/bin/python scripts/diagnose_frozen_agents.py \
  benchmark_packages/EXP-054-highquote-150/main.py \
  external/ahmed_v38_v2/main.py \
  --seeds "$(seq -s, 260930201 260930224)" --workers 4 \
  --output reports/reproduced_parent_vsV38.json
```

原始 144 局使用的脚本精确快照保存在 `reports/evidence/diagnose_frozen_agents_v1.py.txt`。现行脚本仅增加记录 `_CS_REPORT`；候选源码未变。附加 8 局归因复测与原测试的钱差一致，不重复计作独立证据。

## 主要证据文件

- `configs/exp20260930_expected_demand_frozen.json`：候选、24 开发种子与未使用的 96 保留种子
- `reports/exp20260930_expected_demand_decision.json`：配对差值、按种子重采样、升级决策
- `reports/exp20260930_expected_demand_vs054_dev24.json`：48 局直接对战
- `reports/exp20260930_expected_demand_vsV38_dev24.json` 与 `reports/exp054_vsV38_dev24_20260930.json`：相同对手、种子、座位的 96 局
- `reports/exp20260930_expected_demand_decision_audit.json`：HERD2/COWSWAP 分项审计
- `reports/diagnostic066_vs054_fresh6_20260930.json`：066 的 12 局零触发诊断
- `submissions/EXP-20260930-01-expected-demand-REJECTED.tar.gz`：仅用于复核的候选归档
- `SHA256SUMS.json`：本交付包逐文件校验值
