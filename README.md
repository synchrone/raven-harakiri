Raven Harakiri
===

This executable helps you transfer uwsgi harakiris to Sentry. 
Maybe not much context, but a good way to centralize all app issues.


Installation
----
```
[uwsgi]
log-alarm = raven HARAKIRI .* since
alarm = raven cmd:raven-harakiri
```
If you have set SENTRY_DSN for uwsgi, it will be picked up. Alternatively, specify

```
alarm = raven cmd:raven-harakiri --dsn https://api:key@sentry.io/PROJID
```

