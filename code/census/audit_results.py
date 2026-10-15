#!/usr/bin/env python3
"""Audit completed Six Trap outputs without rerunning the full census.

Usage: python audit_results.py RUN_DIR [VERIFICATION_DIR]
Standard library only. This checks internal consistency and all cycle edges;
it does not turn a finite computation into a universal proof.
"""
from __future__ import annotations
import csv
import json
import math
import pathlib
import sys
from fractions import Fraction

def rows(path: pathlib.Path) -> list[dict[str, int]]:
    with path.open(newline='') as f:
        return [{k:int(v) for k,v in r.items()} for r in csv.DictReader(f)]

def largest_proper_divisor_by_enumeration(n: int) -> int:
    best=1
    for d in range(1,math.isqrt(n)+1):
        if n%d==0:
            if d<n: best=max(best,d)
            partner=n//d
            if partner<n: best=max(best,partner)
    return best

def audit(run: pathlib.Path, verification: pathlib.Path | None=None) -> dict:
    s=json.loads((run/'summary.json').read_text())
    assert s['status']=='complete'
    assert s['completed_seed_count']==s['seed_end']-s['seed_start']+1==s['requested_seed_count']
    assert s['unclassified_seed_count']==s['cap_hits']==0
    b=rows(run/'basins.csv'); h=rows(run/'stopping_time_histogram.csv'); c=rows(run/'cycles.csv')
    assert sum(r['seed_count'] for r in b)==s['completed_seed_count']
    assert len(b)==s['cycles_found']==len(set(r['cycle_minimum'] for r in b))
    assert sorted(r['cycle_minimum'] for r in b)==s['cycle_minima']
    assert sum(r['seed_count'] for r in h)==s['completed_seed_count']
    weighted=sum(r['seed_count']*r['steps_to_first_cycle_entry'] for r in h)
    assert weighted==sum(r['total_steps_to_cycle'] for r in b)==s['sum_of_individual_steps_to_cycle']
    assert max(r['steps_to_first_cycle_entry'] for r in h if r['seed_count'])==s['maximum_steps_to_first_cycle_entry']
    assert sum(r['period'] for r in b)==len(c)
    if all(r['cycle_maximum']<=s['seed_end'] for r in b):
        assert h[0]['steps_to_first_cycle_entry']==0
        assert h[0]['seed_count']==sum(r['period'] for r in b)
    for basin in b:
        members=[r for r in c if r['cycle_minimum']==basin['cycle_minimum']]
        assert len(members)==basin['period']
        assert len(set(r['n'] for r in members))==len(members)
        assert min(r['n'] for r in members)==basin['cycle_minimum']
        assert max(r['n'] for r in members)==basin['cycle_maximum']
        for i,r in enumerate(members):
            n=r['n'];expected=n+largest_proper_divisor_by_enumeration(n)-largest_proper_divisor_by_enumeration(n+1)
            assert expected==r['next_n']==members[(i+1)%len(members)]['n']
    a=rows(run/'stopping_time_records.csv'); p=rows(run/'peak_records.csv'); ratios=rows(run/'excursion_ratio_records.csv')
    for recs in [a,p,ratios]:
        assert all(recs[i]['seed']<recs[i+1]['seed'] for i in range(len(recs)-1))
    for recs in [a,p]:
        assert all(recs[i]['value']<recs[i+1]['value'] for i in range(len(recs)-1))
    assert all(Fraction(ratios[i]['value'],ratios[i]['seed'])<Fraction(ratios[i+1]['value'],ratios[i+1]['seed']) for i in range(len(ratios)-1))
    assert a[-1]['value']==s['maximum_steps_to_first_cycle_entry']
    assert a[-1]['seed']==s['first_seed_at_maximum_steps']
    assert p[-1]['value']==s['maximum_orbit_value']
    assert p[-1]['seed']==s['first_seed_attaining_maximum_orbit_value']
    assert ratios[-1]['value']==s['maximum_excursion_ratio_numerator']
    assert ratios[-1]['seed']==s['maximum_excursion_ratio_denominator']
    assert 0<=s['adjacent_seed_pairs_with_different_attractors']<=s['adjacent_seed_pairs']==s['completed_seed_count']-1
    qs={}
    for q in [Fraction(1,2),Fraction(9,10),Fraction(99,100),Fraction(999,1000)]:
        threshold=(q.numerator*s['completed_seed_count']+q.denominator-1)//q.denominator
        cumulative=0
        for r in h:
            cumulative+=r['seed_count']
            if cumulative>=threshold:
                qs[str(q)]=r['steps_to_first_cycle_entry'];break
    v=None
    if verification is not None:
        v=json.loads((verification/'verification.json').read_text())
        assert v['status']=='all_checked_targets_match'
        assert v['independently_discovered_cycles']==s['cycles_found']
        independent=rows(verification/'independently_discovered_cycles.csv')
        assert [(r['cycle_minimum'],r['n'],r['next_n']) for r in independent]==[(r['cycle_minimum'],r['n'],r['next_n']) for r in c]
        witnesses=rows(verification/'record_trajectories_summary.csv')
        witnessed={r['seed']:r for r in witnesses}
        for r in a: assert witnessed[r['seed']]['steps_to_first_cycle_entry']==r['value']
        for r in p+ratios: assert witnessed[r['seed']]['maximum_orbit_value']==r['value']
    result={'status':'passed','all_cycle_edges_brute_divisor_checked':len(c),
            'complete_interval_seed_count':s['completed_seed_count'],
            'count_histogram_weighted_sum_record_and_cycle_checks':'passed',
            'steps_to_cycle_quantiles':qs,
            'mean_steps_to_cycle':weighted/s['completed_seed_count'],
            'adjacent_attractor_difference_percent':100*s['adjacent_seed_pairs_with_different_attractors']/s['adjacent_seed_pairs'],
            'maximum_excursion_ratio':s['maximum_excursion_ratio_numerator']/s['maximum_excursion_ratio_denominator'],
            'independent_verification':v,
            'scope':'Output audit, cycle-edge enumeration and optional independently computed targets; not a second full census or universal proof.'}
    (run/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    if len(sys.argv) not in (2,3): raise SystemExit('Usage: python audit_results.py RUN_DIR [VERIFICATION_DIR]')
    try:
        print(json.dumps(audit(pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2]) if len(sys.argv)==3 else None),indent=2))
    except (OSError,ValueError,KeyError,AssertionError) as e:
        raise SystemExit(f'AUDIT FAILED: {e}')
