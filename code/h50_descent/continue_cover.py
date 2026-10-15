#!/usr/bin/env python3
"""Exact finite-parity continuation, including a prime-aware even-tail bound.
All products, upward rounding, word counts and final weights use integers or
Fractions. Floating point is used only in display and work ordering.
"""
from __future__ import annotations
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import argparse,gzip,json,math,time,bisect
from descent_attack import primes_up_to

def group_frontier(folder:Path,out:Path,step:F,aware:bool):
    grids=[F(1)]
    for _ in range(2000): grids.append(grids[-1]*step)
    groups=defaultdict(F); immediate=F(0); total=F(0); max_prefix=0
    def add(A,prevE,weight,depth):
        nonlocal immediate,max_prefix
        if not weight:return
        max_prefix=max(max_prefix,depth)
        if A<=1:immediate+=weight;return
        idx=bisect.bisect_left(grids,A)
        if idx==len(grids):raise ValueError('grid too short')
        assert grids[idx]>=A and (idx==0 or grids[idx-1]<A)
        groups[idx,prevE]+=weight
    with gzip.open(folder/'frontier.jsonl.gz','rt') as f:
        for line in f:
            d=json.loads(line); A=F(int(d['u']),int(d['M']));w=F(*map(int,d['weight']))
            total+=w; depth=len(d['path'])
            if d['kind']!='prime_tail':
                add(A,0,w,depth);continue
            if d['odd']:
                p=d['next_prime'];add(A*F(p+2,2*p),0,w,depth+1);continue
            if not aware:
                add(A*F(3,2),1,w,depth+1);continue
            add(A*F(9,4),1,w/2,depth+2)
            left=w/2;u=int(d['u']);forbid=d['forbidden']
            for q in primes_up_to(d['next_prime']-1):
                if q==3:continue
                available=q-len(forbid.get(str(q),[]))
                assert available>0
                probability=F(1) if u%q==0 else F(1,available)
                take=left*probability
                add(A*F(3,2)*F(q+2,2*q),0,take,depth+2)
                left-=take
                if not left:break
            if left:
                q=d['next_prime'];add(A*F(3,2)*F(q+2,2*q),0,left,depth+2)
    assert immediate+sum(groups.values(),F(0))==total
    payload={'aware':aware,'grid_step':str(step),'max_prefix':max_prefix,
             'immediate':[str(immediate.numerator),str(immediate.denominator)],
             'total_frontier_mass':[str(total.numerator),str(total.denominator)],
             'groups':[{'idx':i,'prevE':b,'A':str(grids[i]),'weight':str(w)}
                       for (i,b),w in sorted(groups.items())]}
    out.write_text(json.dumps(payload,indent=2)+'\n')
    return payload

def probabilities(A:F,prev:int,H:int,checkpoints:set[int]):
    states={(0,0,prev):1}; result={}; anum=A.numerator; aden=A.denominator
    pow2=[1];pow3=[1];pow5=[1];pow7=[1]
    for i in range(H):
        pow2.append(pow2[-1]*2);pow3.append(pow3[-1]*3)
        pow5.append(pow5[-1]*5);pow7.append(pow7[-1]*7)
    def absorbed(t,e,c):
        o=t-e-c
        return anum*pow3[e]*pow7[c]*pow5[o]<=aden*pow2[t]*pow5[c]*pow3[o]
    for t in range(1,H+1):
        nxt=defaultdict(int)
        for (e,c,b),count in states.items():
            if not absorbed(t,e+1,c):nxt[e+1,c,1]+=count
            co=c+b
            if not absorbed(t,e,co):nxt[e,co,0]+=count
        states=nxt
        if t in checkpoints:
            result[t]=F(pow2[t]-sum(states.values()),pow2[t])
    return result

def run(folder:Path,out:Path,aware:bool,step:F,H:int):
    out.mkdir(exist_ok=True,parents=True);t0=time.perf_counter()
    payload=group_frontier(folder,out/'groups.json',step,aware)
    print(json.dumps({'stage':'grouped','groups':len(payload['groups']),
                      'max_prefix':payload['max_prefix'],
                      'immediate':float(F(*map(int,payload['immediate']))),
                      'seconds':time.perf_counter()-t0}),flush=True)
    summary=json.loads((folder/'summary.json').read_text())
    base=F(*map(int,summary['exact_certified_density']))+F(*map(int,payload['immediate']))
    checkpoints={k for k in (10,20,40,60,80,100,H) if k<=H}
    bounds={k:base for k in checkpoints}; detail=[]
    for j,g in enumerate(payload['groups']):
        A=F(g['A']);w=F(g['weight']); ps=probabilities(A,g['prevE'],H,checkpoints)
        for k,prob in ps.items():bounds[k]+=w*prob
        detail.append({**g,'probabilities':{str(k):str(p) for k,p in ps.items()}})
        if j%20==0:print(json.dumps({'stage':'DP','done':j,'total':len(payload['groups']),
                                   'seconds':time.perf_counter()-t0}),flush=True)
    res={'aware':aware,'grid_step':str(step),'horizon':H,'max_prefix':payload['max_prefix'],
         'certificate_max_steps':summary['certificate_max_steps'],
         'bounds':{str(k):{'total_steps_at_most':max(summary['certificate_max_steps'],payload['max_prefix']+k),
                          'exact_density':str(v),'decimal_density':float(v)} for k,v in sorted(bounds.items())},
         'groups':detail,'seconds':time.perf_counter()-t0}
    (out/'continuation_result.json').write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps({k:v for k,v in res.items() if k!='groups'}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--aware',action='store_true')
    p.add_argument('--grid',default='21/20');p.add_argument('--horizon',type=int,default=60)
    a=p.parse_args();run(a.folder,a.out,a.aware,F(a.grid),a.horizon)
