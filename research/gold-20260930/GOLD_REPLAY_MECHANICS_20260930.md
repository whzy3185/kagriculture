# 2026-09-30 Kaggriculture 金牌头部完整回放：真实成交、生产及执行机制

## 摘要与边界

- 本文分析4场新官方完整回放、8个座位，不是胜率评估。只能证明这些局中的行为/账目，不能证明策略普遍更优，也不能从行为推定源码、算法或某个新submission仍使用作者曾公开的方法。
- 4局均720个记录帧、双方DONE；帧0初态，帧1–719对应719次真正执行。最后一次输入obs718，结果帧719是day29/hour23，**不执行最后一天hour23行动及随后的日终自动卸货**。
- 连续重放从初态保留字典插入顺序；逐单位市场提交时才记录成交。4×719=2,876次转换，双方farms/private/market/town/day/hour全部逐帧相等，最终现金账8/8吻合。未声称运行时余量remainingOverageTime也可模拟。
- 重放直接使用仓库固定版官方解释器的副本；不是重新调用参赛agent，不涉及对手对改变后的策略反应。原用户仓库未修改，所有分析留在本独立目录。
- “差额分解”是会计恒等式，不是独立策略改动的因果贡献；溢出损耗与惜败同时存在，不等于修掉损耗必能翻胜。

## 一页主要发现

1. 榜首M & M & P & Q以106,701胜DECEM104,285（+2,416）。二者开局极相近，买地均在结果帧149/199/250；双方均有8牛3羊、12瓜，最终差距由多品类产量、售价与人工/采购成本累积。销售总额多1,879，采购少328、人工少209。不能归结为换一种开局。
2. 这局同量瓜的出售时间有直接证据：M&M在结果帧389把6瓜DROP入仓并同回合卖833；DECEM的6瓜此时仍在(7,4)，帧391才DROP并卖754。整局双方都卖72瓜，收入14,681/14,293。该79元局部差是实际成交比较，不是完整反事实收益。
3. CDE137,711对Unknown Mother-Goose137,700仅胜11。主生产组合近镜像，收入多147、采购少186、人工多322，净11。输方确有日终丢2草莓+1肥、另一次丢2麦；但必须先证明EXP054在独立样本中也触发，再讨论修补，而不能用此局直接证明054缺少guard。
4. 同active Happy Farm在双PIZZA开局局扩至22番茄，胜yuto0833,713：番茄173个/18,090对57个/4,910，收入差13,180，抵消其他品类劣势。首批番茄出现在day11左右，领先对手的day18建仓；迟到的第15天第三家PIZZA又增强已建生产的需求。
5. 同active Happy Farm另一局并未固守22番茄：前两店FARMERS_MARKET+PIZZA，之后第9/15/18天先后解锁YARN_STORE，转向最多16羊、10番茄；Random Mambo扩到21羊、14番茄，获胜14,901。羊毛卖351个/75,395对281个/60,870，单项收入差14,525；赢家另有更多萝卜/番茄、较少人工。Happy Farm丢72单位货，对手无日终溢出。适应方向相同仍可在规模、部署时间、照料、物流上输。

## 已验证的规则与容易误读处

- 先执行农夫/工人动作，再市场逐订单槽结算，再城镇消费/作物衰败，普通日最后才刷新生长、产出、自动卸货。故当回合DROP可当回合SELL；日终自动卸货所得不能倒回当回合SELL。
- 同一订单槽按单位锁步：双方先按同一库存报价，再提交各自一单位；不是某个座位永远有先手。同一商品放在更早订单槽，仍能先于对方较后订单整批交易。
- SELL只从仓库卖，不能卖工人背包；交易请求可超过仓内实际数量。本文只统计_commit_unit成功的成交。
- DROP和日终卸货容量100，溢出直接丢弃。逐人、逐物品插入顺序会决定被丢品类；从每帧排序后的JSON独立重建会在拥堵处误判品类。因此本工具从初态连续重放，并以实际private全字段验证。
- CARE必须与当日FEED配合才积累下一次产出的照料奖励；产出日只有FEED才兑现已有奖励。FERTILIZE与浇水共同作用；重复动作/非法动作静默无效，不能用请求数冒充有效护理/产出。
- 雇佣是每日重置的斐波那契边际成本；10/11/12/13名工人当日总成本143/232/376/609。为多一名工人所付的成本明显非线性。
- 城镇商店每4步消费，同类型可重复；羊毛专卖店每次消费2，而多商品店每商品消费1；第24天最后一家店后不再新增。生产路由应看实例计数而非去重后的店名。

## EXP045 / EXP054的真实能力与可验证缺口（静态源证据）

核验的是EXP-045-masterv4-step1002与EXP-054-highquote-150打包main.py；不是Ahmed的同号V45/V54。各包SHA见末尾。

- 054继承045的Step1002边界；其新增部分只是最多5轮订单重排闭包，要求所有前移SELL的当前公开单价≥150，且不允许新增“低报价SELL跨到高报价SELL前”的逆序。它保持生产动作、订单集合/数量，不能靠改150阈值创造新的生产路线。
- 但共同基线**绝非没有自适应的固定动作带**：内含41条719行动路线、64种有序前两店映射。_router在obs step>=144首次选主线；前两店含YARN走羊毛特化分支及少量对手早期现金/市场库存指纹；>=648切route2。四个样本店对中双PIZZA→123，其余ICE_CREAM+BAKERY、ICE_CREAM+FARMERS、FARMERS+PIZZA均→105（仅底层初始路线映射，不代表全部后续行动相同）。
- 另已有HERD/HERD2、shop-aware herd、CARROT、RACE/COURIER、抢售、仓容与终局救援等层。HERD在step>=216首次碰到GOOSE购买时决定物种；HERD2在step192–359、首次鹅购买且尚无COOP等门控下比较GOOSE/COW/SHEEP预期收益。shop-aware herd在day8–11按实际店把特定小批动物购买替换；CARROT有价格比、日区间与饲料保留门控。它们利用公开市场、双方可见动物及原路线计划，但候选动作多是既有购买/播种/服务时点的替换，并非任意时刻重建所有作物/工人布局。
- 现存仓容措施：早期day-end guard在hour23；OVERFLOW模拟田间动作与市场后，要求额外出售能保持次日仓内向量不变，且订单槽/预算门控通过；SHEDROOM在hours21/22/23、step<717预估仓+背包，留8单位余量，并为未来饲料/肥保留资源；pre-guard在hours21/22且step<696提前处理指定高价值品类。底层Chassis.room_guard虽配置False，外层这些措施仍存在，因此不能仅看到那个False就宣布没有guard。
- 终局已有712–718七步physical planner及obs718显式DROP/SELL。日终自动卸货不在最后执行窗口内，代码已有认识；本次没有发现新的“054少一天结算”漏洞。

下一轮建议顺序（尚未执行）：
1. 先对054的独立新局做透明库存损耗审计：每步按成功动作/成交平衡“收获+购买−喂养−施肥−出售−最终库存”，定位真实损耗、早卖机会、guard是否触发/被后层改写/受槽位限制。若并无独立触发，不新增通用guard。
2. 在后续商店解锁（day9/12/15/18）时记录当前route、真实双方布局、现价与按已有商店计算的消费，检查既有HERD/route候选是否能及时到达需求所需规模。Happy Farm22番茄和Random Mambo21羊只作为候选能力测试，不直接照抄固定面积。
3. 对物流比较“多收一次”与“提前回仓同回合卖”的机会成本，覆盖瓜/草莓/羊毛等；计入公开市场库存变化、对手可见布局/待收产品/位置、价格曲线、交易槽及本方后续产量；运行时不读取对手private背包或未来动作，不只用单价150或一个现金门槛。
4. 只有明确改变了动作且在未参与筛选的种子、双座位、会反应的对手上稳定改善，才考虑升级。固定官方动作带重放只验证机制/局部反事实，不支持泛化胜率结论。


## 回放 115649229: DECEM vs M & M & P & Q

[官方源](https://www.kaggle.com/competitions/kaggriculture/leaderboard?submissionId=56679033&episodeId=115649229)；seed=177327100；720帧，双方DONE；719次连续状态转移全字段相等。

### 实际成交：数量 / 销售收入 / 加权成交均价

|商品|DECEM|M & M & P & Q|座位1减座位0收入|
|---|---:|---:|---:|
|WHEAT|726 / 21,526 / 29.65|610 / 18,071 / 29.62|-3,455|
|CARROT|73 / 2,988 / 40.93|102 / 4,185 / 41.03|+1,197|
|TOMATO|136 / 7,984 / 58.71|145 / 8,330 / 57.45|+346|
|STRAWBERRY|265 / 38,216 / 144.21|270 / 39,468 / 146.18|+1,252|
|MELON|72 / 14,293 / 198.51|72 / 14,681 / 203.90|+388|
|EGG|356 / 15,440 / 43.37|378 / 16,284 / 43.08|+844|
|MILK|181 / 14,994 / 82.84|184 / 15,750 / 85.60|+756|
|WOOL|65 / 9,139 / 140.60|70 / 9,620 / 137.43|+481|
|FERTILIZER|244 / 12,492 / 51.20|243 / 12,562 / 51.70|+70|

### 现金闭合

|项目|座位0|座位1|
|---|---:|---:|
|opening_cash|3,000|3,000|
|sales|137,072|138,951|
|purchases|20,887|20,559|
|hires|7,900|7,691|
|land|7,000|7,000|
|computed_final|104,285|106,701|

### 成功生产服务 / 峰值布局 / 扩地

- DECEM：FEED 373；CARE 346；FERTILIZE 261；COLLECT_FERTILIZER 505；HARVEST 599；DROP 111；日终丢弃 {}。峰值 {'COW': {'max_tiles': 8, 'first_frame': 156}, 'SHEEP': {'max_tiles': 3, 'first_frame': 8}, 'MELON': {'max_tiles': 12, 'first_frame': 211}, 'WHEAT': {'max_tiles': 43, 'first_frame': 285}, 'STRAWBERRY': {'max_tiles': 35, 'first_frame': 378}, 'GOOSE': {'max_tiles': 11, 'first_frame': 258}, 'TOMATO': {'max_tiles': 19, 'first_frame': 473}, 'CARROT': {'max_tiles': 15, 'first_frame': 550}}；买地结果帧 [149, 199, 250]。
- M & M & P & Q：FEED 391；CARE 355；FERTILIZE 267；COLLECT_FERTILIZER 510；HARVEST 594；DROP 115；日终丢弃 {}。峰值 {'COW': {'max_tiles': 8, 'first_frame': 161}, 'SHEEP': {'max_tiles': 3, 'first_frame': 8}, 'MELON': {'max_tiles': 12, 'first_frame': 165}, 'WHEAT': {'max_tiles': 44, 'first_frame': 305}, 'STRAWBERRY': {'max_tiles': 36, 'first_frame': 394}, 'GOOSE': {'max_tiles': 12, 'first_frame': 263}, 'TOMATO': {'max_tiles': 19, 'first_frame': 468}, 'CARROT': {'max_tiles': 12, 'first_frame': 520}}；买地结果帧 [149, 199, 250]。

### 阶段布局（frame为执行后记录索引，day按游戏0起算）

|frame/day|座位0现金 / 布局|座位1现金 / 布局|
|---|---|---|
|24/1|4 / WHEAT:12, MELON:6, COW:2, SHEEP:3|14 / WHEAT:11, MELON:6, COW:2, SHEEP:3|
|144/6|10 / STRAWBERRY:6, COW:6, MELON:10, SHEEP:3|64 / STRAWBERRY:5, COW:7, MELON:10, SHEEP:3|
|216/9|246 / STRAWBERRY:23, COW:8, MELON:12, WHEAT:13, GOOSE:6, SHEEP:3, TOMATO:3|416 / STRAWBERRY:25, COW:8, MELON:12, SHEEP:3, GOOSE:4, WHEAT:14, TOMATO:2|
|360/15|22,237 / STRAWBERRY:29, COW:8, TOMATO:8, WHEAT:39, GOOSE:11, SHEEP:3, MELON:2|22,565 / STRAWBERRY:30, COW:8, WHEAT:40, SHEEP:3, GOOSE:12, MELON:2, TOMATO:5|
|432/18|39,655 / STRAWBERRY:35, COW:8, TOMATO:14, WHEAT:28, GOOSE:11, SHEEP:3, MELON:1|39,563 / STRAWBERRY:36, COW:8, TOMATO:13, WHEAT:27, SHEEP:3, GOOSE:12|
|480/20|51,187 / STRAWBERRY:31, TOMATO:17, WHEAT:27, COW:8, GOOSE:11, SHEEP:3, CARROT:1|51,694 / TOMATO:18, WHEAT:19, COW:8, STRAWBERRY:32, SHEEP:3, GOOSE:12, CARROT:5|
|576/24|67,575 / CARROT:13, TOMATO:13, WHEAT:33, COW:8, STRAWBERRY:12, GOOSE:11, SHEEP:3|68,322 / WHEAT:29, TOMATO:15, COW:8, SHEEP:3, GOOSE:12, CARROT:8, STRAWBERRY:11|
|624/26|75,911 / WHEAT:41, TOMATO:12, COW:8, STRAWBERRY:12, GOOSE:11, SHEEP:3, CARROT:2|77,439 / WHEAT:34, TOMATO:14, COW:8, SHEEP:3, GOOSE:12, CARROT:6, STRAWBERRY:11|
|719/29|104,285 / CARROT:2, TOMATO:5, WHEAT:2, STRAWBERRY:8, COW:5, GOOSE:10|106,701 / TOMATO:6, COW:6, GOOSE:12, STRAWBERRY:9|

商店解锁顺序：ICE_CREAM_SHOP, BAKERY, BAKERY, FARMERS_MARKET, ICE_CREAM_SHOP, FARMERS_MARKET, BRUNCH_SPOT, YARN_STORE

实际采购明细（quantity/value）：[{"BUY_ANIMAL:COW": {"n": 8, "value": 3200}, "BUY_PRODUCT:WHEAT": {"n": 133, "value": 4887}, "BUY_ANIMAL:SHEEP": {"n": 3, "value": 1500}, "BUY_SEED:MELON": {"n": 12, "value": 960}, "BUY_SEED:WHEAT": {"n": 211, "value": 2110}, "BUY_SEED:STRAWBERRY": {"n": 35, "value": 3500}, "BUY_ANIMAL:GOOSE": {"n": 11, "value": 3300}, "BUY_SEED:TOMATO": {"n": 19, "value": 950}, "BUY_SEED:CARROT": {"n": 24, "value": 480}}, {"BUY_ANIMAL:COW": {"n": 8, "value": 3200}, "BUY_PRODUCT:WHEAT": {"n": 123, "value": 4259}, "BUY_ANIMAL:SHEEP": {"n": 3, "value": 1500}, "BUY_SEED:MELON": {"n": 12, "value": 960}, "BUY_SEED:WHEAT": {"n": 185, "value": 1850}, "BUY_SEED:STRAWBERRY": {"n": 36, "value": 3600}, "BUY_ANIMAL:GOOSE": {"n": 12, "value": 3600}, "BUY_SEED:TOMATO": {"n": 19, "value": 950}, "BUY_SEED:CARROT": {"n": 32, "value": 640}}]

## 回放 115650653: Unknown Mother-Goose vs CDE

[官方源](https://www.kaggle.com/competitions/kaggriculture/leaderboard?submissionId=56689315&episodeId=115650653)；seed=43187779；720帧，双方DONE；719次连续状态转移全字段相等。

### 实际成交：数量 / 销售收入 / 加权成交均价

|商品|Unknown Mother-Goose|CDE|座位1减座位0收入|
|---|---:|---:|---:|
|WHEAT|353 / 15,259 / 43.23|353 / 15,291 / 43.32|+32|
|CARROT|70 / 4,500 / 64.29|88 / 5,617 / 63.83|+1,117|
|TOMATO|79 / 14,440 / 182.78|74 / 13,429 / 181.47|-1,011|
|STRAWBERRY|345 / 67,829 / 196.61|342 / 67,410 / 197.11|-419|
|MELON|66 / 13,848 / 209.82|66 / 14,024 / 212.48|+176|
|EGG|257 / 10,653 / 41.45|254 / 10,522 / 41.43|-131|
|MILK|171 / 14,990 / 87.66|172 / 15,021 / 87.33|+31|
|WOOL|80 / 8,180 / 102.25|77 / 8,371 / 108.71|+191|
|FERTILIZER|206 / 12,068 / 58.58|206 / 12,229 / 59.36|+161|

### 现金闭合

|项目|座位0|座位1|
|---|---:|---:|
|opening_cash|3,000|3,000|
|sales|161,767|161,914|
|purchases|20,139|19,953|
|hires|3,928|4,250|
|land|3,000|3,000|
|computed_final|137,700|137,711|

### 成功生产服务 / 峰值布局 / 扩地

- Unknown Mother-Goose：FEED 321；CARE 321；FERTILIZE 210；COLLECT_FERTILIZER 417；HARVEST 526；DROP 133；日终丢弃 {'FERTILIZER': 1, 'STRAWBERRY': 2, 'WHEAT': 2}。峰值 {'COW': {'max_tiles': 8, 'first_frame': 153}, 'SHEEP': {'max_tiles': 3, 'first_frame': 9}, 'MELON': {'max_tiles': 11, 'first_frame': 159}, 'WHEAT': {'max_tiles': 29, 'first_frame': 570}, 'STRAWBERRY': {'max_tiles': 45, 'first_frame': 428}, 'GOOSE': {'max_tiles': 7, 'first_frame': 230}, 'TOMATO': {'max_tiles': 10, 'first_frame': 426}, 'CARROT': {'max_tiles': 19, 'first_frame': 660}}；买地结果帧 [148, 199]。
- CDE：FEED 315；CARE 318；FERTILIZE 209；COLLECT_FERTILIZER 415；HARVEST 528；DROP 140；日终丢弃 {}。峰值 {'COW': {'max_tiles': 8, 'first_frame': 153}, 'SHEEP': {'max_tiles': 3, 'first_frame': 9}, 'MELON': {'max_tiles': 11, 'first_frame': 159}, 'WHEAT': {'max_tiles': 30, 'first_frame': 589}, 'STRAWBERRY': {'max_tiles': 44, 'first_frame': 377}, 'GOOSE': {'max_tiles': 7, 'first_frame': 231}, 'TOMATO': {'max_tiles': 10, 'first_frame': 428}, 'CARROT': {'max_tiles': 22, 'first_frame': 643}}；买地结果帧 [148, 199]。

### 阶段布局（frame为执行后记录索引，day按游戏0起算）

|frame/day|座位0现金 / 布局|座位1现金 / 布局|
|---|---|---|
|24/1|9 / WHEAT:12, MELON:6, COW:2, SHEEP:3|9 / WHEAT:12, MELON:6, COW:2, SHEEP:3|
|144/6|162 / STRAWBERRY:7, COW:7, MELON:8, SHEEP:3|152 / STRAWBERRY:7, COW:7, MELON:8, SHEEP:3|
|216/9|8 / STRAWBERRY:29, COW:8, MELON:11, GOOSE:5, SHEEP:3, WHEAT:12|81 / STRAWBERRY:30, COW:8, MELON:11, GOOSE:5, SHEEP:3, WHEAT:9|
|360/15|23,848 / STRAWBERRY:41, COW:8, WHEAT:13, GOOSE:7, SHEEP:3, MELON:3|24,164 / STRAWBERRY:40, COW:8, WHEAT:14, GOOSE:7, SHEEP:3, MELON:3|
|432/18|43,384 / STRAWBERRY:45, COW:8, TOMATO:10, WHEAT:2, GOOSE:7, SHEEP:3|44,869 / STRAWBERRY:44, COW:8, TOMATO:10, WHEAT:3, GOOSE:7, SHEEP:3|
|480/20|60,909 / STRAWBERRY:39, WHEAT:8, COW:8, TOMATO:10, GOOSE:7, SHEEP:3|60,589 / STRAWBERRY:38, WHEAT:9, COW:8, TOMATO:10, GOOSE:7, SHEEP:3|
|576/24|84,170 / WHEAT:28, COW:7, TOMATO:10, GOOSE:7, STRAWBERRY:19, SHEEP:3, CARROT:1|83,776 / WHEAT:29, COW:7, CARROT:1, TOMATO:10, GOOSE:7, STRAWBERRY:18, SHEEP:3|
|624/26|97,227 / CARROT:14, WHEAT:24, TOMATO:10, COW:4, GOOSE:7, STRAWBERRY:11, SHEEP:3|99,315 / WHEAT:25, CARROT:12, TOMATO:10, COW:4, GOOSE:7, STRAWBERRY:12, SHEEP:3|
|719/29|137,700 / COW:4, GOOSE:7, STRAWBERRY:7|137,711 / COW:4, GOOSE:7, STRAWBERRY:9|

商店解锁顺序：ICE_CREAM_SHOP, FARMERS_MARKET, FARMERS_MARKET, FARMERS_MARKET, SMOOTHIE_SHOP, FARMERS_MARKET, BAKERY, YARN_STORE

实际采购明细（quantity/value）：[{"BUY_ANIMAL:COW": {"n": 8, "value": 3200}, "BUY_PRODUCT:WHEAT": {"n": 155, "value": 5809}, "BUY_ANIMAL:SHEEP": {"n": 3, "value": 1500}, "BUY_SEED:MELON": {"n": 11, "value": 880}, "BUY_SEED:WHEAT": {"n": 117, "value": 1170}, "BUY_SEED:STRAWBERRY": {"n": 45, "value": 4500}, "BUY_ANIMAL:GOOSE": {"n": 7, "value": 2100}, "BUY_SEED:TOMATO": {"n": 10, "value": 500}, "BUY_SEED:CARROT": {"n": 24, "value": 480}}, {"BUY_ANIMAL:COW": {"n": 8, "value": 3200}, "BUY_PRODUCT:WHEAT": {"n": 152, "value": 5613}, "BUY_ANIMAL:SHEEP": {"n": 3, "value": 1500}, "BUY_SEED:MELON": {"n": 11, "value": 880}, "BUY_SEED:WHEAT": {"n": 116, "value": 1160}, "BUY_SEED:STRAWBERRY": {"n": 44, "value": 4400}, "BUY_ANIMAL:GOOSE": {"n": 7, "value": 2100}, "BUY_SEED:TOMATO": {"n": 10, "value": 500}, "BUY_SEED:CARROT": {"n": 30, "value": 600}}]

## 回放 115653683: yuto083 vs Happy Farm

[官方源](https://www.kaggle.com/competitions/kaggriculture/leaderboard?submissionId=56689469&episodeId=115653683)；seed=398463326；720帧，双方DONE；719次连续状态转移全字段相等。

### 实际成交：数量 / 销售收入 / 加权成交均价

|商品|yuto083|Happy Farm|座位1减座位0收入|
|---|---:|---:|---:|
|WHEAT|604 / 19,240 / 31.85|426 / 13,577 / 31.87|-5,663|
|CARROT|145 / 5,371 / 37.04|51 / 1,756 / 34.43|-3,615|
|TOMATO|57 / 4,910 / 86.14|173 / 18,090 / 104.57|+13,180|
|STRAWBERRY|145 / 10,286 / 70.94|143 / 9,357 / 65.43|-929|
|MELON|72 / 14,534 / 201.86|72 / 14,620 / 203.06|+86|
|EGG|140 / 6,102 / 43.59|168 / 7,351 / 43.76|+1,249|
|MILK|264 / 26,002 / 98.49|266 / 26,727 / 100.48|+725|
|WOOL|173 / 20,676 / 119.51|176 / 18,414 / 104.62|-2,262|
|FERTILIZER|272 / 12,361 / 45.44|316 / 12,805 / 40.52|+444|

### 现金闭合

|项目|座位0|座位1|
|---|---:|---:|
|opening_cash|3,000|3,000|
|sales|119,482|122,697|
|purchases|20,636|19,871|
|hires|5,313|5,580|
|land|3,000|3,000|
|computed_final|93,533|97,246|

### 成功生产服务 / 峰值布局 / 扩地

- yuto083：FEED 400；CARE 408；FERTILIZE 233；COLLECT_FERTILIZER 505；HARVEST 531；DROP 133；日终丢弃 {}。峰值 {'COW': {'max_tiles': 12, 'first_frame': 163}, 'SHEEP': {'max_tiles': 8, 'first_frame': 254}, 'MELON': {'max_tiles': 12, 'first_frame': 162}, 'WHEAT': {'max_tiles': 36, 'first_frame': 287}, 'STRAWBERRY': {'max_tiles': 22, 'first_frame': 354}, 'GOOSE': {'max_tiles': 4, 'first_frame': 208}, 'CARROT': {'max_tiles': 17, 'first_frame': 547}, 'TOMATO': {'max_tiles': 8, 'first_frame': 452}}；买地结果帧 [148, 199]。
- Happy Farm：FEED 412；CARE 412；FERTILIZE 210；COLLECT_FERTILIZER 526；HARVEST 542；DROP 139；日终丢弃 {'CARROT': 3, 'WHEAT': 2}。峰值 {'COW': {'max_tiles': 11, 'first_frame': 181}, 'SHEEP': {'max_tiles': 8, 'first_frame': 297}, 'MELON': {'max_tiles': 12, 'first_frame': 161}, 'WHEAT': {'max_tiles': 34, 'first_frame': 261}, 'STRAWBERRY': {'max_tiles': 19, 'first_frame': 370}, 'GOOSE': {'max_tiles': 5, 'first_frame': 211}, 'TOMATO': {'max_tiles': 22, 'first_frame': 445}, 'CARROT': {'max_tiles': 10, 'first_frame': 663}}；买地结果帧 [148, 197]。

### 阶段布局（frame为执行后记录索引，day按游戏0起算）

|frame/day|座位0现金 / 布局|座位1现金 / 布局|
|---|---|---|
|24/1|9 / WHEAT:12, MELON:6, COW:2, SHEEP:3|9 / WHEAT:12, MELON:6, COW:2, SHEEP:3|
|144/6|153 / STRAWBERRY:7, COW:7, MELON:8, SHEEP:3|153 / STRAWBERRY:7, COW:7, MELON:8, SHEEP:3|
|216/9|155 / STRAWBERRY:12, COW:11, WHEAT:28, GOOSE:4, MELON:12, SHEEP:3|528 / STRAWBERRY:11, COW:11, WHEAT:28, MELON:12, GOOSE:5, SHEEP:3|
|360/15|31,368 / STRAWBERRY:22, COW:11, WHEAT:26, GOOSE:4, SHEEP:8, MELON:4|31,511 / STRAWBERRY:18, COW:11, WHEAT:16, TOMATO:12, GOOSE:5, SHEEP:8, MELON:4|
|432/18|52,517 / STRAWBERRY:21, COW:11, WHEAT:29, GOOSE:4, CARROT:2, SHEEP:8|51,617 / STRAWBERRY:19, COW:11, TOMATO:20, WHEAT:12, GOOSE:5, SHEEP:8|
|480/20|58,836 / STRAWBERRY:13, CARROT:8, WHEAT:23, COW:10, GOOSE:4, TOMATO:8, SHEEP:8|57,006 / STRAWBERRY:13, WHEAT:16, COW:11, TOMATO:22, GOOSE:5, SHEEP:8|
|576/24|68,666 / CARROT:15, WHEAT:19, COW:10, GOOSE:4, TOMATO:8, SHEEP:7, STRAWBERRY:10|67,558 / WHEAT:21, COW:11, TOMATO:20, GOOSE:5, CARROT:3, SHEEP:6, STRAWBERRY:9|
|624/26|74,007 / CARROT:9, WHEAT:27, COW:10, GOOSE:4, TOMATO:8, SHEEP:4, STRAWBERRY:10|76,762 / WHEAT:26, COW:11, TOMATO:10, CARROT:7, GOOSE:4, SHEEP:6, STRAWBERRY:9|
|719/29|93,533 / COW:9, GOOSE:4, TOMATO:8, WHEAT:2, STRAWBERRY:5|97,246 / COW:9, WHEAT:1, GOOSE:4, TOMATO:2, SHEEP:1, STRAWBERRY:3|

商店解锁顺序：PIZZA_SHOP, PIZZA_SHOP, YARN_STORE, BRUNCH_SPOT, PIZZA_SHOP, PET_CAFE, ICE_CREAM_SHOP, BRUNCH_SPOT

实际采购明细（quantity/value）：[{"BUY_ANIMAL:COW": {"n": 12, "value": 4800}, "BUY_PRODUCT:WHEAT": {"n": 124, "value": 4286}, "BUY_ANIMAL:SHEEP": {"n": 8, "value": 4000}, "BUY_SEED:MELON": {"n": 12, "value": 960}, "BUY_SEED:WHEAT": {"n": 195, "value": 1950}, "BUY_SEED:STRAWBERRY": {"n": 22, "value": 2200}, "BUY_ANIMAL:GOOSE": {"n": 4, "value": 1200}, "BUY_SEED:CARROT": {"n": 42, "value": 840}, "BUY_SEED:TOMATO": {"n": 8, "value": 400}}, {"BUY_ANIMAL:COW": {"n": 11, "value": 4400}, "BUY_PRODUCT:WHEAT": {"n": 114, "value": 3911}, "BUY_ANIMAL:SHEEP": {"n": 8, "value": 4000}, "BUY_SEED:MELON": {"n": 12, "value": 960}, "BUY_SEED:WHEAT": {"n": 164, "value": 1640}, "BUY_SEED:STRAWBERRY": {"n": 20, "value": 2000}, "BUY_ANIMAL:GOOSE": {"n": 5, "value": 1500}, "BUY_SEED:TOMATO": {"n": 22, "value": 1100}, "BUY_SEED:CARROT": {"n": 18, "value": 360}}]

## 回放 115648413: Happy Farm vs Random Mambo

[官方源](https://www.kaggle.com/competitions/kaggriculture/leaderboard?submissionId=56689469&episodeId=115648413)；seed=1421196692；720帧，双方DONE；719次连续状态转移全字段相等。

### 实际成交：数量 / 销售收入 / 加权成交均价

|商品|Happy Farm|Random Mambo|座位1减座位0收入|
|---|---:|---:|---:|
|WHEAT|332 / 11,136 / 33.54|293 / 10,264 / 35.03|-872|
|CARROT|80 / 4,541 / 56.76|190 / 10,451 / 55.01|+5,910|
|TOMATO|74 / 9,758 / 131.86|112 / 14,030 / 125.27|+4,272|
|STRAWBERRY|200 / 13,702 / 68.51|112 / 10,451 / 93.31|-3,251|
|MELON|72 / 14,693 / 204.07|78 / 15,067 / 193.17|+374|
|EGG|174 / 7,298 / 41.94|127 / 5,466 / 43.04|-1,832|
|MILK|142 / 14,062 / 99.03|128 / 11,843 / 92.52|-2,219|
|WOOL|281 / 60,870 / 216.62|351 / 75,395 / 214.80|+14,525|
|FERTILIZER|296 / 12,288 / 41.51|301 / 13,876 / 46.10|+1,588|

### 现金闭合

|项目|座位0|座位1|
|---|---:|---:|
|opening_cash|3,000|3,000|
|sales|148,348|166,843|
|purchases|21,930|26,731|
|hires|6,635|5,428|
|land|3,000|3,000|
|computed_final|119,783|134,684|

### 成功生产服务 / 峰值布局 / 扩地

- Happy Farm：FEED 450；CARE 450；FERTILIZE 215；COLLECT_FERTILIZER 514；HARVEST 501；DROP 140；日终丢弃 {'WHEAT': 38, 'EGG': 12, 'FERTILIZER': 3, 'STRAWBERRY': 4, 'MILK': 6, 'TOMATO': 5, 'WOOL': 4}。峰值 {'COW': {'max_tiles': 7, 'first_frame': 156}, 'SHEEP': {'max_tiles': 16, 'first_frame': 468}, 'MELON': {'max_tiles': 12, 'first_frame': 161}, 'WHEAT': {'max_tiles': 34, 'first_frame': 548}, 'STRAWBERRY': {'max_tiles': 26, 'first_frame': 322}, 'GOOSE': {'max_tiles': 5, 'first_frame': 208}, 'TOMATO': {'max_tiles': 10, 'first_frame': 422}, 'CARROT': {'max_tiles': 14, 'first_frame': 647}}；买地结果帧 [148, 199]。
- Random Mambo：FEED 457；CARE 396；FERTILIZE 227；COLLECT_FERTILIZER 433；HARVEST 475；DROP 104；日终丢弃 {}。峰值 {'COW': {'max_tiles': 7, 'first_frame': 156}, 'SHEEP': {'max_tiles': 21, 'first_frame': 454}, 'MELON': {'max_tiles': 12, 'first_frame': 161}, 'WHEAT': {'max_tiles': 31, 'first_frame': 263}, 'STRAWBERRY': {'max_tiles': 23, 'first_frame': 335}, 'GOOSE': {'max_tiles': 7, 'first_frame': 210}, 'CARROT': {'max_tiles': 30, 'first_frame': 643}, 'TOMATO': {'max_tiles': 14, 'first_frame': 455}}；买地结果帧 [148, 199]。

### 阶段布局（frame为执行后记录索引，day按游戏0起算）

|frame/day|座位0现金 / 布局|座位1现金 / 布局|
|---|---|---|
|24/1|2 / WHEAT:12, MELON:6, COW:2, SHEEP:3|6 / WHEAT:12, MELON:6, COW:2, SHEEP:3|
|144/6|568 / STRAWBERRY:9, COW:5, MELON:8, SHEEP:3|570 / STRAWBERRY:9, COW:5, MELON:8, SHEEP:3|
|216/9|214 / STRAWBERRY:23, COW:7, WHEAT:18, MELON:12, GOOSE:5, SHEEP:3|282 / STRAWBERRY:20, COW:7, WHEAT:19, MELON:12, GOOSE:7, SHEEP:3|
|360/15|25,279 / STRAWBERRY:26, COW:7, WHEAT:25, SHEEP:8, GOOSE:5, MELON:4|25,293 / STRAWBERRY:23, COW:7, WHEAT:27, GOOSE:6, MELON:5, SHEEP:7|
|432/18|43,467 / STRAWBERRY:26, COW:5, WHEAT:15, SHEEP:12, GOOSE:5, TOMATO:10|40,156 / TOMATO:10, STRAWBERRY:16, WHEAT:18, COW:6, GOOSE:6, SHEEP:15, MELON:1, CARROT:3|
|480/20|46,970 / STRAWBERRY:20, WHEAT:19, COW:5, SHEEP:16, GOOSE:5, TOMATO:10|43,571 / TOMATO:14, WHEAT:22, SHEEP:21, GOOSE:6, COW:4, MELON:1, CARROT:3, STRAWBERRY:3|
|576/24|67,357 / WHEAT:27, CARROT:8, SHEEP:16, COW:4, GOOSE:5, TOMATO:10, STRAWBERRY:3|64,791 / TOMATO:14, WHEAT:21, SHEEP:21, CARROT:7, GOOSE:5, COW:4, STRAWBERRY:2|
|624/26|84,845 / CARROT:12, WHEAT:22, SHEEP:15, COW:4, GOOSE:5, TOMATO:10, STRAWBERRY:3|91,398 / TOMATO:14, CARROT:27, SHEEP:21, GOOSE:3, COW:4, WHEAT:4, STRAWBERRY:2|
|719/29|119,783 / SHEEP:8, COW:4, GOOSE:5, STRAWBERRY:2|134,684 / CARROT:3, SHEEP:8, COW:4, TOMATO:4, STRAWBERRY:2|

商店解锁顺序：FARMERS_MARKET, PIZZA_SHOP, YARN_STORE, PET_CAFE, YARN_STORE, YARN_STORE, PIZZA_SHOP, FARMERS_MARKET

实际采购明细（quantity/value）：[{"BUY_ANIMAL:COW": {"n": 7, "value": 2800}, "BUY_PRODUCT:WHEAT": {"n": 102, "value": 3490}, "BUY_ANIMAL:SHEEP": {"n": 16, "value": 8000}, "BUY_SEED:MELON": {"n": 12, "value": 960}, "BUY_SEED:WHEAT": {"n": 160, "value": 1600}, "BUY_SEED:STRAWBERRY": {"n": 26, "value": 2600}, "BUY_ANIMAL:GOOSE": {"n": 5, "value": 1500}, "BUY_SEED:TOMATO": {"n": 10, "value": 500}, "BUY_SEED:CARROT": {"n": 24, "value": 480}}, {"BUY_ANIMAL:COW": {"n": 7, "value": 2800}, "BUY_ANIMAL:SHEEP": {"n": 21, "value": 10500}, "BUY_PRODUCT:WHEAT": {"n": 105, "value": 3564}, "BUY_SEED:MELON": {"n": 13, "value": 1040}, "BUY_SEED:WHEAT": {"n": 143, "value": 1430}, "BUY_SEED:STRAWBERRY": {"n": 23, "value": 2300}, "BUY_ANIMAL:GOOSE": {"n": 7, "value": 2100}, "BUY_PRODUCT:FERTILIZER": {"n": 95, "value": 1097}, "BUY_SEED:CARROT": {"n": 60, "value": 1200}, "BUY_SEED:TOMATO": {"n": 14, "value": 700}}]

## 可复现材料

- analyze_exact.py：Python标准库，不依赖kaggle-environments安装。将解释器唯一的resolve_episode_seed导入替换为占位，因重放已有初态不调用初始化；解释器其余动作、市场、日终逻辑原样执行并插桩。
- reference/kaggriculture.py 与 reference/kaggriculture.json：固定解释器/规则副本，用于可携带复算。并未从回放推测价格。
- 运行：python -B analyze_exact.py episode115649229.json episode115650653.json episode115653683.json episode115648413.json
- 再运行：python -B build_report.py
- episode*_exact.json：完整逐单位成功交易、每次田间非移动动作前后、每日状态、逐帧不一致清单（四局均空）。
- gold_replay_features.json：紧凑汇总及完整日序列；daily_layouts.csv：可分析的每日现金/布局/商店/报价。
- overflow_fixtures.json：每次真实日终损耗的完整输入观察、双方原动作、逐单位实际成交、日终卸货前仓/按插入顺序的背包、卸货后仓及逐项丢弃。它是审核测试输入，不是EXP054已存在同样缺陷的证据。
- 原始回放很大，不默认加入用户仓库；保留官方URL、seed、SHA256供再次下载核验。

### SHA256

- episode115649229.json: 62d9382c3b694eea8d7a609b1ae5659dbf9e22a4353757388ed23c6410b3d3a4
- episode115650653.json: 931ba7f7b3ecfb365bbdf27b845171bcc736445e42e6b641d846fc60b4354ad9
- episode115653683.json: eee0d0e02d118d1ad6c83cb24a1e7a59dfc84b3bc437031f5f9d48dff2f5e81e
- episode115648413.json: b1b851acc8e9dad556f93ced24a59d82c4fb99a83dc907a9d41d8b4a2edd7621
- reference/kaggriculture.py: bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
- EXP-045-masterv4-step1002-main.py: 6744b67f9491a65404b70b200bd61a0fd588de513db4f11b119ca0213493686b
- EXP-054-highquote-150-main.py: 3d0002923d42add183e88f912c52b5015639e4386c9a78d7eb3dba91310c33f7

## 如何引入：先审计，再试一个可解释的一步候选（未实施）

以下行号以已核验的 EXP-054-highquote-150-main.py、SHA256 3d0002923d42add183e88f912c52b5015639e4386c9a78d7eb3dba91310c33f7 为准。新候选不改变路线选择，不引入整套规划器，不再次尝试已失败的未来商店需求参数；也不复制EXP066的固定day18/现金42000门控。

### 确切覆盖缺口

- `_v9_courier_plan`，2928行：本步命令或当天剩余原带任一命令不属于PASS/移动/DROP就返回None。因此携有高价值产品但仍安排HARVEST、CARE等工作的工人，旧COURIER有意不接管。
- `_v9_courier`，2943行：只从hour12开始且step<718；只处理原带工人、跳过native.pending。现有四类货物为STRAWBERRY/MILK/WOOL/MELON。它不等于一个“提前送货与多收一次”的机会成本选择器。
- `_race_lost`，5807行：关注上一刻本方仓库已有商品且未卖、对手公开库存变化可归因于出售、原带后续存在销售的错失；它不直接把本方背包中尚未入仓的货纳入这一条件。
- 这说明可以测试一个明确缺口；**尚未证明EXP054在新独立局中因该缺口损失，也未证明扩大覆盖会净赚**。

### 最小实验分两步

1. 先不改变动作，只追加遥测：逐步记录“当前背包、位置、原命令、当前及预计入仓时点、有效仓容、市场剩余槽、RACE信号、候选拒绝理由”。将原带与最后返回动作同时保存，排查原有保护层是否已覆盖。先找真实054独立触发，不能把其他金牌agent的溢出当成本方bug。
2. 只增加一名工人、当前一个动作的A/B候选：A为原054动作；B仅当工人已经站在中央四个仓口、当前原命令是可推迟HARVEST、且背包确有目标产品时，用`PLACE 产品 数量`代替HARVEST，并在同回合卖出真正存入的数量。PLACE只卸目标产品，保留该工人的WHEAT/FERTILIZER，减少DROP带来的后续服务破坏。第一版不挪动位置、不新建多步回仓计划；一步外的移动接管先不做，避免原动作带下一刻站错格。

### 复用点与硬保护

- 外层挂接点：`exp054_highquote_gated_closure_agent`（10266行）返回之后，在独立候选副本中包装。原parent只调用一次，不从中间层重新运行整条策略；原EXP045/054包保持冻结。
- 物理预演：`_r127_fields`（5894行）或`_ov_fields`（4140行附近）模拟全部本方工人顺序与原子PLANT校验；逐项确认B实际存入了多少，不能使用请求数量。仓口容量在田间动作阶段检查，不能用“稍后SELL会腾位”倒推此前PLACE可存入。
- 市场/库存：`_r97_market_stock`（2773行）、`_r97_delivery`（2784行）作为仓存与日终守恒工具，但它们不是完整现金/锁步执行器；购买执行仍需预算检查和官方解释器回归。`_v44y_lockstep`（6044行）可复用逐单位价格比较，`_v44y_factor_margin`（6089行）默认克隆对手只是一种预测，绝不可当成知道对手私有背包。
- 只使用可见对手布局/位置、市场库存变化、已解锁商店及已有`_RACE_STATE`，不得在线读取回放中对手私有库存。既有COURIER计划、native.pending、专用overlay工人、种植/必需FEED/WATER/FERTILIZE/CARE任务一律不接管；第一版排除obs>=696以不碰终局窗口。
- SELL不得无视10槽限制、重复卖同一库存或打乱固定购买的相对顺序；优先合并本商品已有SELL，需新增槽但无空位则拒绝。评价完整市场队列，因为商品报价和订单槽共同决定收入。
- 收益必须减去被推迟HARVEST的机会成本：该格现有产量、下次可收取时间、产出周期、动物max_held或作物衰败、CARE/FEED依赖、以后缺少的可售货。不仅比较当前产品价格。不能证明后续收获可恢复时，应按保守损失上界扣除，或拒绝。
- 选择B后同步`_RACE_STATE[player]['prev_action']`，沿用Step1002（9951行）和054已有的真实动作回写模式，否则下一步对手成交推断会错；其他状态是否受更改影响也需先在影子日志审计。新候选发生异常直接返回已生成的原动作。

### 升级条件

先完成守恒/槽位/供料/下步位置单元测试，再固定官方动作带验证动作确实改变且机制吻合；随后用未参与筛选的种子、双座位和会反应的对手检验净钱差及最坏损失。无独立触发、只在已知例子改善、或仅克隆预测得分上升，都不升级主线。

路线层这次只做覆盖审计：记录day6主路线及day9/12/15/18后续店出现时，既有候选能否达到高需求商品的合理生产规模；不直接硬编码22番茄/21羊，更不根据这四局估计泛化胜率。
