from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CaseTask, CaseObservable, Alert, AlertArtifact
from thehive4py.query import *

from cortex4py.api import Api
from cortex4py.query import *
from config.config import *
import json
import time
# 종류별로 가능한 analysis에서 전부 분석 실행
# Cortex에서 각 아티팩트에 대한 분석 실행
# Cortex API 연결
# TheHive
hive_url = 'http://127.0.0.1:9000'
hive_api_key = hive_api_key

cortex_url = 'http://127.0.0.1:9001'
cortex_api_key = cortex_api_key

Analyzer_List2={"ip":["AbuseIPDB_1_0", "OTXQuery_2_0", "TalosReputation_1_0", "Shodan_Host_History_1_0"], 
               "hash":["VirusTotal_DownloadSample_3_1", "VirusTotal_Rescan_3_1", "Virusshare_2_0", "HybridAnalysis_GetReport_1_0"], 
               "url":["GoogleSafebrowsing_2_0", "Urlscan_io_Search_0_1_1", "PhishTank_CheckURL_2_1", "CuckooSandbox_Url_Analysis_1_2"], 
               "fqdn":["DomainTools_Risk_2_0","Robtex_Forward_PDNS_Query_1_0", "Splunk_Search_Domain_FQDN_3_0", "Zscaler_1_3"]}

Analyzer_List={"ip":["AbuseIPDB_1_0"], 
               "hash":["VirusTotal_GetReport_3_1"], 
               "url":["Urlscan_io_Search_0_1_1"], 
               "fqdn":["DomainTools_Risk_2_0"]}

# TheHive API 연결
hive_api = TheHiveApi(hive_url, hive_api_key)
cortex_api = Api(cortex_url, cortex_api_key)

# Report 생성 및 TheHive Case 업데이트 함수
def Create_Report(case_id, report):

    # TheHive case에 responder report를 작성
    response = hive_api.run_responder(case_id, report)
    if response.status_code == 200:
        print(f"Successfully added report to case {case_id}")
    else:
        print("Failed to add report to case")

def Cortex_Analysis(case_id, artifacts):
    threshold = 0
    reports=[]
    for artifact in artifacts:        
        analyzers = cortex_api.analyzers.find_all({}, range='all')
        for analyzer in analyzers:
            print('Analyzer {} is enabled'.format(analyzer.name))

        target_analyzers = cortex_api.analyzers.get_by_type(artifact.dataType)


        if target_analyzers:
            analyzer_id = analyzers[0].id
            print(f"Running analyzer with id: {analyzer_id} and data: {artifact.data}")
            job = cortex_api.analyzers.run_by_id(analyzer_id,  {
            'data': artifact.data,
            'dataType': artifact.dataType,
            'tlp': artifact.tlp
            }, force=1)
            print(f"Analyzer job started for {artifact.dataType}: {job.id}")

            while True:
                job = cortex_api.jobs.get_by_id(job.id)
                status = job.json().get("status","")

                if status == "Success":
                    print("Analyzer 작업 완료")
                    result = cortex_api.jobs.get_report(job.id)
                    print("결과입니다.", result.report)
                    break
                elif status == "Failure":
                    print("Analyzer 작업 실패")
                    break
                elif status == "Waiting":
                    print("Analyzer 작업 대기 중...")
                    time.sleep(10)  # 10초 대기 후 다시 확인
                else:
                    print(f"알 수 없는 작업 상태: {status}")
                    break
            

            print("report 결과입니다.", result.report)
            if result:
                report = {
                    'message': f"Analysis report for {artifact.dataType}",
                    'data': result.json()
                }
                reports.append(report)

                print(result.json())
                if int(result.report["full"]["indicator"]["total"])!=0:
                    threshold=1
                    break
                else:
                    continue

            ## 시간남으면 Hive에 다가 Reponders_Reports 추가
             # update_case_with_report(case_id, json.dumps(report, indent=4))
        else:
            print(f"No analyzer found for {artifact.dataType}")

    return threshold, reports
