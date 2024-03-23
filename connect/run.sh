#! /bin/bash

COMPONENT_DIR="/home/appuser"

confluent-hub install debezium/debezium-connector-postgresql:latest \
  --component-dir $COMPONENT_DIR \
  --no-prompt

confluent-hub install confluentinc/kafka-connect-elasticsearch:latest \
  --component-dir $COMPONENT_DIR \
  --no-prompt

confluent-hub install neo4j/kafka-connect-neo4j:5.0.3 \
  --component-dir $COMPONENT_DIR \
  --no-prompt

cp /etc/connect/kafka-connect-redis-assembly-6.0.3.jar $COMPONENT_DIR/kafka-connect-redis-assembly-6.0.3.jar
cp /etc/connect/mongo-cdc-connector.jar $COMPONENT_DIR/mongo-cdc-connector.jar
/etc/confluent/docker/run