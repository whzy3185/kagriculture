"""Audit paired-seat calendar experiments without treating mirror seat bias as a policy gain."""
from pathlib import Path
import hashlib
import json
import statistics

ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    result={"decision":"", "mechanism":"seventh expected shop: day 22 to day 21 only",
            "protocol_sha256":sha(ROOT/'configs/calendar_protocol_20260930.json'),"bases":{}}
    for number in ('045','054'):
        path=ROOT/'reports'/f'calendar_{number}_vs{number}_fresh24.json'
        report=json.loads(path.read_text())
        assert report['complete'] and not report['errors']
        assert len(report['games'])==48 and all(g['valid'] for g in report['games'])
        by_seed={}
        for game in report['games']:by_seed.setdefault(game['seed'],{})[game['candidate_seat']]=game
        checks=[]
        for seed,games in sorted(by_seed.items()):
            assert set(games)=={0,1}
            a,b=games[0],games[1]
            row={'seed':seed,'action_sha_equal_by_physical_seat':[a['action_sha256'][s]==b['action_sha256'][s] for s in (0,1)],
                 'paired_mean_margin':(a['margin']+b['margin'])/2,
                 'paired_points':sum(1 if g['margin']>0 else .5 if g['margin']==0 else 0 for g in (a,b))/2,
                 'final_shops_equal':a['final_shops']==b['final_shops'], 'decisions':[]}
            for seat in (0,1):
                new=games[seat]['calendar_decisions'][seat]
                old=games[1-seat]['calendar_decisions'][seat]
                assert new is not None and old is not None
                keys=('money','shops','tomato_inventory','tomato_quote','unlocked_quadrants','own_tomatoes',
                      'rival_tomatoes','own_tomato_seeds','own_tomato_shed','target_tiles_locked')
                assert all(new[k]==old[k] for k in keys), (seed,seat,'predecision worlds differ')
                old_ev=old['features'][-1]['revenue'];new_ev=new['features'][-1]['revenue']
                row['decisions'].append({'seat':seat,'old_ev':old_ev,'new_ev':new_ev,'delta_ev':new_ev-old_ev,
                    'old_eligible':old['eligible'],'new_eligible':new['eligible'],
                    'qualified_changed':old['eligible']!=new['eligible']})
            checks.append(row)
        decisions=[d for r in checks for d in r['decisions']]
        result['bases'][number]={
            'source_result':str(path.relative_to(ROOT)),'source_result_sha256':sha(path),
            'summary':report['summary'],'seeds':len(checks),'decisions':len(decisions),
            'qualification_flips':sum(d['qualified_changed'] for d in decisions),
            'same_action_seat_traces':sum(sum(r['action_sha_equal_by_physical_seat']) for r in checks),
            'total_action_seat_traces':2*len(checks),
            'paired_points':statistics.fmean(r['paired_points'] for r in checks),
            'paired_mean_margin':statistics.fmean(r['paired_mean_margin'] for r in checks),
            'minimum_ev_delta':min(d['delta_ev'] for d in decisions),
            'maximum_ev_delta':max(d['delta_ev'] for d in decisions),
            'minimum_baseline_distance_to_9000':min(abs(d['old_ev']-9000) for d in decisions),
            'games_with_any_structural_invalid_status':sum(g['structural_invalid_statuses']>0 for g in report['games']),
            'paired_checks':checks}
    no_trigger=all(b['qualification_flips']==0 and b['same_action_seat_traces']==b['total_action_seat_traces'] for b in result['bases'].values())
    result['decision']='MODEL_CORRECTION_ONLY_NO_BEHAVIORAL_GAIN' if no_trigger else 'EXPERIMENTAL_REQUIRES_REACTIVE_ANCHOR_AND_HOLDOUT'
    result['limitations']=['Synthetic threshold-crossing tests prove model sensitivity, not real match strength.',
        'No silent-no-op frequency audit was performed; complete DONE status alone does not prove every action executed.',
        'The mean-demand projection, 0.25 probability, 2.4 drain slack, rival supply model and 9000 threshold remain unchanged.',
        'These are current-base mirror tests, not a broad independent-opponent strength evaluation.']
    out=ROOT/'reports/calendar_decision_20260930.json';out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='bases'},indent=2))
    for number,b in result['bases'].items():print(number,json.dumps({k:v for k,v in b.items() if k!='paired_checks'}))

if __name__=='__main__':main()
