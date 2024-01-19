from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CaseTask, CaseObservable, Alert, AlertArtifact
from thehive4py.query import *

from config.config import *
from LLM.Create_Description import * 


# 종류별로 가능한 analysis에서 전부 분석 실행
# Cortex에서 각 아티팩트에 대한 분석 실행
# Cortex API 연결
# TheHive
hive_url = 'http://127.0.0.1:9000'
hive_api_key = hive_api_key

# TheHive API 연결
hive_api = TheHiveApi(hive_url, hive_api_key)

def Update_Description(case_id, Threat_Info=None, Bert_Report=None, Cortex_Report=None, Human_Report=None):

    Threat_Info = Threat_Info
    Bert_Report = Bert_Report
    Cortex_Report = Cortex_Report
    Human_Report = Human_Report

    report = Create_Description(Threat_Info, Bert_Report, Cortex_Report, Human_Report)

    '''
    case = Case(
        title='[Phishing Detection] ' + email_alert_data['subject'],
        description=report,
        severity=email_alert_data["severity"],
        tags=['phishing', 'email'],
        tlp=email_alert_data["tlp"],
        pap=email_alert_data["pap"],
        flag=True,
        # tasks=[{'title': 'Initial Analysis'}] # 태스트는 나중에 생성
    )
    '''

    print("전달된 id",case_id)
    case=hive_api.get_case(case_id)
    case.description = report
    case.id = case_id
    print("가지고온 case",case)
    response = hive_api.update_case(case, fields=["description"])

    # 응답 처리
    if response.status_code == 200:
        return f"Case with ID: {case_id} has been updated successfully."
    else:
        return f"Error updating case: {response.text}"
