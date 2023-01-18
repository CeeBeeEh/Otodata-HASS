# Otodata-HASS
Script to pull propane tank data from Otodata and store it in InfluxDB (presumably with Home Assistant)

I used the following projects as a basis for this one:

* https://github.com/maennes/hydro_greenbutton

* https://github.com/kayvz/neevo_tank_monitor_query

Simply modify the script by changing the relevant bits to your InfluxDB connection details, timezone, your service provider name (who you get your propane/gas from), and your credentials.

The OTODATA_AUTH line is http basic authentication which is a base64 encoded string of your username and password (the one you use to login to the mobile app to see your tank levels).

This is the app that I use: https://play.google.com/store/apps/details?id=ca.otodata.nee_vo

You can generate the authentication string here: https://mixedanalytics.com/tools/basic-authentication-generator/

After everything is configured, add a cron job to run the script at regular intervals. I chose 6 hour intervals.

Here's an example cron job:

`0 */6 * * *     ceebee   /usr/bin/python3 /home/ceebee/otodata_hass.py`

After some data points are logged in the database you can start building dashboards with it in Grafana (or another system).
