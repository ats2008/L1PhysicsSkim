# Import HLT configuration #
from data import *

# STEAM Customization #

# Options
nEvents=500          # number of events to process
#switchL1PS=False       # apply L1 PS ratios to switch to tighter column
#columnL1PS=1           # choose the tighter column ( 0 <=> tightest )
outputName="L1.root"  # output file name
#outputName="ZB323778v0_L1_DoubleMu0er2p0_SQ_OS_dEta_Max1pX.root"  # output file name

# Input
from list_cff import inputFileNames
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:/eos/cms/store/group/phys_bphys/athachay/inclusiveDimuonsAtHLT/ZeroBiasL1PhysicsSkim/zb_323778_v0/L1_262.root'),
    #fileNames = cms.untracked.vstring('file:/eos/cms/store/group/phys_bphys/athachay/inclusiveDimuonsAtHLT/ZeroBiasL1PhysicsSkim/zb_323778_v0/ZB323778v0.root'),
    fileNames = cms.untracked.vstring(inputFileNames),
    inputCommands = cms.untracked.vstring('keep *')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( nEvents )
)

# L1 customizations
#from HLTrigger.Configuration.common import *
#import itertools

def insert_modules_after(process, target, *modules):
    "Add the `modules` after the `target` in any Sequence, Paths or EndPath that contains the latter."                                                      
    for sequence in itertools.chain(
        process._Process__sequences.itervalues(),
        process._Process__paths.itervalues(),
        process._Process__endpaths.itervalues()
    ):                                                                                                                                                      
        try:
            position = sequence.index ( target )
        except ValueError:
            continue
        else:
            for module in reversed(modules):
                sequence.insert(position+1, module)

#       Run3  Seeds
# https://indico.cern.ch/event/1099590/contributions/4626725/attachments/2355890/4023767/TriggerReview_L1Menu_Baseline_November30_Heikkilae.pdf

# 34  L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6 
# 36  L1_DoubleMuOpen_er1p4_OS_dEta_Max1p6 
# 37  L1_DoubleMu3er2p0_SQ_OS_dR_Max1p4   

# 67  L1_TripleMu_2_1p5_0OQ_Mass_Max_15
# 68  L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max_15

# 200 L1_DoubleEG10p5er1p22_dR_0p6
# 201 L1_DoubleEG10er1p22_dR_0p6

# 202 L1_DoubleEG9p5er1p22_dR_0p6
# 203 L1_DoubleEG9er1p22_dR_0p7
# 204 L1_DoubleEG8p5er1p22_dR_0p7
# 211 L1_DoubleEG8er1p22_dR_0p7
# 216 L1_DoubleEG7p5er1p22_dR_0p7
# 219 L1_DoubleEG7er1p22_dR_0p8
# 220 L1_DoubleEG6p5er1p22_dR_0p8
# 221 L1_DoubleEG6er1p22_dR_0p8
# 222 L1_DoubleEG5p5er1p22_dR_0p8
# 223 L1_DoubleEG5er1p22_dR_0p9

#       2018 Seeds
# https://docs.google.com/spreadsheets/d/1naAH5kMgHau01zoGuwvMu7cmyT_UfRCe3EuiE7SoCK4/edit#gid=259080975

# 44  L1_DoubleMu8_SQ 
# 59  L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4 
# 61  L1_DoubleMu4_SQ_OS_dR_Max1p2  
# 83  L1_TripleMu_5_3p5_2p5_DoubleMu_5_2p5_OS_Mass_5to17 
# 85  L1_TripleMu_5SQ_3SQ_0OQ_DoubleMu_5_3_SQ_OS_Mass_Max9 
# 112 L1_DoubleMu3_OS_DoubleEG7p5Upsilon
# 113 L1_DoubleMu5Upsilon_OS_DoubleEG3

#       2018 Backup Seeds
# 35  L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5 
# 45  L1_DoubleMu9_SQ
# 58  L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4 
# 63  L1_DoubleMu4p5_SQ_OS_dR_Max1p2 
# 65  L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7 
# 66  L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18
# 84  L1_TripleMu_5_4_2p5_DoubleMu_5_2p5_OS_Mass_5to17
# 86  L1_TripleMu_5SQ_3SQ_0_DoubleMu_5_3_SQ_OS_Mass_Max9

process.L1PhysicsFilter = cms.EDFilter("L1PhysicsFilter",
             hltProcess = cms.string("HLT2"),
    L1ObjectMapInputTag = cms.InputTag("simGtStage2ObjectMap"),
    #TriggerBitsToCheck  = cms.vint32(34,36,37,67,68,200,201,202,203,204,211,216,219,220,221,222,223,44,59,61,83,85,112,113,35,45,58,63,65,66,84,86) ,
    #TriggerBitsToCheck  = cms.vint32(34,36,37,67,68,44,59,61,83,85,112,113,35,45,58,63,65,66,84,86) ,
    TriggerBitsToCheck  = cms.vint32(200,201,202,203,204,211,216,219,220,221,222,223) ,
    ugtToken = cms.InputTag("simGtStage2Digis")
                                       )
process.l1filter_step = cms.Path(process.L1PhysicsFilter)
process.schedule.append(process.l1filter_step)


process.hltOutputTriggerResults = cms.OutputModule( "PoolOutputModule",
        fileName = cms.untracked.string(outputName),
        SelectEvents = cms.untracked.PSet( 
        SelectEvents = cms.vstring("l1filter_step")
        ),
        outputCommands = cms.untracked.vstring('drop *',
                                        'keep *',
                               # 'keep *_*_*_HLT',
                               # 'keep *_*_*_LHC'
                                )
      )
process.l1filteroutput = cms.EndPath(process.hltOutputTriggerResults)
process.schedule.append(process.l1filteroutput)

#process.TriggerMenu = cms.ESProducer("L1TUtmTriggerMenuESProducer",
#    #L1TriggerMenuFile = cms.string('L1Menu_Collisions2022_v0_1_2.xml')
#    L1TriggerMenuFile = cms.string('L1Menu_Collisions2022_v0_1_1_Bmumu_opt1.xml')
#)

print(process.schedule)


