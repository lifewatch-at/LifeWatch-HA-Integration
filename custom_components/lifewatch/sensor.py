"""Sensor platform for LifeWatch integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

from typing import Any


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up LifeWatch sensors from a config entry."""
    sensors: dict[str, LifeWatchSensor] = {}

    @callback
    def add_or_update_sensor(device_id: str, entity_data: dict[str, Any]) -> None:
        """Add or update a LifeWatch sensor entity."""
        unique_id = f"{device_id.replace(' ', '_').replace('-', '_').lower()}_{entity_data['entity_id']}"
        if unique_id in sensors:
            sensors[unique_id].update_value(entity_data.get("value"))
        else:
            sensor = LifeWatchSensor(device_id, entity_data, unique_id)
            sensors[unique_id] = sensor
            async_add_entities([sensor])

    async_dispatcher_connect(hass, "lifewatch_new_entity", add_or_update_sensor)


class LifeWatchSensor(SensorEntity):
    """Representation of a LifeWatch sensor."""

    def __init__(
        self, device_id: str, entity_data: dict[str, Any], unique_id: str
    ) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = unique_id
        self._attr_name = (
            f"{entity_data.get('device_name')} {entity_data.get('entity_name')}"
        )
        self._attr_native_unit_of_measurement = entity_data.get("unit")
        self._attr_native_value = entity_data.get("value")
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": entity_data.get("device_name"),
            "manufacturer": "LifeWatch",
            "model": "LifeWatch V0.3",
            "model_id": entity_data.get("device_id"),
        }

    def update_value(self, value: Any) -> None:
        """Update the sensor value."""
        self._attr_native_value = value
        self.async_write_ha_state()
