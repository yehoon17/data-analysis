# HDFS Sink를 이용한 Kafka Connect 테스트

이 가이드는 HDFS Sink를 사용하여 Kafka Connect를 테스트하는 단계를 안내합니다. Docker를 사용하여 필요한 서비스를 설정하고, HDFS 권한을 구성하고, Kafka Connect 구성을 배포하고, 테스트 메시지를 생성합니다.

## Kafka Connect 테스트 단계

### 1. 필수 서비스 시작

Docker Compose를 사용하여 Kafka, Zookeeper, HDFS (NameNode, DataNode) 및 Kafka Connect를 시작합니다.

```sh
docker compose up -d kafka zookeeper namenode datanode kafka-connect
```

### 2. HDFS 권한 설정

Kafka Connect는 HDFS에 쓰기 위한 적절한 권한이 필요합니다. 다음 명령을 사용하여 권한을 설정합니다.

```sh
docker exec -it namenode bash
```

컨테이너 내부에서 다음을 실행합니다.

```sh
hdfs dfs -mkdir -p /user/appuser/test
hdfs dfs -chown -R appuser:supergroup /user/appuser
hdfs dfs -chmod -R 770 /user/appuser
```

컨테이너를 종료합니다.

```sh
exit
```

### 3. Kafka Connect HDFS Sink 배포

HDFS Sink에 대한 Kafka Connect 구성을 제출합니다.

```sh
curl -X POST -H "Content-Type: application/json" --data @kafka/hdfs-sink-config/hdfs-sink-test.json http://localhost:8083/connectors
```

커넥터가 생성되었는지 확인합니다.

```sh
curl http://localhost:8083/connectors
```

### 4. 테스트 메시지 생성

Kafka 컨테이너 쉘을 엽니다.

```sh
docker exec -it kafka bash
```

Kafka 콘솔 프로듀서를 시작합니다.

```sh
kafka-console-producer --broker-list kafka:9093 --topic test-topic
```

다음 JSON 메시지를 수동으로 입력합니다.

```json
{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob"}
{"id": 3, "name": "Charlie"}
{"id": 4, "name": "David"}
{"id": 5, "name": "Eve"}
{"id": 6, "name": "Frank"}
```

**Ctrl+D**를 눌러 프로듀서를 종료합니다.

### 5. HDFS에서 데이터 확인

HDFS의 파일 목록을 표시합니다.

```sh
hdfs dfs -ls /user/appuser/test
```

생성된 파일의 내용을 확인합니다.

```sh
hdfs dfs -cat /user/appuser/test/<your-file>
```

`<your-file>`을 실제 파일 이름으로 바꿉니다.
