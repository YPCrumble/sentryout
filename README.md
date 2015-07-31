# sentryout

## Overview

`sentryout` is a command line utility that sends stdout/stderr and other information to sentry.

This is useful for unattended operations like cron jobs.

## Installation

1. Create tarball from repo directory
```
tar -czf sentryout-0.0.1.tar.gz sentryout/
```

2. Install with pip

```
pip install -U sentryout-0.0.1.tar.gz
```

## Use

Example, execute a database backup and send the results to sentry:
```
sentryout --project cron --message 'database backup' --command 'pg_dump database > dump.sql'
```

By default `sentryout` sends stdout, stderr, and environment variables when an executed command returns a non-zero exit code.
This behavior can be overridden using any of the `--ignore-<item>` flags.

If you want to send *all* messages to sentry, regardless of exit code:

```
sentryout --project 'my project' --message 'my message here' --command 'echo "msg"' --ignore-exitcode
```

For the full list of options use the `--help` flag:
```
usage: to_sentry [-h] -p PROJECT -m MSG -e CMD [-c PATH]
                 [--ignore-environment] [--ignore-exitcode] [--ignore-stderr]
                 [--ignore-stdout] [-v]

dump command line sentry logger

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        the name of a Sentry project
  -m MSG, --message MSG
                        a description of what broke
  -e CMD, --cmd CMD     bash command or script to execute
  -c PATH, --config PATH
                        location of Sentry configuration file
  --ignore-environment  do not send environment variables to sentry
  --ignore-exitcode     send results to sentry regardless of exit code
  --ignore-stderr       do not send stderr output to sentry
  --ignore-stdout       do not send stdout output to sentry
  -v, --version         show program's version number and exit
```

## Configuration File

`sentryout` relies upon a configuration file for specifying the DSN url.
The default config file should be placed at `/etc/sentryout.conf`.
An alternative configuration file can be specified using the `--config` flag.

The configuration file should be formatted like the example below:
```
[project name]                                                                           
url=http://<sentry_dsn_url>
                                                                                 
[project name 2]                                                                       
url=http://<other_sentry_dsn_url>
```
