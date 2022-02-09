//         Created:  Wed, 15 Dec 2021 17:36:13 GMT
//         Original Author: Sanu Varghese
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include<vector>
#include "CondFormats/DataRecord/interface/L1TUtmTriggerMenuRcd.h"
#include "CondFormats/L1TObjects/interface/L1TUtmTriggerMenu.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMapFwd.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMap.h"
#include "DataFormats/L1TGlobal/interface/GlobalObjectMapRecord.h"
#include "DataFormats/L1TGlobal/interface/GlobalObject.h"

// class declaration
//

class L1PhysicsFilter : public edm::stream::EDFilter<> {
private:
    
  std::string hltProcess_; //name of HLT process, usually "HLT"
  
public:
  explicit L1PhysicsFilter(const edm::ParameterSet&);
  ~L1PhysicsFilter(){};

  //  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginRun(const edm::Run& ,const edm::EventSetup& ) override;
  //virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;
  //GlobalAlgBlk const *results_;
  
  /// InputTag for L1 Global Trigger object maps. This is done per menu. Should be part of Run.
  const edm::EDGetTokenT<GlobalAlgBlkBxCollection> ugt_token_;
    std::vector<int> tVector;
    std::vector<size_t> triggerVector;
};
L1PhysicsFilter::L1PhysicsFilter(const edm::ParameterSet& iConfig):
  hltProcess_(iConfig.getParameter<std::string>("hltProcess")),
  ugt_token_(consumes<GlobalAlgBlkBxCollection>(iConfig.getParameter<edm::InputTag>("ugtToken"))),
  tVector(iConfig.getParameter<vector<int>>("TriggerBitsToCheck"))
{
    for(auto &i : tVector)
    {
            triggerVector.push_back(i);
            std::cout<<"Has trigger bit : "<<i<<"\n";
    }
}

void L1PhysicsFilter::beginRun(const edm::Run& run,const edm::EventSetup& setup)
{

}
//bool L1PhysicsFilter::filter(edm::Event const &event, edm::EventSetup const &setup) { 
bool L1PhysicsFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)  {

  // using namespace edm;
  bool passEvents = false;
  //unsigned long long id = iSetup.get<L1TUtmTriggerMenuRcd>().cacheIdentifier();
  // if (id != cache_id_) {
  //   cache_id_ = id;
  //   edm::ESHandle<L1TUtmTriggerMenu> menu;
  //  iSetup.get<L1TUtmTriggerMenuRcd>().get(menu);
  edm::Handle<GlobalAlgBlkBxCollection> ugt;
  iEvent.getByToken(ugt_token_, ugt);


  const GlobalAlgBlk* L1uGT(nullptr);
    if (ugt.isValid()) {
    L1uGT = &ugt->at(0, 0);
    //cout<<"The ugtValid is working"<<endl;
  }
  //  }
  //GlobalAlgBlk* L1uGT = new GlobalAlgBlk();

  //bool passEvents = false;
    if(L1uGT != 0){
      //cout<<"The pointer is working"<<endl;
      std::vector<bool> m_algoDecisionFinal = L1uGT->getAlgoDecisionFinal();
      // // cout<<m_algoDecisionFinal<<endl;
      for(size_t s = 0; s < m_algoDecisionFinal.size(); s++){
	//   //  cout<<m_algoDecisionFinal[s]<<endl;
	if(s<458)
   for(size_t k=0;k<triggerVector.size();k++) {
      if( (s== triggerVector[k])  and (m_algoDecisionFinal[s] > 0) ){
	  passEvents = true;
	  cout<<" SUCESS !! for "<<triggerVector[k]<<" "<<s<<endl; 
	    }
     }
        if(passEvents) break;
    }          
   }
   return passEvents;

}

  
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
DEFINE_FWK_MODULE(L1PhysicsFilter);
