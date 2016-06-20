import argparse
import os
import raven
import sys
from subprocess import PIPE, Popen

try:
    from ConfigParser import RawConfigParser, NoSectionError
except ImportError:
    from configparser import RawConfigParser, NoSectionError


def send_to_sentry(args, stdout, stderr, exitcode, client_factory=raven.Client, extra={}):

    # set up sentry client by parsing config file
    config = RawConfigParser()
    config.read(args.config)
    client = client_factory(dsn=config.get(args.project, 'url'))

    # set tag based on exit code if configured
    try:
        tag = config.get('tag', 'name')
        success = config.get('tag', 'success')
        failure = config.get('tag', 'failure')
        if exitcode == 0:
            client.tags[tag] = success
        else:
            client.tags[tag] = failure
    except NoSectionError:
        pass
        
    # send to sentry
    if exitcode != 0 or args.ignore_exitcode:
        extra['exitcode'] = exitcode
        for key, value in os.environ.items():
            extra['env.' + key] = value
        msg = "{}\n\nstdout:\n{}\n\nstderr:\n{}".format(args.message, stdout, stderr)
        client.captureMessage(msg, extra=extra)

def main():
    parser = argparse.ArgumentParser(prog='sentryout', description='simple sentry cli wrapper')

    parser.add_argument('-p', '--project', metavar='PROJECT',
                        required=True, type=str,
                        help='the name of a Sentry project')

    parser.add_argument('-m', '--message', metavar='MSG',
                        required=True, type=str,
                        help='a description of what broke')

    parser.add_argument('-e', '--cmd', metavar='CMD',
                        required=True, type=str,
                        help='bash command or script to execute')

    parser.add_argument('-c', '--config', metavar='PATH', type=str,
                        default=os.path.join(os.path.expanduser('~'), '.sentryout.conf'),
                        help='location of Sentry configuration file')

    parser.add_argument('--ignore-exitcode', action='store_true',
                        help='send results to sentry regardless of exit code')

    parser.add_argument('-v', '--version', action='version', version='0.0.3')

    args = parser.parse_args()

    # execute provided command
    p = Popen(args.cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()

    # send results to sentry
    send_to_sentry(args, stdout, stderr, p.returncode)

if __name__ == "__main__":
    sys.exit(int(bool(main())))
