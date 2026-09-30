import json,sys,copy,collections,types,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
SOURCE=ROOT/'reference/kaggriculture.py'
class D(dict):
 def __getattr__(self,k):
  try:return self[k]
  except KeyError:raise AttributeError(k)
 def __setattr__(self,k,v):self[k]=v

def attr(x):
 if isinstance(x,dict):return D({k:attr(v) for k,v in x.items()})
 if isinstance(x,list):return [attr(v) for v in x]
 return x
m=types.ModuleType('interp');m.__file__=str(SOURCE)
exec(compile(SOURCE.read_text().replace('from kaggle_environments.utils import resolve_episode_seed','resolve_episode_seed = None'),str(SOURCE),'exec'),m.__dict__)

def analyze(path):
 j=json.load(open(path));steps=j['steps'];ctx={};events=[];units=[];costs=[];overflows=[];mismatches=[]
 orig_commit=m._commit_unit;orig_unit=m._apply_unit_action;orig_hire=m._do_hire;orig_land=m._do_buy_land;orig_drop=m._drop_inventories_to_shed
 def commit(op,item,price,farm,private,market,shed_capacity=100):
  ok=orig_commit(op,item,price,farm,private,market,shed_capacity)
  if ok:events.append(dict(step=ctx['step'],player=ctx['ids'][id(farm)],op=op,item=item,price=price))
  return ok
 def unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity=100):
  pos=m._farmer_position(farm,idx)
  if pos is None:return orig_unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
  x,y=pos;before=copy.deepcopy((farm['tiles'][y][x],private));beforepos=list(pos)
  result=orig_unit(farm,private,idx,action,board_size,day,turns_per_day,shed_capacity)
  op=action[0] if action else ''
  if op not in ('NORTH','SOUTH','EAST','WEST','PASS'):
   btil,bpri=before;atil=farm['tiles'][y][x];ainv=private['inventories'][idx];binv=bpri['inventories'][idx]
   delta={k:ainv.get(k,0)-binv.get(k,0) for k in set(ainv)|set(binv) if ainv.get(k,0)!=binv.get(k,0)}
   shdelta={k:private['shed'].get(k,0)-bpri['shed'].get(k,0) for k in private['shed'] if private['shed'].get(k,0)!=bpri['shed'].get(k,0)}
   ev=dict(step=ctx['step'],player=ctx['ids'][id(farm)],unit=idx,pos=beforepos,action=action,success=(btil!=atil or bpri!=private),inventory_delta=delta,shed_delta=shdelta,tile_before=btil,tile_after=copy.deepcopy(atil))
   units.append(ev)
  return result
 def hire(farm,private,board_size,mult=1):
  b=farm['money'];n=farm['hires_today'];orig_hire(farm,private,board_size,mult)
  costs.append(dict(step=ctx['step'],player=ctx['ids'][id(farm)],op='HIRE',cost=b-farm['money'],success=farm['hires_today']>n))
 def land(farm,board_size):
  b=farm['money'];orig_land(farm,board_size)
  costs.append(dict(step=ctx['step'],player=ctx['ids'][id(farm)],op='BUY_LAND',cost=b-farm['money'],success=b>farm['money']))
 def drop(private,capacity):
  b=collections.Counter(private['shed']);[b.update(inv) for inv in private['inventories']]
  before=copy.deepcopy(private)
  orig_drop(private,capacity)
  loss=b-collections.Counter(private['shed'])
  if loss:overflows.append(dict(step=ctx['step'],observation_step=ctx['step']-1,player=ctx['pids'][id(private)],loss=dict(loss),capacity=capacity,pre_auto_drop_private=before,pre_auto_drop_ordered_cargo=[list(inv.items()) for inv in before['inventories']],post_auto_drop_private=copy.deepcopy(private)))
 m._commit_unit=commit;m._apply_unit_action=unit;m._do_hire=hire;m._do_buy_land=land;m._drop_inventories_to_shed=drop
 env=types.SimpleNamespace(done=False,configuration=attr(j['configuration']),info=j['info'])
 st=[attr({'observation':copy.deepcopy(steps[0][p]['observation']),'action':None,'status':'ACTIVE','reward':0}) for p in range(2)]
 for t in range(1,len(steps)):
  for p in range(2):st[p].action=attr(steps[t][p]['action'])
  st[0].observation.step=t-1
  ctx.update(step=t,ids={id(f):p for p,f in enumerate(st[0].observation.farms)},pids={id(s.observation.private):p for p,s in enumerate(st)})
  m.interpreter(st,env)
  for p in range(2):
   for k in ['farms','private','market','town','day','hour']:
    a=st[p].observation.get(k);b=steps[t][p]['observation'].get(k)
    if a!=b:
     mismatches.append({'step':t,'player':p,'field':k,'simulated':a,'replay':b})
     if len(mismatches)<5:print('MISMATCH',t,p,k)
 m._commit_unit=orig_commit;m._apply_unit_action=orig_unit;m._do_hire=orig_hire;m._do_buy_land=orig_land;m._drop_inventories_to_shed=orig_drop
 def counts(f):
  c=collections.Counter()
  for row in f['tiles']:
   for tile in row:
    if isinstance(tile,dict):c[tile.get('crop',tile.get('animal',tile['kind']))]+=1
  return dict(c)
 daily=[]
 for t in [*range(0,len(steps),24),len(steps)-1]:
  o=steps[t][0]['observation']
  daily.append(dict(step=t,day=o['day'],money=[f['money'] for f in o['farms']],layout=[counts(f) for f in o['farms']],shops=o['town']['unlocked_shops'],price=o['market']['prices']))
 summaries=[]
 for p in range(2):
  trade={}
  for e in events:
   if e['player']!=p:continue
   key=e['op']+':'+e['item'];v=trade.setdefault(key,{'n':0,'value':0});v['n']+=1;v['value']+=e['price']
  s=dict(name=j['info']['TeamNames'][p],money=j['rewards'][p],trade=trade,hire_cost=sum(e['cost'] for e in costs if e['player']==p and e['op']=='HIRE'),land_cost=sum(e['cost'] for e in costs if e['player']==p and e['op']=='BUY_LAND'))
  for tag in ['FEED','CARE','FERTILIZE','HARVEST','DROP','COLLECT_FERTILIZER','PLANT','DIG','WATER']:
   u=[e for e in units if e['player']==p and e['action'][0]==tag];s[tag]={'requests':len(u),'successful':sum(e['success'] for e in u),'positive_inventory':dict(sum((collections.Counter({k:v for k,v in e['inventory_delta'].items() if v>0}) for e in u),collections.Counter()))}
  s['overflows']=[e for e in overflows if e['player']==p]
  s['purchases_and_hires']=[e for e in costs if e['player']==p and e['success'] and e['op']=='BUY_LAND']
  s['hire_days']=[{'day':d,'n':sum(e['success'] for e in costs if e['player']==p and e['op']=='HIRE' and (e['step']-1)//24==d),'cost':sum(e['cost'] for e in costs if e['player']==p and e['op']=='HIRE' and (e['step']-1)//24==d)} for d in range(30)]
  summaries.append(s)
 result={'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'interpreter_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'source':str(path),'episode':j['info'],'statuses':j['statuses'],'recorded_frames':len(steps),'transitions_verified':len(steps)-1,'mismatch_count':len(mismatches),'summary':summaries,'daily':daily,'transactions':events,'unit_events':units,'cost_events':costs,'overflows':overflows,'mismatches':mismatches}
 out=path.parent/(path.stem+'_exact.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:result[k] for k in ['episode','statuses','transitions_verified','mismatch_count','summary','daily']},ensure_ascii=False,indent=2))
 return out
if __name__=='__main__':
 for arg in sys.argv[1:]:analyze(pathlib.Path(arg))
