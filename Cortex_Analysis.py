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