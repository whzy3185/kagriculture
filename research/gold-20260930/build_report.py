import json,pathlib,collections,csv,hashlib
R=pathlib.Path(__file__).resolve().parent
IDS=[115649229,115650653,115653683,115648413]
SUB={115649229:56679033,115650653:56689315,115653683:56689469,115648413:56689469}
allj=[];fixtures=[];daily=[]
for ep in IDS:
 j=json.load(open(R/f'episode{ep}_exact.json'));raw=json.load(open(R/f'episode{ep}.json'));j['url']=f'https://www.kaggle.com/competitions/kaggriculture/leaderboard?submissionId={SUB[ep]}&episodeId={ep}'
 for p,s in enumerate(j['summary']):
  inc=sum(v['value'] for k,v in s['trade'].items() if k.startswith('SELL'));buy=sum(v['value'] for k,v in s['trade'].items() if k.startswith('BUY'))
  s['ledger']={'opening_cash':3000,'sales':inc,'purchases':buy,'hires':s['hire_cost'],'land':s['land_cost'],'computed_final':3000+inc-buy-s['hire_cost']-s['land_cost'],'matches_reward':3000+inc-buy-s['hire_cost']-s['land_cost']==s['money']}
  peak={}
  for t,ss in enumerate(raw['steps']):
   f=ss[0]['observation']['farms'][p];c=collections.Counter(tile.get('crop',tile.get('animal','')) for row in f['tiles'] for tile in row if isinstance(tile,dict))
   for k,n in c.items():
    if k and n>peak.get(k,{}).get('max_tiles',0):peak[k]={'max_tiles':n,'first_frame':t}
  s['peaks']=peak;s['actual_overflow_units']=dict(sum((collections.Counter(e['loss']) for e in s['overflows']),collections.Counter()))
  s['terminal_private']=raw['steps'][-1][p]['observation']['private']
 for ev in j['overflows']:
  t=ev['step'];p=ev['player'];fixtures.append({'episode':ep,'source':j['url'],'source_sha256':j['source_sha256'],'name':j['episode']['TeamNames'][p],**ev,'observation_before':raw['steps'][t-1][p]['observation'],'actions_both':[s['action'] for s in raw['steps'][t]],'own_actual_transactions':[e for e in j['transactions'] if e['step']==t and e['player']==p]})
 for d in j['daily']:
  for p,s in enumerate(j['summary']):daily.append({'episode':ep,'frame':d['step'],'observation_day':d['day'],'player':p,'name':s['name'],'money':d['money'][p],'layout':json.dumps(d['layout'][p],ensure_ascii=False),'shops':json.dumps(d['shops']),'prices':json.dumps(d['price'])})
 allj.append(j)
(R/'overflow_fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2))
with open(R/'daily_layouts.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=daily[0].keys());w.writeheader();w.writerows(daily)
compact=[]
for j in allj:compact.append({k:v for k,v in j.items() if k not in ['transactions','unit_events','cost_events','mismatches']})
(R/'gold_replay_features.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2))
head='''# 2026-09-30 Kaggriculture 金牌头部完整回放：真实成交、生产及执行机制

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

'''
lines=[head]
for j in allj:
 ep=j['episode']['EpisodeId'];ss=j['summary'];lines += [f"## 回放 {ep}: {ss[0]['name']} vs {ss[1]['name']}\n",f"[官方源]({j['url']})；seed={j['episode']['seed']}；720帧，双方DONE；719次连续状态转移全字段相等。\n",'### 实际成交：数量 / 销售收入 / 加权成交均价\n',f"|商品|{ss[0]['name']}|{ss[1]['name']}|座位1减座位0收入|",'|---|---:|---:|---:|']
 for item in ['WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER']:
  v=[s['trade'].get('SELL:'+item,{'n':0,'value':0}) for s in ss];fmt=lambda x:f"{x['n']} / {x['value']:,} / {x['value']/max(1,x['n']):.2f}"
  lines.append(f"|{item}|{fmt(v[0])}|{fmt(v[1])}|{v[1]['value']-v[0]['value']:+,}|")
 lines += ['\n### 现金闭合\n','|项目|座位0|座位1|','|---|---:|---:|']
 for k in ['opening_cash','sales','purchases','hires','land','computed_final']:
  lines.append(f"|{k}|{ss[0]['ledger'][k]:,.0f}|{ss[1]['ledger'][k]:,.0f}|")
 lines+=['\n### 成功生产服务 / 峰值布局 / 扩地\n']
 for p,s in enumerate(ss):
  lines.append(f"- {s['name']}：FEED {s['FEED']['successful']}；CARE {s['CARE']['successful']}；FERTILIZE {s['FERTILIZE']['successful']}；COLLECT_FERTILIZER {s['COLLECT_FERTILIZER']['successful']}；HARVEST {s['HARVEST']['successful']}；DROP {s['DROP']['successful']}；日终丢弃 {s['actual_overflow_units']}。峰值 {s['peaks']}；买地结果帧 {[x['step'] for x in s['purchases_and_hires']]}。")
 lines += ['\n### 阶段布局（frame为执行后记录索引，day按游戏0起算）\n','|frame/day|座位0现金 / 布局|座位1现金 / 布局|','|---|---|---|']
 for d in j['daily']:
  if d['step'] not in [24,144,216,360,432,480,576,624,719]:continue
  fmt=lambda p:f"{d['money'][p]:,.0f} / "+', '.join(f'{k}:{v}' for k,v in d['layout'][p].items() if k not in ['WEED','PASTURE','COOP'])
  lines.append(f"|{d['step']}/{d['day']}|{fmt(0)}|{fmt(1)}|")
 lines.append('\n商店解锁顺序：'+', '.join(j['daily'][-1]['shops'])+'\n')
 lines.append('实际采购明细（quantity/value）：'+json.dumps([{k:v for k,v in s['trade'].items() if k.startswith('BUY')} for s in ss],ensure_ascii=False)+'\n')
lines+=['''## 可复现材料

- analyze_exact.py：Python标准库，不依赖kaggle-environments安装。将解释器唯一的resolve_episode_seed导入替换为占位，因重放已有初态不调用初始化；解释器其余动作、市场、日终逻辑原样执行并插桩。
- reference/kaggriculture.py 与 reference/kaggriculture.json：固定解释器/规则副本，用于可携带复算。并未从回放推测价格。
- 运行：python -B analyze_exact.py episode115649229.json episode115650653.json episode115653683.json episode115648413.json
- 再运行：python -B build_report.py
- episode*_exact.json：完整逐单位成功交易、每次田间非移动动作前后、每日状态、逐帧不一致清单（四局均空）。
- gold_replay_features.json：紧凑汇总及完整日序列；daily_layouts.csv：可分析的每日现金/布局/商店/报价。
- overflow_fixtures.json：每次真实日终损耗的完整输入观察、双方原动作、逐单位实际成交、日终卸货前仓/按插入顺序的背包、卸货后仓及逐项丢弃。它是审核测试输入，不是EXP054已存在同样缺陷的证据。
- 原始回放很大，不默认加入用户仓库；保留官方URL、seed、SHA256供再次下载核验。

### SHA256
''']
for j in allj:lines.append(f"- episode{j['episode']['EpisodeId']}.json: {j['source_sha256']}")
lines.append(f"- reference/kaggriculture.py: {allj[0]['interpreter_sha256']}")
for p in sorted(R.glob('EXP-*-main.py')):lines.append(f'- {p.name}: {hashlib.sha256(p.read_bytes()).hexdigest()}')
lines.append('\n'+(R/'EXP054_MINIMAL_CANDIDATE_NOTES.md').read_text())
(R/'GOLD_REPLAY_MECHANICS_20260930.md').write_text('\n'.join(lines),encoding='utf-8')
print('Report ready:',R/'GOLD_REPLAY_MECHANICS_20260930.md')
print('All ledgers:',[(j['episode']['EpisodeId'],j['mismatch_count'],[s['ledger']['matches_reward'] for s in j['summary']]) for j in allj])
