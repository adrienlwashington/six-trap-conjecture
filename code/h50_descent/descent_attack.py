#!/usr/bin/env python3
"""Exact arithmetic-family descent search for T(n)=n+D(n)-D(n+1).
No sampled trajectory is used as a proof. Every terminal proof describes
an infinite congruence family. Unresolved prime tails are explicitly retained.
"""
from __future__ import annotations
from fractions import Fraction as F
from dataclasses import dataclass
import argparse, heapq, itertools, json, gzip, time
from pathlib import Path


def primes_up_to(n: int) -> list[int]:
    a=bytearray(b'\x01')*(n+1); a[:2]=b'\x00\x00'
    for p in range(2,int(n**.5)+1):
        if a[p]: a[p*p:n+1:p]=b'\x00'*len(range(p*p,n+1,p))
    return [p for p in range(3,n+1) if a[p]]

@dataclass(slots=True)
class Node:
    M:int; r:int; u:int; v:int
    forbidden:dict[int,frozenset[int]]
    weight:F
    path:tuple[tuple[int,int],...]


def sub(node:Node, a:int, b:int, weight:F) -> Node | None:
    """Substitute old parameter t=a*s+b exactly."""
    forb={}
    for q, bad in node.forbidden.items():
        if a%q==0:
            if b%q in bad: return None
        else:
            inv=pow(a,-1,q)
            forb[q]=frozenset(((x-b)*inv)%q for x in bad)
    return Node(node.M*a,node.r+node.M*b,node.u*a,node.v+node.u*b,
                forb,weight,node.path)


def fix_parity(node:Node, odd:int) -> Node:
    assert node.u%2==1
    b=(odd-node.v)%2
    ans=sub(node,2,b,node.weight/2)
    assert ans is not None and ans.v%2==odd
    return ans


def apply_branch(node:Node, odd:int, p:int) -> Node:
    if odd:
        a,b=p+2,p
    else:
        a,b=3*p-2,2
    assert (a*node.u)%(2*p)==0
    assert (a*node.v-b)%(2*p)==0
    return Node(node.M,node.r,a*node.u//(2*p),(a*node.v-b)//(2*p),
                node.forbidden,node.weight,node.path+((odd,p),))


def least_prime_children(node:Node, odd:int, primes:list[int]):
    """Yield exact least-prime children, plus final unprocessed tail."""
    rem=node
    for p in primes:
        u=rem.u; v=rem.v+(1-odd)
        if u%p==0:
            if v%p==0:
                yield apply_branch(rem,odd,p),None
                return
            continue
        root=(-v*pow(u,-1,p))%p
        bad=rem.forbidden.get(p,frozenset())
        if root in bad: continue
        available=p-len(bad)
        child=sub(rem,p,root,rem.weight/available)
        assert child is not None
        yield apply_branch(child,odd,p),None
        if available==1: return
        ff=rem.forbidden.copy(); ff[p]=bad|{root}
        rem=Node(rem.M,rem.r,rem.u,rem.v,ff,
                 rem.weight*F(available-1,available),rem.path)
    yield None,rem


def encode(node:Node, kind:str, **extra):
    obj={'kind':kind,'path':node.path,'M':str(node.M),'r':str(node.r),
         'u':str(node.u),'v':str(node.v),
         'forbidden':{str(q):sorted(v) for q,v in node.forbidden.items()},
         'weight':[str(node.weight.numerator),str(node.weight.denominator)]}
    obj.update(extra)
    return obj


def run(prime_max:int,max_nodes:int,max_depth:int,out:Path):
    out.mkdir(parents=True,exist_ok=True)
    primes=primes_up_to(prime_max)
    nxt=prime_max+1
    while any(nxt%p==0 for p in range(2,int(nxt**.5)+1)): nxt+=1
    serial=itertools.count(); heap=[]
    root=Node(1,0,1,0,{},F(1),())
    heapq.heappush(heap,(-1.0,next(serial),root))
    cert_mass=F(0); tail_mass=F(0);depth_mass=F(0)
    cert_count=tail_count=depth_count=0; max_cert_depth=0; expanded=0
    t0=time.perf_counter(); checkpoints=[]
    certfile=gzip.open(out/'certificates.jsonl.gz','wt')
    frontierfile=gzip.open(out/'frontier.jsonl.gz','wt')
    def savecert(node,kind,depth,**extra):
        nonlocal cert_mass,cert_count,max_cert_depth
        cert_mass+=node.weight;cert_count+=1;max_cert_depth=max(max_cert_depth,depth)
        certfile.write(json.dumps(encode(node,kind,**extra),separators=(',',':'))+'\n')
    while heap and expanded<max_nodes:
        _,__,node=heapq.heappop(heap)
        assert node.u%2==1
        if node.path and node.u<=node.M:
            savecert(node,'exact',len(node.path));continue
        if len(node.path)>=max_depth:
            depth_mass+=node.weight;depth_count+=1
            frontierfile.write(json.dumps(encode(node,'depth'))+'\n');continue
        expanded+=1
        for odd in (0,1):
            par=fix_parity(node,odd)
            upper=F(5,6) if odd else F(3,2)
            if par.u*upper.numerator<=par.M*upper.denominator:
                savecert(par,'parity_bound',len(node.path)+1,odd=odd);continue
            for child,tail in least_prime_children(par,odd,primes):
                if child is not None:
                    if child.u<=child.M:
                        savecert(child,'exact',len(child.path))
                    else:
                        heapq.heappush(heap,(-float(child.weight),next(serial),child))
                else:
                    assert tail is not None
                    bound=F(nxt+2,2*nxt) if odd else F(3,2)
                    if tail.u*bound.numerator<=tail.M*bound.denominator:
                        savecert(tail,'tail_bound',len(tail.path)+1,odd=odd,next_prime=nxt)
                    else:
                        tail_mass+=tail.weight;tail_count+=1
                        frontierfile.write(json.dumps(encode(tail,'prime_tail',odd=odd,next_prime=nxt))+'\n')
        if expanded%1000==0:
            record={'expanded':expanded,'certified_density':float(cert_mass),
                    'prime_tail_density':float(tail_mass),'heap_nodes':len(heap),
                    'seconds':round(time.perf_counter()-t0,3)}
            checkpoints.append(record);print(json.dumps(record),flush=True)
    heap_mass=F(0)
    for _,__,node in heap:
        heap_mass+=node.weight
        frontierfile.write(json.dumps(encode(node,'node_frontier'))+'\n')
    certfile.close();frontierfile.close()
    assert cert_mass+tail_mass+depth_mass+heap_mass==1
    total={'prime_max':prime_max,'next_prime':nxt,'max_nodes':max_nodes,
           'max_depth':max_depth,'expanded':expanded,'certificates':cert_count,
           'certificate_max_steps':max_cert_depth,
           'certified_density':float(cert_mass),
           'exact_certified_density':[str(cert_mass.numerator),str(cert_mass.denominator)],
           'prime_tail_density':float(tail_mass),'prime_tail_families':tail_count,
           'depth_frontier_density':float(depth_mass),'depth_frontier_families':depth_count,
           'node_frontier_density':float(heap_mass),'node_frontier_families':len(heap),
           'mass_partition_exactly_one':True,
           'elapsed_seconds':time.perf_counter()-t0,'checkpoints':checkpoints}
    (out/'summary.json').write_text(json.dumps(total,indent=2)+'\n')
    print(json.dumps(total),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prime-max',type=int,default=97)
    p.add_argument('--max-nodes',type=int,default=10000)
    p.add_argument('--max-depth',type=int,default=20)
    p.add_argument('--out',type=Path,default=Path('exact_cover'))
    a=p.parse_args();run(a.prime_max,a.max_nodes,a.max_depth,a.out)
