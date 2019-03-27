# home-assistant-nws-alert-sensor
National Weather Service alert component for Home Assistant.

#### Usage
- Stick the sensor.py file in `custom_components/nws/`.
- In your configuration.yaml, add the following:
```
sensor:
  - platform: nws
    zones:
      - COZ240
      - COZ040
      - COC005
```
- Replace the zones with your zones, otherwise you'll get alerts for Arapahoe County, Colorado. You can do this by going to https://alerts.weather.gov/ and finding your county(ies) & zone(s).
- The output of the sensor is "active" or "inactive" and the attributes will return `event_i`, `headline_i`, `desc_i`, and `expiry_i` for each weather alert, where `i` is the index in the array of alerts returned. Feel free to do whatever you want with these - extract attributes with custom sensors, etc. I use a custom lovelace UI card to show up to 3 alerts in the same card. Someone smarter than me can probably come up with a better solution.
