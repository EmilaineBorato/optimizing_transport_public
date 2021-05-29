"""Defines trends calculations for stations"""
import logging
import faust
from dataclasses import asdict, dataclass


logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
@dataclass
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
@dataclass
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker="kafka://localhost:9092", store="memory://")

# TODO: Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
topic = app.topic("com.udacity.cta.stations", value_type=Station)

# TODO: Define the output Kafka Topic
out_topic = app.topic("com.udacity.cta.stations.transform", partitions=1)

# TODO: Define a Faust Table
table = app.Table(
   "com.udacity.cta.stations.table.transform",
   partitions = 1,
   changelog_topic = out_topic,
   value_type = TransformedStation
)

#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#
@app.agent(topic)
async def station(stations):

    async for st in stations:

        new_line = None

        if st.red is True:
             new_line = "red"
        elif st.blue is True:
             new_line = "blue" 
        elif st.green is True:
             new_line = "green"


        transformed = TransformedStation(
            station_id = st.station_id,
            station_name = st.station_name,
            order = st.order,
            line = new_line
        )
      
        # TODO: Send the data to the topic you created above
        #
        await out_topic.send(value=transformed)


if __name__ == "__main__":
    app.main()