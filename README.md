

# Home Thermostat Display

This uses:
 - Raspberry Pi Pico W
 - MicroPython 1.27
 - Waveshare CapTouch ePaper 2.9 
 - Home Assistant
 - MQTT

aka: Is there any hot water?

### Pico Setup

Copy the file 'config-example.py' to 'config.py' and fill in the relevant values. Deploy to your Pico W.

### Home Assistant Setup

You'll need to configure HA to publish the temperature to a topic 'sensor.hw.temp', 
and the hot water state to 'sensor.hw.status'

Here are the HomeAssistant automations I use - this is from a Mitsubishi Heat Pump, you might have to tweak things.

The 'sensor.hw.status' will publish 'idle', 'heat_water' or 'heat_home' - you can find these strings in the code if you need 
something else.

```yaml
alias: Publish Hot Water Heater Status
description: ''
triggers:
  - trigger: state
    entity_id:
      - water_heater.home
    attribute: status
conditions: []
actions:
  - action: mqtt.publish
    metadata: {}
    data:
      evaluate_payload: false
      qos: '0'
      retain: false
      topic: sensor.hw.status
      payload: '{{ state_attr(''water_heater.home'', ''status'') }}'
mode: single
```

```yaml
alias: Publish Home Tank Temperature
description: ''
triggers:
  - trigger: state
    entity_id:
      - sensor.home_tank_temperature
conditions: []
actions:
  - action: mqtt.publish
    metadata: {}
    data:
      evaluate_payload: false
      qos: '0'
      retain: true
      topic: sensor.hw.temp
      payload: '{{ states(''sensor.home_tank_temperature'') }}'
mode: single
```

### Waveshare Driver

The display.py is a modified version of the supplied Waveshare python driver - it handles rotated display, and
screen updates are significantly quicker.

### writer.py

This is a modified version of writer.py -> https://github.com/peterhinch/micropython-font-to-py/blob/master/writer/writer.py
This version uses a very inefficient loop to draw the fonts, but it works properly on a grayscale display.

### ubuntu.py

This is generated using font_to_py. Here is the command line I used.

```bash
./venv/bin/python3 ./font_to_py.py /usr/share/fonts/truetype/ubuntu/UbuntuSans\[wdth\,wght\].ttf -c '0123456789.?' 90 ubuntu.py
```