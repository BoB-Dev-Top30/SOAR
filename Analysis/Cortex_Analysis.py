from cortex4py.api import Api
from cortex4py.query import *
from config.config import *
# 종류별로 가능한 analysis에서 전부 분석 실행
# Cortex에서 각 아티팩트에 대한 분석 실행
# Cortex API 연결
cortex_url = 'http://127.0.0.1:9001'
cortex_api_key = cortex_api_key

cortex_api = Api(cortex_url, cortex_api_key)

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