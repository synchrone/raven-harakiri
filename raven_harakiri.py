#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import sys
from optparse import OptionParser
from raven import get_version, os, Client
from raven.transport import HTTPTransport


def store_json(option, opt_str, value, parser):
    try:
        value = json.loads(value)
    except ValueError as e:
        raise ValueError("Invalid JSON was used for option %s.  Received: %s" % (opt_str, value)) from e
    setattr(parser.values, option.dest, value)


def parse_harakiri_line(line):
    # Tue Dec 19 15:10:59 2017 - HARAKIRI [core 0] 127.0.0.1 - POST /bla/url?query=string since 1513692655
    date, harakiri, request = line.split(' - ')
    remote_ip = harakiri.split(' ')[-1]
    method, url, _, start_time = request.split(' ')
    query_string = None
    if '?' in url:
        url, query_string = url.split('?')

    return dict(method=method, url=url, query_string=query_string, env=dict(REMOTE_ADDR=remote_ip))


def main():
    root = logging.getLogger('sentry.errors')
    root.setLevel(logging.DEBUG)
    root.addHandler(logging.StreamHandler())

    parser = OptionParser(version=get_version())
    parser.add_option("--tags", type="string", nargs=1, dest="tags", default={}, action="callback", callback=store_json)
    parser.add_option("--dsn")
    opts, args = parser.parse_args()

    dsn = opts.dsn or os.environ.get('SENTRY_DSN')
    if not dsn:
        logging.error("Error: No configuration detected!\n"
                      "You must either pass a DSN to the command, or set the SENTRY_DSN environment variable.")
        return 1

    client = Client(dsn, include_paths=['raven'],
                    install_sys_hook=False,
                    install_logging_hook=False,
                    string_max_length=100000,
                    transport=HTTPTransport
                    )

    input = sys.stdin.readline().strip()
    try:
        info = parse_harakiri_line(input)
        info['env'].update(os.environ)

        client.captureMessage(
            message='uwsgi harakiri on worker',
            data=dict(
                request=info,
                logger='uwsgi.log-alarm.harakiri'
            ),
            level=logging.FATAL,
            stack=False,
            tags=opts.tags
        )

    except ValueError:
        logging.exception('Cannot parse STDIN')
        return 1


if __name__ == '__main__':
    main()
