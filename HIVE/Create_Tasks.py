from thehive4py.api import TheHiveApi
from thehive4py.models import Case, CaseObservable
from thehive4py.models import CaseTask
from config.config import *

import datetime
import base64
import os
import time
# TheHive
hive_url = 'http://127.0.0.1:9000'
hive_api_key = hive_api_key

# TheHive API 연결
hive_api = TheHiveApi(hive_url, hive_api_key)

# TheHive에 Task1 생성 뒤에는 Task2, Task3
def Create_Task1(case_id):
    # 새 태스크 생성

    task_title="Task1을 수행하세요"
    task_description= '''
    1) 해당 보안 시스템에 점검을 요청하거나 확인해주세요.
    2) Playbook을 보고 Task1에 대한 TTP를 작성해주세요.
    3) 본인이 수행한 일에 대한 Activity를 작성해주세요.
    '''
    task = CaseTask(
        title=task_title,
        description=task_description,
    )
    
    # 태스크를 사례에 추가
    response = hive_api.create_case_task(case_id, task)

    if response.status_code == 201:
        task_id = response.json()['id']
        result = f"Task created in The Hive with ID: {task_id}"
    else:
        result = f"Error creating task: {response.text}"

    return result

def Create_Task2(case_id):
    # 새 태스크 생성

    task_title="Task2를 수행하세요"
    task_description= '''
    1) 담당자분은 Case에 Comment를 작성해주세요
    2) Playbook을 보고 Task2에 대한 TTP를 작성해주세요.
    3) 본인이 수행한 일에 대한 Activity를 작성해주세요.
    '''

    task = CaseTask(
        title=task_title,
        description=task_description,
        startDate=int(time.time()) * 1000
    )
    
    # 태스크를 사례에 추가
    response = hive_api.create_case_task(case_id, task)

    if response.status_code == 201:
        task_id = response.json()['id']
        result = f"Task created in The Hive with ID: {task_id}"
    else:
        result = f"Error creating task: {response.text}"

    return result

def Create_Task3(case_id):
    # 새 태스크 생성

    task_title="Task3를 수행하세요"
    task_description= '''
    1) 담당자분은 Case에 Comment를 작성해주세요
    2) Playbook을 보고 Task3에 대한 TTP를 작성해주세요.
    3) 본인이 수행한 일에 대한 Activity를 작성해주세요.
    '''

    task = CaseTask(
        title=task_title,
        description=task_description,
        _parent=case_id
    )
    
    # 태스크를 사례에 추가
    response = hive_api.create_case_task(task)

    if response.status_code == 201:
        task_id = response.json()['id']
        result = f"Task created in The Hive with ID: {task_id}"
    else:
        result = f"Error creating task: {response.text}"

    return result