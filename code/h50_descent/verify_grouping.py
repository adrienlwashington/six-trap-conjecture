#!/usr/bin/env python3
"""Rebuild continuation masses without importing the grouping implementation.
Uses cumulative CRT survival products and logarithm-seeded, exact-corrected
upward rounding, rather than the original sequential mixture/bisect routine.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json,gzip,math,time,argparse

def run(folder,result,out):
    t0=time.perf_counter();d=json.loads(result.read_text());step=F(d['grid_step'])
    groups=defaultdict(F);absorbed=F(0);mass=F(0);depth=0;records=0
    powers={0:F(1)}
    def power(i):
        if i not in powers:powers[i]=step**i
        return powers[i]
    def record(A,previousE,w,k):
        nonlocal absorbed,depth
        depth=max(depth,k)
        if A<=1:absorbed+=w;return
        i=max(0,math.ceil(math.log(float(A))/math.log(float(step))))
        while power(i)<A:i+=1
        while i and power(i-1)>=A:i-=1
        groups[i,previousE]+=w
    primes=[q for q in range(5,98,2) if all(q%r for r in range(3,math.isqrt(q)+1,2))]
    with gzip.open(folder/'frontier.jsonl.gz','rt') as f:
        for line in f:
            x=json.loads(line);A=F(int(x['u']),int(x['M']));w=F(*map(int,x['weight']));k=len(x['path'])
            mass+=w;records+=1
            if x['kind']!='prime_tail':record(A,0,w,k);continue
            if x['odd']:record(A*F(103,202),0,w,k+1);continue
            assert d['aware']
            record(A*F(9,4),1,w/2,k+2)
            before=F(1)
            for q in primes:
                allowed=q-len(x['forbidden'].get(str(q),()))
                after=F(0) if int(x['u'])%q==0 else before*F(allowed-1,allowed)
                record(A*F(3*(q+2),4*q),0,w*(before-after)/2,k+2)
                before=after
                if not before:break
            if before:record(A*F(309,404),0,w*before/2,k+2)
    expected={(a['idx'],a['prevE']):F(a['weight']) for a in d['groups']}
    groups={key:value for key,value in groups.items() if value}
    assert groups==expected
    assert absorbed==F(*map(int,d['immediate']))
    assert mass==F(*map(int,d['total_frontier_mass'])) and mass==absorbed+sum(groups.values(),F(0))
    assert depth==d['max_prefix']
    res={'all_passed':True,'frontier_families_regrouped':records,'groups_matched':len(groups),
         'immediate_density':str(absorbed),'total_frontier_density':str(mass),
         'max_prefix_steps':depth,'seconds':time.perf_counter()-t0}
    out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True)
    p.add_argument('--groups',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();run(a.folder,a.groups,a.out)
