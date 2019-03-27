import logging
from collections import namedtuple
from datetime import timedelta
import json
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.components.sensor.rest import RestData
from homeassistant.const import CONF_NAME

_LOGGER = logging.getLogger(__name__)
_ENDPOINT = 'https://api.weather.gov/alerts/active?zone='

CONF_ZONES = 'zones'

DEFAULT_NAME = 'NWS Weather Alert'
DEFAULT_VERIFY_SSL = True

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ZONES, default=[]): cv.ensure_list,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    method = 'GET'
    zones = config['zones']
    endpoint = _ENDPOINT + ','.join(zones)
    payload = auth = None
    verify_ssl = DEFAULT_VERIFY_SSL
    headers = {
        'User-Agent': 'Homeassistant',
        'Accept': 'application/geo+json',
    }

    rest = RestData(method, endpoint, auth, headers, payload, verify_ssl)
    rest.update()
    
    
    add_entities([NWSAlert(rest, name)], True)


class NWSAlert(Entity):

    def __init__(self, rest, name):
        self.rest = rest
        self._name = name
        self.out = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        if self.out is not None:
            if len(self.out) == 0:
                return "inactive"
            else:
                return "active"
        return None

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        if self.out is not None:
            alerts = {}
            for i, alert in enumerate(self.out):
                alerts['event_' + str(i)] =  alert['properties']['event']
                alerts['headline_' + str(i)] = alert['properties']['headline']
                alerts['desc_' + str(i)] = alert['properties']['description']
                alerts['expiry_' + str(i)] = alert['properties']['expires']
            return alerts

    def update(self):
        """Get the latest data from NWS and updates the state."""
        self.rest.update()
        try:
            self.out = json.loads(self.rest.data)['features']
        except IndexError:
            self.out = None
