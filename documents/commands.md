# 커맨드 목록

---

### **가상 환경 설정**
- `python -m venv venv`  
  Python 가상 환경을 생성
  
- `venv\Scripts\activate`  
  Windows에서 가상 환경을 활성화

---

### **Docker 관련 명령어**

- `docker exec data-analysis-kafka-1 kafka-topics --list --bootstrap-server localhost:9092`  
  Kafka의 토픽 목록을 조회

- `docker exec -it data-analysis-postgres-1 psql -U user -d mydb`  
  Docker 컨테이너 내의 PostgreSQL에 접속

- `docker compose -f docker-compose.light.yml up -d`  
  Docker Compose를 사용하여 컨테이너들을 백그라운드에서 실행

---

### **네트워크 관련 명령어**

- `netstat -ano | findstr :5432`  
  5432 포트로 연결된 프로세스 반환

---

### **Git 명령어**

- `git diff kafka/docker-compose.light.yml >> diff.txt`  
  특정 파일의 변경 내용을 `diff.txt`에 저장

- `git reset HEAD~1`  
  마지막 커밋 복구

- `git add -p docker-compose.yml`  
  `docker-compose.yml` 파일의 부분 변경 사항만 선택적으로 staging 

---

### **Python 패키지 관리**

- `pip freeze >> requirements.txt`  
  현재 가상 환경에 설치된 패키지 목록을 `requirements.txt`에 기록
