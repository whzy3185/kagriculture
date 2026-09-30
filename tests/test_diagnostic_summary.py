import pytest
from scripts.diagnose_frozen_agents import percentile, summarize

def game(margin,valid=True):
    return {'valid':valid,'margin':margin,'elapsed_seconds':1}

def test_invalid_terminal_results_do_not_become_wins():
    report=summarize([game(1000000,False),game(-5),game(5),game(0)])
    assert report['valid_games']==3 and report['invalid_games']==1
    assert (report['wins'],report['ties'],report['losses'])==(1,1,1)
    assert report['mean_margin']==0 and report['points']==.5

def test_no_valid_matches_have_no_win_rate():
    assert summarize([game(5,False)])=={'valid_games':0,'invalid_games':1}

def test_interpolated_tail_metrics():
    assert percentile([30,0,10,20],.1)==pytest.approx(3)
