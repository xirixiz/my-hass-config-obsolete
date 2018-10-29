#!/bin/bash
docker stop hass && rm -rf home-assistant* && docker start hass
