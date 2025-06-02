"""Integration for LifeWatch devices."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from .mqtt_handler import async_setup_mqtt

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up LifeWatch integration."""
    _LOGGER.debug("async_setup called")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up LifeWatch from a config entry."""
    _LOGGER.debug("async_setup_entry called")
    await async_setup_mqtt(hass)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry called")
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
