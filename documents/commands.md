# **커맨드 목록**  

---

## **가상 환경 설정**  
- `python -m venv venv`  
  Python 가상 환경을 생성  
- `venv\Scripts\activate`  
  Windows에서 가상 환경을 활성화  

---

## **Docker 관련 명령어**  

- `docker compose -f docker-compose.light.yml up -d`  
  Docker Compose를 사용하여 컨테이너들을 백그라운드에서 실행  

- `docker build --tag airflow-custom:v4 airflow/`  
  `airflow/` 디렉토리를 기반으로 `airflow-custom:v4` 태그를 가진 Docker 이미지 빌드  

- `docker exec data-analysis-kafka-1 kafka-topics --list --bootstrap-server localhost:9092`  
  Kafka의 토픽 목록을 조회  

- `docker exec -it data-analysis-postgres-1 psql -U user -d mydb`  
  Docker 컨테이너 내의 PostgreSQL에 접속  

- `docker exec -it kafka kafka-console-producer \`  
  `--topic hdfs_pipeline \`  
  `--bootstrap-server kafka:9092`  
  Kafka 프로듀서를 실행하여 `hdfs_pipeline` 토픽으로 메시지를 보냄  

- `docker exec -it -u root spark-master /bin/bash`  
  Spark Master 컨테이너에 root 사용자로 접속  

- `docker exec -it -u root airflow-webserver /bin/bash`  
  Airflow Webserver 컨테이너에 root 사용자로 접속  

- `docker exec -it -u root airflow-scheduler /bin/bash`  
  Airflow Scheduler 컨테이너에 root 사용자로 접속  

- `docker cp <hostpath> <container>:<path>`  
  호스트에서 Docker 컨테이너로 파일을 복사  

- `docker inspect <container_id>`  
  특정 컨테이너의 상세 정보를 조회  

---

## **PostgreSQL 명령어**  

- `psql -U admin -d postgres`  
  PostgreSQL에 `admin` 사용자로 접속  

- `\dt`  
  PostgreSQL에서 현재 데이터베이스의 테이블 목록 조회  

---

## **네트워크 관련 명령어**  

- `netstat -ano | findstr :5432`  
  5432 포트로 연결된 프로세스 반환  

- `ping spark-master`  
  `spark-master` 노드에 대한 네트워크 연결 확인  

---

## **Git 명령어**  

- `git diff kafka/docker-compose.light.yml >> diff.txt`  
  특정 파일의 변경 내용을 `diff.txt`에 저장  

- `git diff --cached`  
  Staging된 변경 사항을 확인  

- `git diff branch1..branch2`  
  `branch1`과 `branch2`의 차이점 비교  

- `git reset HEAD~1`  
  마지막 커밋 복구  

- `git add -p docker-compose.yml`  
  `docker-compose.yml` 파일의 부분 변경 사항만 선택적으로 staging  

- `git checkout -b NEW_BRANCH_NAME COMMIT_ID`  
  특정 커밋 ID에서 새로운 브랜치를 생성하고 이동  

- `git clone -b issue-report https://github.com/yehoon17/data-analysis.git`  
  `issue-report` 브랜치를 기준으로 `data-analysis` 저장소 클론  

- `git stash push --staged -m "new line and custom docker image version"`  
  Staging된 변경 사항을 stash에 저장  

- `git log --follow -- <filename>`  
  특정 파일의 변경 이력을 추적  

---

## **Python 및 Spark 관련 명령어**  

- `pip freeze >> requirements.txt`  
  현재 가상 환경에 설치된 패키지 목록을 `requirements.txt`에 기록  

- `spark-submit /opt/spark/jobs/load_parquet_to_hdfs.py`  
  Spark 잡을 실행하여 Parquet 데이터를 HDFS로 로드  

- `spark-submit --master spark://spark-master:7077 /opt/spark/jobs/test_simple_job.py`  
  Spark Master에서 `test_simple_job.py` 잡 실행  

- `find / -name "spark_submit.py"`  
  시스템에서 `spark_submit.py` 파일 검색  

- `nano /home/airflow/.local/lib/python3.12/site-packages/airflow/providers/apache/spark/hooks/spark_submit.py`  
  Airflow Spark Hook의 `spark_submit.py` 파일을 nano 에디터로 열기  

- `sed -i '270s|conn_data\["master"\] = f"{conn.host}:{conn.port}"|conn_data["master"] = f"{conn.conn_type}://{conn.host}:{conn.port}"|' /home/airflow/.local/lib/python3.12/site-packages/airflow/providers/apache/spark/hooks/spark_submit.py`  
  Airflow의 Spark Hook에서 특정 코드 수정  

---

## **리눅스 패키지 설치 명령어**  

- `apt-get update -y`  
  패키지 목록 업데이트  

- `apt-get install -y nano`  
  Nano 에디터 설치  

- `apt-get install -y iputils-ping`  
  `ping` 명령어를 포함하는 `iputils-ping` 패키지 설치  
