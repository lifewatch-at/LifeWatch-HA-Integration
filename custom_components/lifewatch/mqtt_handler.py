"""MQTT handler for LifeWatch integration."""

import logging
import json
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.components.mqtt import async_subscribe
from homeassistant.core import HomeAssistant, callback
from .const import MQTT_TOPIC

_LOGGER = logging.getLogger(__name__)


async def async_setup_mqtt(hass: HomeAssistant) -> None:
    """Set up MQTT subscription for LifeWatch."""

    @callback
    def message_received(msg) -> None:
        """Handle incoming MQTT messages."""
        try:
            payload = json.loads(msg.payload)
            telemetry = payload.get("telemetry", {})
            entities = payload.get("entities", [])
        except json.JSONDecodeError:
            _LOGGER.error("Invalid JSON in payload: %s", msg.payload)
            return

        device_id = telemetry.get("id")
        device_name = telemetry.get("pretty_name")
        if not device_id:
            _LOGGER.warning("No device id in telemetry: %s", telemetry)
            return

        for entity in entities:
            entity_data = {
                "entity_id": entity.get("id"),
                "entity_name": entity.get("name"),
                "value": entity.get("value"),
                "unit": entity.get("unit"),
                "device_id": device_id,
                "device_name": device_name,
            }
            async_dispatcher_send(hass, "lifewatch_new_entity", device_id, entity_data)

    _LOGGER.debug("Registering MQTT handler")
    await async_subscribe(hass, MQTT_TOPIC, message_received)
