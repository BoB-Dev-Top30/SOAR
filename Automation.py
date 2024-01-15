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

# 이메일 보안 시스템에서 받은 데이터 (예시)
email_alert_data = {
    "sender": "60.10.3.4",
    "subject": "Urgent Request",
    "attachment": "invoice.pdf",
    "link": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php"
}

# TheHive에 경고 생성
alert = Alert(
    title='[Phishing Detection] ' + email_alert_data['subject'],
    description='Suspicious email detected',
    type='external',
    source='EmailSecuritySystem',  # 경고 출처
    sourceRef='email-' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),  # 고유한 출처 참조
    severity=3,
    artifacts=[
        AlertArtifact(dataType='url', data=email_alert_data['link'])
    ],
    tags=['phishing', 'email']
)

response = hive_api.create_alert(alert)
if response.status_code == 201:
    print("Alert created in TheHive")
else:
    print("Error creating alert")

# Cortex에서 각 아티팩트에 대한 분석 실행
for artifact in alert.artifacts:
    
    analyzers = cortex_api.analyzers.find_all({}, range='all')
    for analyzer in analyzers:
        print('Analyzer {} is enabled'.format(analyzer.name))

    url_analyzers = cortex_api.analyzers.get_by_type('url')


    if url_analyzers:
        analyzer_id = analyzers[0].id
        print(f"Running analyzer with id: {analyzer_id} and data: {artifact.data}")
        job = cortex_api.analyzers.run_by_id(analyzer_id,  {
        'data': artifact.data,
        'dataType': 'url',
        'tlp': 1
}, force=1)
        print(f"Analyzer job started for {artifact.dataType}: {job.id}")
    else:
        print(f"No analyzer found for {artifact.dataType}")
