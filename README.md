# 데이터 분석 통합 시스템

## **프로젝트 개요**
이 프로젝트는 **Kafka**, **Airflow**, **PostgreSQL**, **Kafka Connect**, **Grafana**, **Kibana**, **Jupyter Notebooks**와 같은 도구들을 사용하여 로컬 데이터 분석 파이프라인을 설정합니다. 이 파이프라인은 **Kaggle 데이터셋**을 처리하고 분석하는 용도로 설계되었으며, **HDFS**를 통한 대규모 데이터 저장에 대한 기본 통합이 포함되어 있습니다.

## **사용 기술**
- **Apache Kafka**: 실시간 데이터 스트리밍 및 수집을 위한 플랫폼
- **Airflow**: ETL 파이프라인을 오케스트레이션
- **PostgreSQL**: 구조화된 데이터를 저장
- **Kafka Connect**: Kafka와 외부 시스템(PostgreSQL 등)을 연결
- **Grafana & Kibana**: 모니터링, 시각화 및 로그 분석 도구
- **Jupyter Notebooks**: 데이터 탐색 및 분석을 위한 도구
- **HDFS**: 분산 저장 시스템
- **Docker**: 모든 서비스를 위한 컨테이너화 및 오케스트레이션

## **Getting Started**

### **Prerequisites**
- **Docker** 설치 (Windows 사용자의 경우 WSL 2도 설치)
- **Docker Compose** 설치
- **Python** 설치 (스크립트 및 Airflow 실행 용도)

### **설치 방법**

1. **리포지토리 클론**:
   ```bash
   git clone https://github.com/yehoon17/data-analysis-project.git
   cd data-analysis-project
   ```

2. **컨테이너 빌드 및 실행**:
   Docker Compose를 사용하여 모든 서비스 시작
   ```bash
   docker-compose up -d
   ```

3. **Kaggle 데이터 다운로드**  
   Kaggle API 설정: [Kaggle API 설정 가이드](https://github.com/yehoon17/data-analysis/blob/data-analysis/raw_data/README.md)

   neo bank 데이터 다운로드:
   ```bash
   ./raw_data/download_neo_bank_data.sh
   ```
   
### HDFS 설정

Airflow 작업에 필요한 디렉토리와 권한을 HDFS에서 설정

1. **Hadoop Namenode 컨테이너에 접근:**
   ```bash
   docker exec -it namenode bash
   ```

2. **HDFS에 Airflow 디렉토리 생성:**
   ```bash
   hdfs dfs -mkdir -p /user/airflow
   ```

3. **디렉토리의 소유자 변경:**
   ```bash
   hdfs dfs -chown airflow:supergroup /user/airflow
   ```

4. **디렉토리 권한 설정:**
   ```bash
   hdfs dfs -chmod 770 /user/airflow
   ```
