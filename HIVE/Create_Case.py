from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CaseObservable
from config.config import *

import datetime
import base64
import os

# TheHive와 Cortex 설정
hive_url = 'http://127.0.0.1:9000'
hive_api_key = hive_api_key

# TheHive API 연결
hive_api = TheHiveApi(hive_url, hive_api_key)

# TheHive에 case 생성
def Create_Case(email_alert_data, file_path):
    # 사례 생성
    
    case = Case(
        title='[Phishing Detection] ' + email_alert_data['subject'],
        description='Suspicious Email Detected!',
        severity=email_alert_data["severity"],
        tags=['phishing', 'email'],
        tlp=email_alert_data["tlp"],
        pap=email_alert_data["pap"],
        flag=True,
        # tasks=[{'title': 'Initial Analysis'}] # 태스트는 나중에 생성
    )
    response = hive_api.create_case(case)


    if response.status_code == 201:
        case_id = response.json()['id']
        print(f"Case created in The Hive with ID: {case_id}")
        # 관측치 추가 로직
        for observable_type in ['ip', 'hash', 'url']:
            if observable_type in email_alert_data and email_alert_data[observable_type]:
                observable_data = email_alert_data[observable_type]
                observable = CaseObservable(
                    dataType=observable_type,
                    data=observable_data,
                    message=f'Observable of type {observable_type}',
                    tlp=3,
                    ioc=False,
                    tags=['phishing', 'email'],
                    caseId=case_id  # 사례 ID를 지정합니다.
                )
                observable_response = hive_api.create_case_observable(case_id, observable)
                if observable_response.status_code == 201:
                    print(f"{observable_type.capitalize()} observable added successfully: {observable_data}")
                else:
                    print(f"Error adding {observable_type} observable: {observable_data}")
        return case, case_id
    else:
        print("Error creating case")
        return case, None
    '''

     # observable 추가
        file_observable = CaseObservable(
            dataType='file',
            data=file_path,  # 파일 경로를 직접 전달합니다.
            message='Attached file',
            tlp=3,
            ioc=False,
            tags=['attachment']
            # _parent=case_id  # 이 부분은 실제 사례 ID에 따라 설정합니다.
        )
        # 파일을 바이너리로 읽어서 base64 인코딩
        with open(file_path, 'rb') as file:
            file_content = base64.b64encode(file.read()).decode()

        # 파일 관측치를 생성합니다.
        file_observable = CaseObservable(
            dataType='file',
            data=file_path,  # 파일 경로를 직접 전달합니다.
            message='Attached file',
            tlp=3,
            ioc=False,
            tags=['attachment']
            # _parent=case_id  # 이 부분은 실제 사례 ID에 따라 설정합니다.
        )

        observable_response = hive_api.create_case_observable(case_id, file_observable)

        print(observable_response)
        if observable_response.status_code != 201:
            result += f"\nError adding file observable: {file_path}"
        else:
            result += "\nFile observable added successfully"
            '''