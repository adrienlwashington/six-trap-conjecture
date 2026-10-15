// Independent internal verifier: direct n+D(n)-D(n+1), no factor sieve,
// no parity formula, no preloaded attractors. Trial division by 2,3,6k+-1.
// Checks requested targets and exports complete record-trajectory witnesses.
// Build: g++ -O3 -std=c++17 verify.cpp -o verify
// Run: ./verify INPUT_RUN_DIRECTORY OUTPUT_DIRECTORY
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using U=uint64_t;
struct Info {U minimum,steps,peak;};
std::unordered_map<U,Info> memo;
std::map<U,std::vector<U>> cycles;
U evaluations=0,divisions=0;
U D(U n) {
    if(n<2)throw std::runtime_error("invalid divisor input");
    if(n%2==0)return n/2;
    if(n%3==0)return n/3;
    for(U d=5;d<=n/d;d+=6){
        ++divisions;if(n%d==0)return n/d;
        ++divisions;if(n%(d+2)==0)return n/(d+2);
    }
    return 1;
}
U T(U n){++evaluations;return n+D(n)-D(n+1);}
Info classify(U seed){
    if(auto it=memo.find(seed);it!=memo.end())return it->second;
    std::vector<U> path;std::unordered_map<U,size_t> where;U n=seed;Info tail{};
    while(true){
        if(n<2 || n>10000000000000000ULL || path.size()>=100000)throw std::runtime_error("verifier safety limit; incomplete");
        if(auto it=memo.find(n);it!=memo.end()){tail=it->second;break;}
        if(auto it=where.find(n);it!=where.end()){
            size_t at=it->second;std::vector<U> cyc(path.begin()+at,path.end());
            U lo=*std::min_element(cyc.begin(),cyc.end()),hi=*std::max_element(cyc.begin(),cyc.end());
            std::rotate(cyc.begin(),std::find(cyc.begin(),cyc.end(),lo),cyc.end());
            cycles[lo]=cyc;tail={lo,0,hi};for(U x:cyc)memo[x]=tail;
            path.resize(at);break;
        }
        where[n]=path.size();path.push_back(n);n=T(n);
    }
    for(auto it=path.rbegin();it!=path.rend();it++){++tail.steps;tail.peak=std::max(tail.peak,*it);memo[*it]=tail;}
    return memo.at(seed);
}
std::vector<U> parse(const std::string&s){std::stringstream ss(s);std::string t;std::vector<U> a;while(std::getline(ss,t,','))a.push_back(std::stoull(t));return a;}
int main(int argc,char**argv){try{
    if(argc!=3)throw std::runtime_error("usage: verify INPUT_RUN_DIR OUTPUT_DIR");
    auto start=std::chrono::steady_clock::now();std::filesystem::path in=argv[1],out=argv[2];std::filesystem::create_directories(out);
    std::ifstream f(in/"verification_targets.csv");if(!f)throw std::runtime_error("missing targets");
    std::string line;std::getline(f,line);U checked=0,checked_peaks=0;
    while(std::getline(f,line)){
        auto a=parse(line);if(a.size()!=4)throw std::runtime_error("bad target row");
        Info r=classify(a[0]);
        if(r.minimum!=a[1] || r.steps!=a[2] || (a[3] && r.peak!=a[3])){
            std::ostringstream msg;msg<<"MISMATCH seed "<<a[0]<<" computed "<<r.minimum<<','<<r.steps<<','<<r.peak<<" expected "<<a[1]<<','<<a[2]<<','<<a[3];throw std::runtime_error(msg.str());
        }
        ++checked;if(a[3])++checked_peaks;
    }
    std::set<U> records;
    for(const char* name:{"stopping_time_records.csv","peak_records.csv","excursion_ratio_records.csv"}){
        std::ifstream rf(in/name);if(!rf)throw std::runtime_error("missing records");std::getline(rf,line);
        while(std::getline(rf,line)){
            auto a=parse(line);records.insert(a[0]);Info r=classify(a[0]);
            U got=std::string(name)=="stopping_time_records.csv"?r.steps:r.peak;
            if(got!=a[1] || r.minimum!=a[2])throw std::runtime_error("record witness mismatch at "+std::to_string(a[0]));
        }
    }
    U witness_edges=0;
    std::ofstream ri(out/"record_trajectories_summary.csv");ri<<"seed,cycle_minimum,steps_to_first_cycle_entry,maximum_orbit_value,first_peak_index\n";
    for(U seed:records){
        std::ofstream wf(out/("trajectory_"+std::to_string(seed)+".csv"));wf<<"index,n,D_n,D_n_plus_1,next_n,in_cycle\n";
        U n=seed,index=0,peak_index=0,high=0;std::set<U> seen;
        while(!seen.count(n)){
            seen.insert(n);U dn=D(n),dn1=D(n+1),next=n+dn-dn1;
            if(n>high){high=n;peak_index=index;}
            auto info=classify(n);wf<<index<<','<<n<<','<<dn<<','<<dn1<<','<<next<<','<<(info.steps==0)<<'\n';
            ++witness_edges;++index;n=next;
        }
        Info r=classify(seed);if(high!=r.peak)throw std::runtime_error("witness peak mismatch");
        ri<<seed<<','<<r.minimum<<','<<r.steps<<','<<r.peak<<','<<peak_index<<'\n';
    }
    std::ofstream cf(out/"independently_discovered_cycles.csv");cf<<"cycle_minimum,index,n,next_n\n";
    for(auto&[lo,cyc]:cycles)for(size_t i=0;i<cyc.size();i++){
        U next=T(cyc[i]);if(next!=cyc[(i+1)%cyc.size()])throw std::runtime_error("cycle edge mismatch");
        cf<<lo<<','<<i<<','<<cyc[i]<<','<<next<<'\n';
    }
    double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::ofstream js(out/"verification.json");js<<"{\n  \"status\":\"all_checked_targets_match\",\n  \"checked_seed_classifications\":"<<checked<<",\n  \"checked_per_seed_peaks\":"<<checked_peaks<<",\n  \"independently_discovered_cycles\":"<<cycles.size()<<",\n  \"verified_record_trajectories\":"<<records.size()<<",\n  \"record_witness_edges\":"<<witness_edges<<",\n  \"distinct_memoized_states\":"<<memo.size()<<",\n  \"map_evaluations\":"<<evaluations<<",\n  \"trial_divisions\":"<<divisions<<",\n  \"wall_seconds\":"<<sec<<",\n  \"limitations\":\"Internal independently written implementation; selected targets, not a second full billion-seed census or external review.\"\n}\n";
    std::cout<<"VERIFIED "<<checked<<" targets, "<<records.size()<<" record trajectories, "<<sec<<" seconds\n";
}catch(const std::exception&e){std::cerr<<"VERIFICATION FAILED: "<<e.what()<<'\n';return 2;}}
