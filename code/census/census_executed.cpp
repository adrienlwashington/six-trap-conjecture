// Six Trap census. C++17, standard library only.
// T(n)=n+D(n)-D(n+1), D(n)=n/least_prime_factor(n), n>=2.
// Cycles are discovered, never preloaded. Exact arithmetic only.
// Run: ./census UPPER OUTPUT_DIRECTORY [full|compact]
// In compact mode per-seed peaks are omitted, but global peak and ratio
// records remain exact: a reused tail occurred at an earlier, smaller seed.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using u64=uint64_t; using u32=uint32_t; using u16=uint16_t; using u8=uint8_t;
static constexpr u64 VALUE_CAP=10000000000000000ULL;
static constexpr size_t PATH_CAP=100000;
static constexpr u32 PRIME_LIMIT=10000000;
struct Cycle { u64 minimum,maximum; std::vector<u64> states; u64 count=0, steps_sum=0, max_steps=0, max_seed=0; };
struct Record { u64 seed,value,cycle_min=0; };
class LeastFactor {
    u64 bound; std::vector<u16> odd_spf; std::vector<u32> primes;
public:
    u64 sieve_calls=0, trial_calls=0, trial_divisions=0;
    explicit LeastFactor(u64 b):bound(b),odd_spf(b/2+1,0) {
        if(b>4000000000ULL) throw std::runtime_error("sieve bound exceeds supported uint16 SPF domain");
        for(u64 p=3;p<=b/p;p+=2) if(!odd_spf[p/2]) {
            for(u64 x=p*p;x<=b;x+=2*p) if(!odd_spf[x/2]) odd_spf[x/2]=(u16)p;
        }
        std::vector<bool> composite(PRIME_LIMIT+1,false);
        for(u32 p=2;p<=PRIME_LIMIT;p++) {
            if(!composite[p]) {
                primes.push_back(p);
                if((u64)p*p<=PRIME_LIMIT) for(u64 j=(u64)p*p;j<=PRIME_LIMIT;j+=p) composite[j]=true;
            }
        }
    }
    u64 operator()(u64 n) {
        if(n<2) throw std::runtime_error("least factor requested below 2");
        if((n&1)==0) return 2;
        if(n<=bound) {++sieve_calls; u64 p=odd_spf[n/2];return p?p:n;}
        ++trial_calls;
        for(u32 p:primes) {
            if(p==2) continue;
            if((u64)p>n/p) return n;
            ++trial_divisions;
            if(n%p==0) return p;
        }
        // Continue exact trial division above the precomputed prime list if needed.
        for(u64 d=(u64)PRIME_LIMIT+1;d<=n/d;d+=2) {
            ++trial_divisions;
            if(n%d==0) return d;
        }
        return n;
    }
};
int main(int argc,char**argv) {
    u64 N=0,completed=0,current_seed=0; std::filesystem::path out;
    try {
        if(argc<3 || argc>4) throw std::runtime_error("usage: census UPPER OUTPUT_DIR [full|compact]");
        size_t used=0; N=std::stoull(argv[1],&used);
        if(used!=std::string(argv[1]).size() || N<2 || N>2000000000ULL) throw std::runtime_error("UPPER must be 2..2,000,000,000");
        out=argv[2];std::filesystem::create_directories(out);
        bool full=argc<4 || std::string(argv[3])=="full";
        if(argc==4 && std::string(argv[3])!="full" && std::string(argv[3])!="compact") throw std::runtime_error("invalid mode");
        auto begin=std::chrono::steady_clock::now();
        std::cerr<<"Building exact least-factor sieve through "<<N+1<<"\n";
        LeastFactor factor(N+1);
        // Packed state: 4 label bits + 12 distance bits, using two bytes per seed.
        // Labels: 0 unknown, 15 active, 1..14 discovered cycles.
        // All capacity/overflow limits fail closed; no truncated classifications.
        std::vector<u16> packed(N+1,0);
        auto label=[&](u64 n)->u8{return (u8)(packed[n]&15);};
        auto distance=[&](u64 n)->u16{return (u16)(packed[n]>>4);};
        auto assign=[&](u64 n,u8 id,u64 dist){
            if(id>15 || dist>=4096) throw std::runtime_error("packed state capacity exceeded; incomplete");
            packed[n]=(u16)((dist<<4)|id);
        };
        std::vector<u64> height; if(full) height.resize(N+1,0);
        std::vector<Cycle> cycles;
        std::vector<u64> path;path.reserve(1024);
        std::unordered_map<u64,size_t> active_high;
        std::vector<Record> step_records,peak_records,ratio_records;
        u64 calls=0,max_value=0,max_value_seed=0,max_steps=0,max_steps_seed=0;
        u64 ratio_peak=0,ratio_seed=1,total_steps=0,neighbor_changes=0;
        std::vector<u64> histogram(1,0);u8 previous=0;
        // CSVs store direct edge witnesses for discovered cycles and record trajectories.
        auto step=[&](u64 n)->u64 {
            if(n<2 || n>VALUE_CAP) throw std::runtime_error("value cap/domain violation");
            ++calls;
            // Exact parity simplification: the even argument has least factor 2.
            u64 r=(n&1)?(n-1)/2+n/factor(n):n+n/2-(n+1)/factor(n+1);
            if(r<2 || r>VALUE_CAP) throw std::runtime_error("next value cap/domain violation");
            return r;
        };
        auto note_value=[&](u64 n,u64 seed) {
            if(n>max_value) {max_value=n;max_value_seed=seed;}
            if((__uint128_t)n*ratio_seed>(__uint128_t)ratio_peak*seed) {ratio_peak=n;ratio_seed=seed;}
        };
        std::cerr<<"Sieve ready; classifying consecutive seeds\n";
        for(u64 seed=2;seed<=N;seed++) {
            current_seed=seed;
            u64 old_peak=max_value,old_ratio_peak=ratio_peak,old_ratio_seed=ratio_seed;
            note_value(seed,seed);
            if(!label(seed)) {
                path.clear();active_high.clear();u64 n=seed;
                u8 tail_id=0;u64 tail_dist=0,tail_height=0;
                while(true) {
                    note_value(n,seed);
                    if(n<=N && label(n)!=0 && label(n)!=15) {
                        tail_id=label(n);tail_dist=distance(n);if(full)tail_height=height[n];break;
                    }
                    size_t cycle_at=std::numeric_limits<size_t>::max();
                    if(n<=N && label(n)==15) {
                        auto it=std::find(path.begin(),path.end(),n);
                        if(it==path.end()) throw std::runtime_error("active marker inconsistent");
                        cycle_at=it-path.begin();
                    } else if(n>N) {
                        auto it=active_high.find(n);if(it!=active_high.end())cycle_at=it->second;
                    }
                    if(cycle_at!=std::numeric_limits<size_t>::max()) {
                        if(cycles.size()>=14) throw std::runtime_error("cycle label capacity exceeded; incomplete");
                        std::vector<u64> members(path.begin()+cycle_at,path.end());
                        auto mi=std::min_element(members.begin(),members.end());
                        std::rotate(members.begin(),mi,members.end());
                        u64 high=*std::max_element(members.begin(),members.end());
                        cycles.push_back({members.front(),high,members});
                        tail_id=(u8)cycles.size();tail_dist=0;tail_height=high;
                        for(u64 x:members) if(x<=N) {assign(x,tail_id,0);if(full)height[x]=high;}
                        path.resize(cycle_at);break;
                    }
                    if(path.size()>=PATH_CAP) throw std::runtime_error("active path cap reached; incomplete");
                    if(n<=N)assign(n,15,0);else active_high[n]=path.size();
                    path.push_back(n);n=step(n);
                }
                while(!path.empty()) {
                    u64 x=path.back();path.pop_back();
                    ++tail_dist;
                    if(tail_dist>=4096) throw std::runtime_error("distance storage limit reached; incomplete");
                    if(full)tail_height=std::max(tail_height,x);
                    if(x<=N) {assign(x,tail_id,tail_dist);if(full)height[x]=tail_height;}
                }
            }
            if(label(seed)==0 || label(seed)==15) throw std::runtime_error("seed left unclassified");
            auto &c=cycles.at(label(seed)-1);u64 d=distance(seed);
            ++c.count;c.steps_sum+=d;total_steps+=d;
            if(d>c.max_steps){c.max_steps=d;c.max_seed=seed;}
            if(d>max_steps){max_steps=d;max_steps_seed=seed;step_records.push_back({seed,d,c.minimum});}
            if(max_value>old_peak)peak_records.push_back({seed,max_value,c.minimum});
            if((__uint128_t)ratio_peak*old_ratio_seed>(__uint128_t)old_ratio_peak*ratio_seed)ratio_records.push_back({seed,ratio_peak,c.minimum});
            if(d>=histogram.size()) histogram.resize(d+1,0);
            ++histogram[d];
            if(previous && previous!=label(seed)) ++neighbor_changes;
            previous=label(seed);++completed;
            if(seed%10000000==0 || seed==N) {
                double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count();
                std::cerr<<"completed_through="<<seed<<" cycles="<<cycles.size()<<" max_steps="<<max_steps<<" peak="<<max_value<<" seconds="<<elapsed<<"\n";
            }
        }
        auto end=std::chrono::steady_clock::now();double elapsed=std::chrono::duration<double>(end-begin).count();
        std::vector<size_t> order(cycles.size());std::iota(order.begin(),order.end(),0);
        std::sort(order.begin(),order.end(),[&](size_t a,size_t b){return cycles[a].minimum<cycles[b].minimum;});
        std::ofstream basin(out/"basins.csv");basin<<"cycle_minimum,period,cycle_maximum,seed_count,total_steps_to_cycle,max_steps_to_cycle,first_seed_at_max_steps\n";
        std::ofstream cy(out/"cycles.csv");cy<<"cycle_minimum,position,n,next_n\n";
        for(auto i:order){auto &c=cycles[i];basin<<c.minimum<<','<<c.states.size()<<','<<c.maximum<<','<<c.count<<','<<c.steps_sum<<','<<c.max_steps<<','<<c.max_seed<<'\n';for(size_t j=0;j<c.states.size();j++)cy<<c.minimum<<','<<j<<','<<c.states[j]<<','<<c.states[(j+1)%c.states.size()]<<'\n';}
        auto save_records=[&](const std::string&name,const std::vector<Record>&rs){std::ofstream f(out/name);f<<"seed,value,cycle_minimum\n";for(auto r:rs)f<<r.seed<<','<<r.value<<','<<r.cycle_min<<'\n';};
        save_records("stopping_time_records.csv",step_records);save_records("peak_records.csv",peak_records);save_records("excursion_ratio_records.csv",ratio_records);
        std::ofstream hi(out/"stopping_time_histogram.csv");hi<<"steps_to_first_cycle_entry,seed_count\n";for(size_t i=0;i<histogram.size();i++)hi<<i<<','<<histogram[i]<<'\n';
        // Save deterministic verification targets, including all first record seeds.
        std::vector<u64> targets={2,N};for(u64 x=2;x<=std::min<u64>(N,100000);x++)targets.push_back(x);
        u64 rng=0xD20260924ULL;for(int i=0;i<20000;i++){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;targets.push_back(2+rng%(N-1));}
        for(auto r:step_records) targets.push_back(r.seed);
        for(auto r:peak_records) targets.push_back(r.seed);
        for(auto r:ratio_records) targets.push_back(r.seed);
        std::sort(targets.begin(),targets.end());targets.erase(std::unique(targets.begin(),targets.end()),targets.end());
        std::ofstream samples(out/"verification_targets.csv");samples<<"seed,cycle_minimum,steps_to_cycle,peak_or_zero_if_not_stored\n";for(u64 x:targets)samples<<x<<','<<cycles[label(x)-1].minimum<<','<<distance(x)<<','<<(full?height[x]:0)<<'\n';
        std::ofstream js(out/"summary.json");js<<std::setprecision(17);
        js<<"{\n  \"status\":\"complete\",\n  \"seed_start\":2,\n  \"seed_end\":"<<N<<",\n  \"requested_seed_count\":"<<N-1<<",\n  \"completed_seed_count\":"<<completed<<",\n  \"unclassified_seed_count\":0,\n  \"cycles_found\":"<<cycles.size()<<",\n  \"map_evaluations_before_tail_reuse\":"<<calls<<",\n  \"sum_of_individual_steps_to_cycle\":"<<total_steps<<",\n  \"maximum_steps_to_first_cycle_entry\":"<<max_steps<<",\n  \"first_seed_at_maximum_steps\":"<<max_steps_seed<<",\n  \"maximum_orbit_value\":"<<max_value<<",\n  \"first_seed_attaining_maximum_orbit_value\":"<<max_value_seed<<",\n  \"maximum_excursion_ratio_numerator\":"<<ratio_peak<<",\n  \"maximum_excursion_ratio_denominator\":"<<ratio_seed<<",\n  \"adjacent_seed_pairs_with_different_attractors\":"<<neighbor_changes<<",\n  \"adjacent_seed_pairs\":"<<N-2<<",\n  \"classification_wall_seconds_including_sieve\":"<<elapsed<<",\n  \"factor_sieve_calls\":"<<factor.sieve_calls<<",\n  \"factor_trial_calls\":"<<factor.trial_calls<<",\n  \"trial_divisions\":"<<factor.trial_divisions<<",\n  \"value_cap\":"<<VALUE_CAP<<",\n  \"active_path_cap\":"<<PATH_CAP<<",\n  \"distance_cap_exclusive\":4096,\n  \"cap_hits\":0,\n  \"full_per_seed_height_cache\":"<<(full?"true":"false")<<",\n  \"verification_targets\":"<<targets.size()<<",\n  \"cycle_minima\":[";
        for(size_t k=0;k<order.size();k++){if(k)js<<',';js<<cycles[order[k]].minimum;}js<<"]\n}\n";
        if(!js || !basin || !cy || !samples)throw std::runtime_error("output write failure");
        std::cout<<"COMPLETE "<<completed<<" seeds, "<<cycles.size()<<" cycles, "<<elapsed<<" s\n";
        return 0;
    } catch(const std::exception&e) {
        std::cerr<<"INCOMPLETE: "<<e.what()<<" current_seed="<<current_seed<<" completed="<<completed<<"\n";
        if(!out.empty()){std::ofstream f(out/"failure.txt");f<<"INCOMPLETE\n"<<e.what()<<"\nrequested_upper="<<N<<"\ncompleted_seed_count="<<completed<<"\ncurrent_seed="<<current_seed<<'\n';}
        return 2;
    }
}
