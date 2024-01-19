# SOAR
> pip install thehive4py==1.8.1

> pip install cortex4py==2.1.0

> pip install openai==0.28.0

> pip install python-magic==0.4.27
> 
> pip install python-magic-bin
requirements.txt를 참고해주세요.

## 환경구축
https://github.com/pidydx/libmagicwin64
-> 여기서 git clone 후 md파일들을 system32에 옮긴다.

### 애먹었던점
CoretexAPI가 아니라 그냥 API로 바꿔야함
참조 링크 : https://github.com/TheHive-Project/Cortex4py/blob/master/Usage.md

# 구성도
![Playbook(피싱 이메일 상황) (2)](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/52ead01e-f581-44ff-b81b-925c22de8819)


# Playbook 흐름 (Cortex는 위협이라고 판단하지 못했지만, AI모델이 위협이라고 판단한 상황)
### 보안시스템으로 부터 전달받은 데이터
![스크린샷 2024-01-19 231052](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/f437c2e3-fc54-41e6-b241-4afbc0b1e821)



## 1) Alert생성
Hive 패키지의 Alert_Phishing 모듈이 동작
![스크린샷 2024-01-19 232554](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/ec2dc91f-1be5-4856-abc4-d087f6936493)

![스크린샷 2024-01-19 233406](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/9dd71b90-8783-4f7b-86cc-14c045887c59)




## 2) Case생성
Hive패키지의 Create_Case 모듈이 동작

![case코드](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/9f651d33-9c99-4c49-9539-537e3b0fe294)

![스크린샷 2024-01-19 233253](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/ddc4c879-b2ac-4f08-a68d-835e39f554af)

![스크린샷 2024-01-19 233336](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/35b7b802-6143-4f5b-92aa-6240208e47b6)




## 3) 기존 Block-List와 비교(추후 DB로 구현)
![스크린샷 2024-01-19 231327](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/30b4af24-2ce2-4b50-87aa-d5ad80c6ec25)



## 4) 위협수준 분류
> 위협수준 분류에는 Analysis패키지가 관여 그중에서도 Analysis_Frame이 메인 core 모듈이 됨.

### 1> Cortex(Url_scan_io 분석기 사용) 추후 더 많은 분석기를 통해 정확도 향상
![스크린샷 2024-01-19 231500](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/0d525c07-603a-46e6-9771-19d23a570c56)


report가 생성되기 까지 while문을 통해 기다리다가 report를 받으면 여기서 total필드에서 악성여부 판별

### 2> BERT
전 프로젝트에서 같이 개발한 BERT 모델 사용 (가짜뉴스 및 사기데이터로 Fine-Tuning 된 모델)
![스크린샷 2024-01-19 231736](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/053c4855-282d-48ae-819e-e349f1bd9efe)


## 5) 메일전송
![스크린샷 2024-01-19 231836](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/2b2c7f72-e9f0-46b7-a260-f41527e1bb00)

![KakaoTalk_20240119_233454958](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/f0562401-e65e-45e2-86da-a8f98695eae6)




## 6) Task 생성(Playbook의 흐름대로 HIVE에 Task2 생성)
![스크린샷 2024-01-19 231911](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/d489d35b-b5b1-4801-be31-854d58df461f)


![스크린샷 2024-01-19 233730](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/87427aa4-daff-411c-825f-24d063377f63)



## 7) 정탐 vs 오탐 여부 전달
분석가가 정탐 인지 오탐인지 여부 전달

![스크린샷 2024-01-19 233802](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/24f5d88b-fb0b-4dea-9d8f-2e1a65d354ac)




## 8) 분석정보 LLM에 전달 및 Description 작성
### 1> 생성
![스크린샷 2024-01-19 232021](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/811e76c3-e185-4341-8822-a7a88dc17a13)


### 2> 프롬프트 템플릿
![스크린샷 2024-01-19 232035](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/d99a28e7-2235-4124-88aa-e20f4985599e)

### 3> Update 모듈
Hive 패키지의 Update_Description 모듈
![스크린샷 2024-01-20 001540](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/49dcf8c9-df42-4808-a8da-5de29c08a356)


### 4> Description 자동 업데이트
![스크린샷 2024-01-19 233858](https://github.com/BoB-Dev-Top30/SOAR/assets/109223193/cde5a988-0e24-4f54-ad6d-ef906f41e2ee)



## 9) 케이스 종료
