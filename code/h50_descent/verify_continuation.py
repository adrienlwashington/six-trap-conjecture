#!/usr/bin/env python3
"""Independent continuation checker using Fraction-valued state keys,
explicit short-word enumeration, and modular tests of the prime-tail lemma.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import argparse,json,gzip,itertools,time,math

def fraction_dp(A,prev,H):
    live={(A,prev):1}
    for t in range(1,H+1):
        nxt=defaultdict(int)
        for (product,b),count in live.items():
            ee=product*F(3,2)
            if ee>1:nxt[ee,1]+=count
            oo=product*(F(7,10) if b else F(5,6))
            if oo>1:nxt[oo,0]+=count
        live=nxt
    return F(2**H-sum(live.values()),2**H)

def brute(A,prev,H):
    yes=0
    for word in itertools.product((0,1),repeat=H):
        B=A;b=prev
        for odd in word:
            B*= (F(7,10) if b else F(5,6)) if odd else F(3,2)
            b=1-odd
            if B<=1:yes+=1;break
    return F(yes,2**H)

def modular_checks(folder,limit=700):
    primes=[p for p in range(3,102,2) if all(p%d for d in range(3,math.isqrt(p)+1,2))]
    selected=0; tests=0
    with gzip.open(folder/'frontier.jsonl.gz','rt') as f:
        for line in f:
            d=json.loads(line)
            if d['kind']!='prime_tail' or d['odd']:continue
            u,v=int(d['u']),int(d['v']);bad={int(q):set(a) for q,a in d['forbidden'].items()}
            p=101
            if u%p==0:continue
            r=(-(v+1)*pow(u,-1,p))%p
            UU=(3*p-2)*u//2
            VV=((3*p-2)*(u*r+v)-2)//(2*p)
            assert ((3*p-2)*(u*r+v)-2)%(2*p)==0 and UU%2==1
            bit=(1-VV)%2; AA=2*UU;BB=UU*bit+VV
            assert BB%2==1
            for q in primes:
                if q>=101:break
                allowed=[];hits=0
                for s in range(q):
                    old=(p*(2*s+bit)+r)%q
                    if old not in bad.get(q,set()):
                        allowed.append(s);hits+=(AA*s+BB)%q==0
                assert len(allowed)==q-len(bad.get(q,set()))
                if q==3:assert hits==0
                else:
                    cap=F(1) if u%q==0 else F(1,len(allowed))
                    assert F(hits,len(allowed))<=cap
                tests+=1
            selected+=1
            if selected==limit:break
    return {'prime_tail_families_sampled':selected,'modular_divisibility_bounds_checked':tests,
            'actual_even_branch_prime':101,'all_passed':True,
            'scope':'finite checks only; universal lemma is proved in the report'}

def run(folder,result,out):
    t0=time.perf_counter();d=json.loads(result.read_text());H=d['horizon']
    groups=d['groups'];done=0
    for g in groups:
        ans=fraction_dp(F(g['A']),g['prevE'],H)
        assert ans==F(g['probabilities'][str(H)])
        done+=1
        if done%50==0:print(json.dumps({'groups_checked':done,'total':len(groups),'seconds':time.perf_counter()-t0}),flush=True)
    short=0
    for idx in sorted({0,len(groups)//5,len(groups)//2,3*len(groups)//4,len(groups)-1}):
        g=groups[idx]
        for h in (6,10,12):
            assert brute(F(g['A']),g['prevE'],h)==fraction_dp(F(g['A']),g['prevE'],h)
            short+=1
    mod=modular_checks(folder)
    groupdata=json.loads((result.parent/'groups.json').read_text())
    summary=json.loads((folder/'summary.json').read_text())
    total=F(*map(int,summary['exact_certified_density']))+F(*map(int,groupdata['immediate']))
    for g in groups:total+=F(g['weight'])*F(g['probabilities'][str(H)])
    assert total==F(d['bounds'][str(H)]['exact_density'])
    out.write_text(json.dumps({'all_passed':True,'fraction_DP_groups_checked':done,
        'horizon':H,'brute_force_short_word_checks':short,'modular_checks':mod,
        'final_exact_density':str(total),'seconds':time.perf_counter()-t0},indent=2)+'\n')
    print(json.dumps({'all_passed':True,'groups':done,'seconds':time.perf_counter()-t0}),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True)
    p.add_argument('--result',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();run(a.folder,a.result,a.out)
