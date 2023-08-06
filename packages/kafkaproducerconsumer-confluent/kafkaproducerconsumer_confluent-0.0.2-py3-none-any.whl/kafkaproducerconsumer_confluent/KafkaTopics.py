from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka import Producer, Consumer, KafkaError
import json 
import argparse, sys
from confluent_kafka import avro, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from uuid import uuid4


name_schema = """
    {
        "namespace": "io.confluent.examples.clients.cloud",
        "name": "Name",
        "type": "record",
        "fields": [
            {"name": "name", "type": "string"}
        ]
    }
"""

class Name(object):
    """
        Name stores the deserialized Avro record for the Kafka key.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["name", "id"]

    def __init__(self, name=None):
        self.name = name
        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    @staticmethod
    def dict_to_name(obj, ctx):
        return Name(obj['name'])

    @staticmethod
    def name_to_dict(name, ctx):
        return Name.to_dict(name)

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return dict(name=self.name)


# Schema used for serializing Count class, passed in as the Kafka value
count_schema = """
    {
        "namespace": "io.confluent.examples.clients.cloud",
        "name": "Count",
        "type": "record",
        "fields": [
            {"name": "count", "type": "int"}
        ]
    }
"""


class Count(object):
    """
        Count stores the deserialized Avro record for the Kafka value.
    """

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["count", "id"]

    def __init__(self, count=None):
        self.count = count
        # Unique id used to track produce request success/failures.
        # Do *not* include in the serialized object.
        self.id = uuid4()

    @staticmethod
    def dict_to_count(obj, ctx):
        return Count(obj['count'])

    @staticmethod
    def count_to_dict(count, ctx):
        return Count.to_dict(count)

    def to_dict(self):
        """
            The Avro Python library does not support code generation.
            For this reason we must provide a dict representation of our class for serialization.
        """
        return dict(count=self.count)


class KafkaProducerConsumer():

    def pop_schema_registry_params_from_config(self, conf):
        """Remove potential Schema Registry related configurations from dictionary"""

        conf.pop('schema.registry.url', None)
        conf.pop('basic.auth.user.info', None)
        conf.pop('basic.auth.credentials.source', None)

        return conf

    def create_topic(conf, topic):
        """
            Create a topic if needed
            Examples of additional admin API functionality:
            https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py
        """

        admin_client_conf = self.pop_schema_registry_params_from_config(conf.copy())
        a = AdminClient(admin_client_conf)

        fs = a.create_topics([NewTopic(
            topic,
            num_partitions=1,
            replication_factor=3
        )])
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except Exception as e:
                # Continue if error code TOPIC_ALREADY_EXISTS, which may be true
                # Otherwise fail fast
                if e.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
                    print("Failed to create topic {}: {}".format(topic, e))
                    sys.exit(1)

    # Messages will be serialized as JSON 
    def json_serializer(self, messages):
        return json.dumps(messages).encode('utf-8')

    def acked(self, err, msg):       
        global delivered_records
        if err is not None:
            print("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            print("Produced record to topic {} partition [{}] @ offset {}"
                  .format(msg.topic(), msg.partition(), msg.offset()))

    def kafka_json_producer(self, topic_name,  message_type, key = None, messages_list = None,**conf):
        producer_conf = self.pop_schema_registry_params_from_config(conf)
        producer = Producer(producer_conf)
        ccloud_lib.create_topic(conf, topic_name)
        for messages in messages_list:
            producer.produce(topic = topic_name, key = key, value = self.json_serializer(messages), on_delivery=self.acked)
            producer.poll(0)
        producer.flush()


    def kafka_json_consumer(self, topic_name, auto_offset_reset, consumer_group,  **conf):
        
        consumer_conf = self.pop_schema_registry_params_from_config(conf)
        consumer_conf['group.id'] = consumer_group
        consumer_conf['auto.offset.reset'] = auto_offset_reset
        consumer = Consumer(consumer_conf)

        consumer.subscribe([topic_name])
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                elif msg.error():
                    print('error: {}'.format(msg.error()))
                else:
                    record_key = msg.key()
                    record_value = json.loads(msg.value())
                    yield(record_value)

        except KeyboardInterrupt:
            pass
        finally:
            # Leave group and commit final offsets
            consumer.close()

    def kafka_avro_consumer(self, topic_name, auto_offset_reset,consumer_group, **conf):  

        schema_registry_conf = {
            'url': conf['schema.registry.url'],
            'basic.auth.user.info': conf['basic.auth.user.info']}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        name = Name()
        count = Count()

        name_avro_deserializer = AvroDeserializer(schema_registry_client = schema_registry_client,
                                                schema_str = name_schema,
                                                from_dict = name.dict_to_name)
        count_avro_deserializer = AvroDeserializer(schema_registry_client = schema_registry_client,
                                                schema_str = count_schema,
                                                from_dict = count.dict_to_count)

        consumer_conf = self.pop_schema_registry_params_from_config(conf)
        consumer_conf['key.deserializer'] = name_avro_deserializer
        consumer_conf['value.deserializer'] = count_avro_deserializer
        consumer_conf['group.id'] = consumer_group
        consumer_conf['auto.offset.reset'] = auto_offset_reset
        consumer = DeserializingConsumer(consumer_conf)

        consumer.subscribe([topic_name])

    # Process messages
        total_count = 0
        while True:
            try:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                elif msg.error():
                    print('error: {}'.format(msg.error()))
                else:
                    name_object = msg.key()
                    count_object = msg.value()
                    count = count_object.count
                    total_count += count
                    print("Consumed record with key {} and value {}, \
                        and updated total count to {}"
                        .format(name_object.name, count, total_count))
            except KeyboardInterrupt:
                break
            except SerializerError as e:
                # Report malformed record, discard results, continue polling
                print("Message deserialization failed {}".format(e))
                pass
        consumer.close()
