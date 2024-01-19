from HIVE.Alert_Phishing import *
from HIVE.Create_Case import *
from HIVE.Create_Tasks import *
from HIVE.Update_Description import *
from thehive4py.models import Case, CaseObservable
# from Analysis.Analysis_Frame import *
# from External_Modules.Mailing import *

import json

import tkinter as tk
from tkinter import messagebox


# 이메일 보안 시스템에서 받은 데이터 (예시)
email_normal_data = {
    "ip": "60.10.3.4", # ip
    "subject": "덜 수상한 파일첨부", # 제목
    "attachment": "제출용.hwp", # 파일이름
    "text" : "",
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


data = email_MaliciousFile_data

# artifacts는  나중에 Cortex_Analysis에 쓰일거임
alert_result, artifacts = Alert_Phishing(data) 

if(alert_result == "Alert created in The Hive"):
    case, case_id = Create_Case(data, file_path) # id 값 저장 나중에 Tasks 생성에 쓰임
    block_list_result=0
    ## 기존에 가지고 있는 차단 DB값에 쿼리(똑같은 값 전부 &로)
    for i in block_list:
        if(i["ip"]== data["ip"] and i["text"]==data["text"] and i["hash"]==data["hash"] and i["url"]==data["url"] and i["fqdn"]==data["fqdn"]):
            block_list_result=1

    if(block_list_result==1):    
        ## 만약 똑같은 값 있다면, case_result(id)에 Task1 생성
        print("이미 리스트에 차단리스트가 존재합니다.\n")
        task_result = Create_Task1(case_id)
        print(task_result)
        Human_Report =  "이미 차단 리스트가 존재합니다."
        Data_Info = data
        Update_Description(case_id, data, Data_Info, Human_Report)
        print("Case가 종료되었습니다.\n")
    '''
    ## 만약 값이 하나라도 다르면(DB에 없으면)
    else:    
        threshold = Analysis_Frame(data, case_id, artifacts)

        if(threshold==1):
            # 1 IP차단 간지나게 띄우는 척 하는거 띄움
            print("IP를 차단합니다.")            
            # 2 DB에 해당값 INSERT


            Create_Task3(case_id)
            Create_Description(case_id, report_info)
            print("Case가 종료되었습니다.\n")

        else:
            # 분석가들에게 메일 보냄
            Mailing()

            Create_Task3(case_id)

            # 추가할 내용 입력받기
            human_analysis_info = input("분석한 정보를 입력해주세요!")
            Create_Description(case_id, report_info, human_analysis_info)

            print("Case가 종료되었습니다.\n")

    '''


