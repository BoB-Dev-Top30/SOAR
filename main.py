from HIVE.Alert_Phishing import *
from HIVE.Create_Case import *

# 이메일 보안 시스템에서 받은 데이터 (예시)
email_normal_data = {
    "ip": "60.10.3.4", # ip
    "subject": "덜 수상한 파일첨부", # 제목
    "attachment": "제출용.hwp", # 파일이름
    "text" : "",
    "hash" : "", # 파일 해시값
    "url": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php", # URL
    "severity": 1,
    "tlp":1,
    "pap":1,
}

email_MaliciousFile_data = {
    "ip": "80.34.3.8", # ip
    "subject": "수상한 파일첨부", # 제목
    "attachment": "제출용.hwp", # 파일이름
    "text" : "",
    "hash" : "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae", # 파일 해시값
    "url": "www.revitolcream.org/wp-content/plugins/all-in-one-seo-pack/rex/secure-code5/security/login.php", # URL
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
    "severity": 2,
    "tlp":2,
    "pap":2,
}

file_path = "C:/Users/scw10/OneDrive/바탕 화면/탑30/한주성멘토/0113/Suspicious_File/제출용.hwp"  # 첨부할 파일의 경로

alert_result = Alert_Phishing(email_MaliciousFile_data)
if(alert_result == "Alert created in The Hive"):
    case_result = Create_Case(email_MaliciousFile_data, file_path)
    print(case_result)