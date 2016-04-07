#!/bin/bash

docker run --restart always --link postgres --link nginx --link memcached --name brp_demo_harvest --env-file /opt/apps/brptoolkit-demo-harvest/production.env -d demo-harvest
