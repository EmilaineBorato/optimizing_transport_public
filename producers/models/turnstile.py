"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from models.producer import Producer
from models.turnstile_hardware import TurnstileHardware


logger = logging.getLogger(__name__)

TOPIC_NAME = "com.udacity.cta.producer.turnstile"


class Turnstile(Producer):
    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")

    #
    # TODO: Define this value schema in `schemas/turnstile_value.json, then uncomment the below
    #
    value_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_value.json")

    def __init__(self, station):
        """Create the Turnstile"""
        #
        #
        # TODO: Complete the below by deciding on a topic name, number of partitions, and number of
        # replicas
        #
        #
        super().__init__(
            topic_name = TOPIC_NAME, # TODO: Come up with a better topic name
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema, #TODO: Uncomment once schema is defined
            num_partitions=1,
            num_replicas=1,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)
        logger.info(f"Turnstile num_entries: {num_entries}")
        #
        #
        # TODO: Complete this function by emitting a message to the turnstile topic for the number
        # of entries that were calculated
        #
        #
        try: 
            for i in range(num_entries):
                
                self.producer.produce(
                topic=self.topic_name,
                key_schema = self.key_schema,
                value_schema = self.value_schema,
                key={"timestamp": self.time_millis()},
                value={
                        "station_id" : self.station.station_id,
                        "station_name" : self.station.name,
                        "line" : self.station.color.name,
                    },
                )
        except Exception as e:
            logger.error(f"Error producer Turnstile: {e}")