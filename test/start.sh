#!/usr/bin/env bash
[ -z "$SENTRY_DSN" ] && echo "Specify SENTRY_DSN" && exit 1
uwsgi --http :8080 -w slow --master --processes 2 --threads 4 --harakiri 1 --log-alarm="raven HARAKIRI .* since" --alarm "raven cmd:python ../raven_harakiri.py"
