#!/usr/bin/env bash
uwsgi --http :8080 -w slow --master --processes 2 --threads 4 --harakiri 1 --log-alarm="raven HARAKIRI .* since" --alarm "raven cmd:raven-harakiri"
