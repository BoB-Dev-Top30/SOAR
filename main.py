from HIVE.Alert_Phishing import *
from HIVE.Create_Case import *
from HIVE.Create_Tasks import *
from HIVE.Update_Description import *
from thehive4py.models import Case, CaseObservable
from Analysis.Analysis_Frame import *

from External_Modules.Send_Email import *

import json

import tkinter as tk
from tkinter import messagebox

from config.config import *


# 이메일 보안 시스템에서 받은 데이터 (예시)

## Bert가 판별할 데이터
email_normal_data = {
    "ip": "60.10.3.4", # ip
    "subject": "수상한 텍스트", # 제목
    "attachment": "제출용.hwp", # 파일이름
    "text" : "광고 대*박*행*운!",
    "hash" : "", # 파일 해시값
    "url": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php", # URL
    "fqdn":"",
    "severity": 1,
    "tlp":1,
    "pap":1,
}

email_MaliciousFile_data = {
    "ip": "80.34.3.8", # ip
    "subject": "수상한 파일첨부", # 제목
    "attachment": "제출용.hwp", # 파일이름
    "text" : "abc",
    "hash" : "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", # 파일 해시값
    "url": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php", # URL
    "fqdn" : "www.naverr.com",
    "severity": 3,
    "tlp":3,
    "pap":3,
}

email_MaliciousUrl_data = {
    "ip": "10.50.46.65", # ip
    "subject": "수상한 url", # 제목
    "attachment": "", # 파일이름
    "text" : "",
    "hash" : "", # 파일 해시값
    "url": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php", # URL
    "fqdn" : "",
    "severity": 2,
    "tlp":2,
    "pap":2,
}

file_path = "C:/Users/scw10/OneDrive/바탕 화면/탑30/한주성멘토/0113/Suspicious_File/제출용.hwp"  # 첨부할 파일의 경로



block_list=[{
    "ip": "80.34.3.8", # ip
    "text" : "abc",
    "hash" : "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", # 파일 해시값
    "url": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php", # URL
    "fqdn" : "www.naverr.com",
}]

charger_mail_list=["sirius5b8b@gmail.com"]



data = email_MaliciousFile_data
data2 = email_normal_data


def SOAR(data):
# artifacts는  나중에 Cortex_Analysis에 쓰일거임
    alert_result, artifacts = Alert_Phishing(data) 

    if(alert_result == "Alert created in The Hive"):
        case, case_id = Create_Case(data, file_path) # id 값 저장 나중에 Tasks 생성에 쓰임
        block_list_result=0

        ## 기존에 가지고 있는 차단 DB값에 쿼리(현재는 일단 리스트)
        for i in block_list:
            if(i["ip"]== data["ip"] and i["text"]==data["text"] and i["hash"]==data["hash"] and i["url"]==data["url"] and i["fqdn"]==data["fqdn"]):
                block_list_result=1

        if(block_list_result==1):    
            ## 만약 똑같은 값 있다면, case_result(id)에 Task1 생성
            print("이미 리스트에 차단리스트가 존재합니다.\n")
            task_result = Create_Task1(case_id)
            print(task_result)
            Human_Report =  "이미 차단 리스트가 존재하였지만, 보안제품이 차단하지 못하였습니다."
            Threat_Info = data
            Update_Description(case_id, Threat_Info, Human_Report)
            print("Case가 종료되었습니다.\n")

        ## 만약 값이 하나라도 다르면(DB에 없으면)
        else:    
            Analysis_Result, Info =  Analysis_Frame(data, case_id, artifacts)
            
            # Cortex 혼자 찾았다면
            if(Analysis_Result=="Cortex Found"):
                # 1 IP차단  띄움
                print("IP를 차단합니다.")            
                
                # 2 리스트에 해당값 INSERT -> 추후 DB로 수정
                block_list.append(data)

                # 3 태스크 생성
                Create_Task3(case_id)

                # 4 Description 생성
                Threat_Info = data
                Cortex_Report = Info
                Update_Description(case_id, Threat_Info, None, Cortex_Report, Human_Report)
                print("Case가 종료되었습니다.\n")

            elif(Analysis_Result=="Bert & Cortex Found"):

                # 1 IP차단 간지나게 띄우는 척 하는거 띄움
                print("IP를 차단합니다.")            
                
                # 2 리스트에 해당값 INSERT -> 추후 DB로 수정
                block_list.append(data)

                # 3 태스크 생성
                Create_Task3(case_id)

                Cortex_Report, Bert_Report = Info.split("///////") # 구분에서 2개로 쪼개기
                Threat_Info = data
                # 4 Description 생성
                Update_Description(case_id, Threat_Info, Bert_Report, Cortex_Report, Human_Report)
                print("Case가 종료되었습니다.\n")
            
            # BERT 혼자 찾았다면
            elif(Analysis_Result=="Bert Found"):   
                print("분석가들의 도움이 필요합니다.")

                # 1> 분석가들에게 메일 보냄
                for charger in charger_mail_list:
                    Send_Email('sirius5b8b@gmail.com', google_pwd, charger, 'Need Analyst!', f'분석이 필요합니다. case{case_id}를 확인해주시고 Task를 수행하세요!\n')

                # 2> 태스크2 생성
                Create_Task2(case_id)

                # 3> 정오탐 판별
                Is_Malicious = input("분석한 결과는 정탐인가요? 오탐인가요?")

                ### 정탐이면
                if(Is_Malicious=="정탐"):
                    print("IP가 차단되었습니다.")

                ### 정탐이든 오탐이든
                Threat_Info = data
                Human_Report = "분석가가 분석한 결과는 "+Is_Malicious+" 입니다.\n"
                Bert_Report = Info
                Human_Report += input("분석한 정보를 입력해주세요!")
                
                # 4> Description 생성
                Update_Description(case_id, Threat_Info, Bert_Report, None, Human_Report)
                print("case가 종료되었습니다.")

            else:
                # 분석가들에게 메일 보냄
                for charger in charger_mail_list:
                    Send_Email('sirius5b8b@gmail.com', google_pwd, charger, 'Need Analyst!', f'분석이 필요합니다. case{case_id}를 확인해주시고 Task를 수행하세요!\n')

                # 2> 태스크2 생성
                Create_Task2(case_id)

                # 3> 정오탐 판별
                Is_Malicious = input("분석한 결과는 정탐인가요? 오탐인가요?")

                ### 정탐이면
                if(Is_Malicious=="정탐"):
                    print("IP가 차단되었습니다.")

                ### 정탐이든 오탐이든
                Threat_Info = data
                Human_Report = "분석가가 분석한 결과는 "+Is_Malicious+" 입니다.\n"
                Human_Report += input("분석한 정보를 입력해주세요!")
                
                # 4> Description 생성
                Update_Description(case_id, Threat_Info, None, None, Human_Report)
                print("case가 종료되었습니다.")

# SOAR(data) # task1
                
# 예제 데이터는 Cortex는 위협이라고 감지하지 않았지만, AI모델이 위협이라고 판단한 상황!
SOAR(data2) # task2
