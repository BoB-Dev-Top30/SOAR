from thehive4py.api import TheHiveApi
from cortex4py.api import Api
from thehive4py.models import Alert, AlertArtifact
from cortex4py.query import *

import datetime

# TheHive와 Cortex 설정
hive_url = 'http://127.0.0.1:9000'
hive_api_key = 'O+hgLkPUCzoDCFB+8TJQ7YGnjzbCLNnZ'
cortex_url = 'http://127.0.0.1:9001'
cortex_api_key = 'FrfLo5S0DZT7p1VR0vvoJ0gK8z60tfJv'

# TheHive API 연결
hive_api = TheHiveApi(hive_url, hive_api_key)

# Cortex API 연결
cortex_api = Api(cortex_url, cortex_api_key)


 # TheHive에 경고 생성
def Alert_Phishing(email_alert_data):
    artifacts=[]
    # artifacts의 종류에 따라서 append 여부 결정

    if(email_alert_data["ip"]!=""):
        artifacts.append(AlertArtifact(dataType='ip', data=email_alert_data['ip']))
    
    if(email_alert_data["hash"]!=""):
        artifacts.append(AlertArtifact(dataType='hash', data=email_alert_data['hash']))
    
    if(email_alert_data["url"]!=""):
        artifacts.append(AlertArtifact(dataType='url', data=email_alert_data['url']))

    alert = Alert(
        title='[Phishing Detection] ' + email_alert_data['subject'],
        description='Suspicious Email Detected!',
        type='external',
        source='Email-Security-System',  # 경고 출처
        sourceRef='email-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),  # 고유한 출처 참조
        
        severity=email_alert_data["severity"], # 피싱메일은 이정도로 고정한다고 가정
        tlp = email_alert_data["tlp"],
        pap = email_alert_data["pap"],
        artifacts=artifacts,
        tags=['phishing', 'email']
    )
    response = hive_api.create_alert(alert)

    if response.status_code == 201:
        result = "Alert created in The Hive"
    else:
        result = "Error creating alert"

    return result


