import Cortex_Analysis
import Bert_Analysis

# 분석 결과에서 임계치 추출 및 판별해서 main으로 보내줌
# threat_intelligence기반에서는 어떤 분석기에서 하나라도 1이면 자동차단, 아니면 인간분석필요(새로운 유형의 악성코드)

# AI가 75%가 넘는 확률로 텍스트자체에서 이상을 감지하면 관련내용이 참조됨



def Analysis_Frmae(email_analysis_data, case_id, alert, ):
    
    # 만약 
    AI_Analysis = Bert_Analysis(email_analysis_data["text"]) # 1 vs 0 AI가,  75퍼 넘어서 잡으면 1이됨

    if(AI_Analysis==1):
        AI_Info = "자체 모델이 텍스트에서 수상함을 감지하였습니다."
        threshold = Cortex_Analysis(case_id, alert, AI_Info)# [1, 0, 1, 1], 각 분석기에서 하나라도 1이면 1이됨

    else:
        threshold = Cortex_Analysis(case_id, alert)
        
    return threshold