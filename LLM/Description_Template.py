def Description_Template(Threat_Info, Bert_Report, Cortex_Report, Human_Report):

    template=f'''
    너는 SOAR(Security Orchestration, Automation, and Response)시스템에서 분석 보고서를 자동으로 작성해주는 솔루션이야.
    아래 정보를 보고 분석 보고서를 작성해줘

    <위협 이벤트 정보>
    {Threat_Info}

    
    <텍스트 분석 전용 AI Report>
    {Bert_Report}
    
    <Cortex 분석 Report>
    {Cortex_Report}
    
    <인간 분석가의 Report>
    {Human_Report}

    [주의사항]
    관련 정보가 없는 부분은 생략하고 작성해줘!
    '''
    print(template)
    return template