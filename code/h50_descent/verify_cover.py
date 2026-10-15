#!/usr/bin/env python3
"""Independent checker: explicit symbolic branch replay, CRT exclusions,
periodic densities recomputed from M and forbidden residues, and leaf disjointness.
Does not import the search program or rely on its stored density calculations.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,gzip,json,time,math

P=[p for p in range(3,102,2) if all(p%d for d in range(3,math.isqrt(p)+1,2))]

def verify(folder:Path,out:Path):
    t0=time.perf_counter();mass=F(0);cmass=F(0);records=certs=0
    leaves={}; symbol_steps=exclusions=0;maxdepth=0
    for fname in ('certificates.jsonl.gz','frontier.jsonl.gz'):
        with gzip.open(folder/fname,'rt') as f:
            for line in f:
                d=json.loads(line)
                M,r,u,v=map(int,(d['M'],d['r'],d['u'],d['v']))
                assert M>0 and 0<=r<M and u>0
                Fq={int(q):frozenset(a) for q,a in d['forbidden'].items()}
                weight=F(1,M)
                for q,bad in Fq.items():
                    assert q in P and len(bad)<q and all(0<=z<q for z in bad)
                    weight*=F(q-len(bad),q)
                assert weight==F(*map(int,d['weight']))
                a,b=M,r;events=[]
                def excludes_prime(q,aa,bb):
                    nonlocal exclusions
                    exclusions+=1
                    if aa%q==0:assert bb%q!=0
                    else:assert (-bb*pow(aa,-1,q))%q in Fq.get(q,())
                for odd,p in d['path']:
                    assert p in P and a%2==0 and b%2==odd
                    offset=1-odd
                    assert a%p==0 and (b+offset)%p==0
                    for q in P:
                        if q>=p:break
                        excludes_prime(q,a,b+offset)
                    numerator=p+2 if odd else 3*p-2
                    subtract=p if odd else 2
                    assert numerator*a%(2*p)==0
                    assert (numerator*b-subtract)%(2*p)==0
                    a,b=numerator*a//(2*p),(numerator*b-subtract)//(2*p)
                    symbol_steps+=1;events.extend((('parity',odd),('prime',p)))
                assert (a,b)==(u,v)
                if d['path']:assert u*r-v*M>0
                kind=d['kind'];depth=len(d['path'])
                if kind in ('parity_bound','prime_tail','tail_bound'):
                    odd=d['odd'];assert u%2==0 and v%2==odd
                    events.append(('parity',odd));depth+=1
                    if kind!='parity_bound':
                        nxt=d['next_prime'];assert nxt==101
                        for q in P:
                            if q>=nxt:break
                            excludes_prime(q,u,v+(1-odd))
                        events.append(('tail',nxt))
                    if kind!='prime_tail':
                        bound=(F(5,6) if odd else F(3,2)) if kind=='parity_bound' else (F(103,202) if odd else F(3,2))
                        assert F(u,M)*bound<=1
                else:
                    assert u%2==1
                    if kind=='exact':assert u<=M
                events=tuple(events)
                assert events not in leaves
                leaves[events]=kind
                mass+=weight;records+=1
                if fname.startswith('cert'):
                    assert kind in ('exact','parity_bound','tail_bound')
                    cmass+=weight;certs+=1;maxdepth=max(maxdepth,depth)
                if records%50000==0:print(json.dumps({'records':records,'seconds':time.perf_counter()-t0}),flush=True)
    for word in leaves:
        for k in range(len(word)):
            assert word[:k] not in leaves
    assert mass==1
    s=json.loads((folder/'summary.json').read_text())
    assert cmass==F(*map(int,s['exact_certified_density']))
    assert certs==s['certificates'] and maxdepth==s['certificate_max_steps']
    res={'all_checks_passed':True,'families_checked':records,'certificates_checked':certs,
         'symbolic_branch_steps_checked':symbol_steps,'least_prime_exclusions_checked':exclusions,
         'density_recomputed_from_periodic_constraints':str(cmass),
         'full_partition_mass':str(mass),'prefix_disjointness_passed':True,
         'max_certified_steps':maxdepth,'seconds':time.perf_counter()-t0}
    out.write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();verify(a.folder,a.out)
