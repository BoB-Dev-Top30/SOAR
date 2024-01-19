from  .Cortex_Analysis import Cortex_Analysis
from .Bert_Analysis import Bert_Analysis

# 분석 결과에서 임계치 추출 및 판별해서 main으로 보내줌
# threat_intelligence기반에서는 어떤 분석기에서 하나라도 1이면 자동차단, 아니면 인간분석필요(새로운 유형의 악성코드)

# AI가 75%가 넘는 확률로 텍스트자체에서 이상을 감지하면 관련내용이 참조됨



def Analysis_Frame(email_analysis_data, case_id, artifacts):
    
    # 만약 
    AI_Results, AI_Info = Bert_Analysis(email_analysis_data["text"]) # 1 vs 0 AI가,  75퍼 넘어서 잡으면 1이됨
    
    Cortex_Results, Cortex_Info = Cortex_Analysis(case_id, artifacts) # 하나라도 1이면 1과 관련정보 return

    if(Cortex_Results==1):
        print("분석도구가 위험을 찾았습니다.")

        return "Cortex Found", Cortex_Info

    elif(Cortex_Results==0 and AI_Results==1):
        print("자체 모델이 텍스트에서 수상함을 찾았습니다.")

        return "Bert Found", AI_Info
    elif(Cortex_Results==1 and AI_Results==1):
        print("자체 모델과 분석도구가 위험을 찾았습니다.")
        
        return "Bert & Cortex Found", AI_Info +"///////"+Cortex_Info # 한번에 리턴하기 위한 구분자
    else:
        print("분석가의 도움이 필요합니다.")

        return "Need Analyst"