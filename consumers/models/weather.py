"""Contains functionality related to Weather"""
import logging


logger = logging.getLogger(__name__)

WEATHER_TOPIC = "com.udacity.cta.producer.weather"


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

    def process_message(self, message):
        """Handles incoming weather data"""

        topic_name = message.topic()
        msg = message.value()
        logger.info(f"Topic: {topic_name} \nMessage: {msg} ")
        #
        #
        # TODO: Process incoming weather messages. Set the temperature and status.
        #
        #
        if topic_name == WEATHER_TOPIC:
            try:
                value = json.loads(msg)
                self.temperature = value['temperature']
                self.status = value['status']

            except Exception as e:
                logger.error(f"Weather error: {e}")
        else:
            logger.info(f"Topic '{topic_name}' not corresponding to the WEATHER TOPIC")
