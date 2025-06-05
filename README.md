# 데이터 분석 통합 시스템

이 프로젝트는 **Kafka**, **Airflow**, **PostgreSQL**, **Kafka Connect**, **Grafana**, **Jupyter Notebooks** 등을 활용하여 로컬 환경에서 데이터 파이프라인을 구축하기 위한 예제입니다. 주로 Kaggle 데이터셋을 활용하며, 대규모 데이터 저장을 위해 **HDFS**와의 통합을 포함합니다.

## 목차
- [기술 스택](#기술-스택)
- [시작하기](#시작하기)
  - [사전 준비](#사전-준비)
  - [설치](#설치)
  - [HDFS 설정](#hdfs-설정)
- [프로젝트 구조](#프로젝트-구조)
- [TODO](#todo)

## 기술 스택
- **Apache Kafka**: 실시간 데이터 스트리밍 플랫폼
- **Airflow**: ETL 파이프라인 오케스트레이션
- **PostgreSQL**: 구조화된 데이터 저장소
- **Kafka Connect**: Kafka와 외부 시스템(PostgreSQL 등) 연결
- **Grafana**: 모니터링 및 로그 시각화 도구
- **Jupyter Notebooks**: 데이터 탐색 및 분석 환경
- **HDFS**: 분산 파일 시스템
- **Docker**: 서비스 컨테이너화 및 오케스트레이션

## 시작하기
### 사전 준비
- Docker (Windows의 경우 WSL2 포함)
- Docker Compose
- Python

### 설치
1. 리포지토리 클론
   ```bash
   git clone https://github.com/yehoon17/data-analysis-project.git
   cd data-analysis-project
   ```
2. 컨테이너 빌드 및 실행
   ```bash
   docker-compose up -d
   ```
3. Kaggle 데이터 다운로드
   - Kaggle API 설정 방법은 [raw_data/README.md](raw_data/README.md) 참고
   ```bash
   ./raw_data/download_neo_bank_data.sh
   ```

### HDFS 설정
Airflow 작업에 필요한 디렉터리와 권한을 HDFS에 생성합니다.
1. Hadoop Namenode 컨테이너 접속
   ```bash
   docker exec -it namenode bash
   ```
2. 디렉터리 생성 및 권한 부여
   ```bash
   hdfs dfs -mkdir -p /user/airflow
   hdfs dfs -chown airflow:supergroup /user/airflow
   hdfs dfs -chmod 770 /user/airflow
   ```

## 프로젝트 구조
```text
airflow/      # Airflow DAGs 및 Dockerfile
flask/        # 예제 Flask 애플리케이션
kafka/        # Kafka 설정 및 HDFS Sink 설정
postgres/     # 초기화 스크립트
raw_data/     # Kaggle 데이터 다운로드 스크립트
scripts/      # 테스트 스크립트
```

## TODO
- [ ] Dockerfile 빌드 문서 작성 또는 docker-compose.yml 수정
- [ ] Kaggle 데이터 압축 해제 스크립트 작성
