# Get propane data from Otodata API
# The time-based series are stored in InfluxDB.

# Requires username/password used with the Nee-vo mobile app (or similar app)

import json
import requests
import datetime
from pytz import timezone
from influxdb import InfluxDBClient

# Set parameters
NEEVO_AUTH = '<basic auth>'
TIMEZONE = 'US/Eastern'
PROVIDER_NAME = '<provider_name>'
METRIC_NAME = 'propane'

INFLUXDB_HOST = '<ip>'
INFLUXDB_PORT = '<port>'
INFLUXDB_USERNAME = '<username>'
INFLUXDB_PASSWORD = '<password>'
INFLUXDB_DATABASE = '<db_name>'

# Instantiate database
influxClient = InfluxDBClient(
    host=INFLUXDB_HOST,
    port=INFLUXDB_PORT,
    username=INFLUXDB_USERNAME,
    password=INFLUXDB_PASSWORD,
    database=INFLUXDB_DATABASE
)


def getDateTimeByZone(tz):
    t = timezone(tz)
    return datetime.datetime.now(t)


def printme(str):
    t = getDateTimeByZone(TIMEZONE)
    print(t.strftime("%Y-%m-%d %H:%M:%S"), str)
    return


def processChartData(tank_size, tank_level):
    try:
        remaining = (tank_level/100) * tank_size
        json_body = []
        json_body.append({
            "measurement": METRIC_NAME,
            "tags": {
                "source": PROVIDER_NAME
            },
            "time": getDateTimeByZone(TIMEZONE),
            "fields": {
                "litres": remaining,
                "level": tank_level
            }
        })
        influxClient.write_points(json_body)

    except Exception as e:
        if hasattr(e, 'message'):
            printme(e.message)
        else:
            printme(e)
        exit(0)

def main():

    session = requests.Session()

    printme("Getting levels")
    r = session.get(
        "https://telematics.otodatanetwork.com:4432/v1.5/DataService.svc/GetAllDisplayPropaneDevices",
        headers={
            "Accept": "*/*",
            "Accept-Language": "en-US;q=1, fa-US;q=0.9",
            "User-Agent": "Nee-Vo/2.5 (iPhone; iOS 16.0.2; Scale/3.00)",
            "Host": "telematics.otodatanetwork.com:4432",
            "Authorization": NEEVO_AUTH
        }
    )

    j = json.loads(r.text)
    processChartData(j[0]['TankCapacity'], j[0]['Level'])

    printme('Finished')


if __name__ == "__main__":
    main()
