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
![Playbook(피싱 이메일 상황) (2)](https://github.com/S-SIRIUS/SOAR/assets/109223193/7240985e-dec5-4319-a578-72190e5913e6)

# Playbook 흐름 (Cortex는 위협이라고 판단하지 못했지만, AI모델이 위협이라고 판단한 상황)
### 보안시스템으로 부터 전달받은 데이터
![스크린샷 2024-01-19 231052](https://github.com/S-SIRIUS/SOAR/assets/109223193/72527180-ca44-4a52-80da-2a7bcf526fc2)

## 1) Alert생성
Hive 패키지의 Alert_Phishing 모듈이 동작

![스크린샷 2024-01-19 232554](https://github.com/S-SIRIUS/SOAR/assets/109223193/0294f598-98f3-40e9-bd1e-4e264c9fca8d)

![스크린샷 2024-01-19 233406](https://github.com/S-SIRIUS/SOAR/assets/109223193/47ca97b2-05a7-4514-9437-9fb10afe97d3)


## 2) Case생성
Hive패키지의 Create_Case 모듈이 동작

![스크린샷 2024-01-19 231224](https://github.com/S-SIRIUS/SOAR/assets/109223193/2ec5a8ae-69d5-43ab-8cb8-9ec6913cad11)

![스크린샷 2024-01-19 233253](https://github.com/S-SIRIUS/SOAR/assets/109223193/ecf788d0-254c-4ceb-9ae3-4d6441a7b05e)

![스크린샷 2024-01-19 233336](https://github.com/S-SIRIUS/SOAR/assets/109223193/50504156-ad80-4e1d-999f-35d218e07837)



## 3) 기존 Block-List와 비교(추후 DB로 구현)
![스크린샷 2024-01-19 231327](https://github.com/S-SIRIUS/SOAR/assets/109223193/4dc6fdc2-2f8a-410e-aefa-3227739ea456)


## 4) 위협수준 분류
> 위협수준 분류에는 Analysis패키지가 관여 그중에서도 Analysis_Frame이 메인 core 모듈이 됨.

### 1> Cortex(Url_scan_io 분석기 사용) 추후 더 많은 분석기를 통해 정확도 향상
![스크린샷 2024-01-19 231500](https://github.com/S-SIRIUS/SOAR/assets/109223193/ea7f9e47-4758-4b56-ad61-b0879e1a09fe)
report가 생성되기 까지 while문을 통해 기다리다가 report를 받으면 여기서 total필드에서 악성여부 판별

### 2> BERT
전의 프로젝트에서 같이 개발한 BERT 모델 사용 (가짜뉴스 및 사기데이터로 Fine-Tuning 된 모델)
![스크린샷 2024-01-19 231736](https://github.com/S-SIRIUS/SOAR/assets/109223193/4bf67537-ff07-43b6-bd25-c7ac5b2694bf)


## 5) 메일전송
![스크린샷 2024-01-19 231836](https://github.com/S-SIRIUS/SOAR/assets/109223193/19e14d42-c633-4463-903f-ed181b8b9fe3)

![KakaoTalk_20240119_233454958](https://github.com/S-SIRIUS/SOAR/assets/109223193/dfeba35f-0765-4b60-b6a4-45da82baecf2)


## 6) Task 생성(Playbook의 흐름대로 HIVE에 Task2 생성)
![스크린샷 2024-01-19 231911](https://github.com/S-SIRIUS/SOAR/assets/109223193/a5afe4c3-1af0-4d7c-a0b9-e44bdae4acba)

![스크린샷 2024-01-19 233730](https://github.com/S-SIRIUS/SOAR/assets/109223193/6736d85c-3c6b-42bb-bc59-ea069075aa02)


## 7) 정탐 vs 오탐 여부 전달
분석가가 정탐 인지 오탐인지 여부 전달

![스크린샷 2024-01-19 233802](https://github.com/S-SIRIUS/SOAR/assets/109223193/3bc64d61-cd7b-4e92-8964-85ddd45b86c7)



## 8) 분석정보 LLM에 전달 및 Description 작성
### 1> 생성
![스크린샷 2024-01-19 232021](https://github.com/S-SIRIUS/SOAR/assets/109223193/d3f910c3-e64d-4c75-b308-948b31dcdb0d)

### 2> 프롬프트 템플릿
![스크린샷 2024-01-19 232035](https://github.com/S-SIRIUS/SOAR/assets/109223193/1deb8119-62b7-4504-8bd6-273fa59a7fc2)

### 3> Description 자동 업데이트
![스크린샷 2024-01-19 233858](https://github.com/S-SIRIUS/SOAR/assets/109223193/d141ae0c-8f43-4617-afe3-04fe4ac1890c)


## 9) 케이스 종료
