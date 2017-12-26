import os
import re
import sys
import json
import smtplib
import readline
import subprocess

from os.path import expanduser

import click
from click_didyoumean import DYMGroup


CONFIG_PATH = '{}/.lmk-config'.format(expanduser("~"))

def _missing_creds():
    print '''eMail creds are Missing!
Please run: `lmk --config`'''
    sys.exit()

def _config():
    print "Please provide Authentication details"
    LMK_GMAIL_ACCOUNT=raw_input('Enter Your Gmail Account Name : ')
    LMK_GMAIL_PASSWORD=raw_input('Enter Your Gmail Account Password : ')
    LMK_DESTINATION=_isvalidemail(raw_input('Enter lmk Destination eMail Address : '))
    config = {'LMK_GMAIL_ACCOUNT': LMK_GMAIL_ACCOUNT, 'LMK_GMAIL_PASSWORD': LMK_GMAIL_PASSWORD, 'LMK_DESTINATION': LMK_DESTINATION}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

def _isvalidemail(email):
    import re

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if match == None:
        print 'Bad Syntax - Invalid Email Address'
        sys.exit()
    else:
        return email

def _send_mail(destination, msg):
    subject = 'lmk service'
    msg = 'Let you know\n\n'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ.get("LMK_GMAIL_ACCOUNT"), os.environ.get("LMK_GMAIL_PASSWORD"))
    server.sendmail(os.environ.get("LMK_GMAIL_ACCOUNT"), os.environ.get("LMK_DESTINATION"), 'Subject: {}\n\n{}'.format(subject, msg))
    server.quit()

class CommandExecute(object):
    def __init__(self, command):
        self.command = command

    def __enter__(self):
        return self

    # def __exit__(self, *args, **kwargs):
    #     self.file.close()

    def __iter__(self):
        return self

    def next(self):
        # line = self.file.readline()

        if line == None or line == "":
            raise StopIteration

        return line


CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda param: param.lower(),
    ignore_unknown_options=True)
    
@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option('-c',
              '--config',
              is_flag=True,
              help="display run log in verbose mode")
def lmk(config=None):
    """cron based deamon to alert on command output
    """
    if config:
        if os.path.isfile(CONFIG_PATH):
            if click.confirm('You are overwriting exsisting creds!\nDo you want to continue?', default=True):
                _config()
            else:
                print "You are safe Now!"
                sys.exit()
        else:
            _config()
    
    try:
        with open(CONFIG_PATH) as config_file:
            cfg = json.load(config_file)
        if cfg['LMK_GMAIL_ACCOUNT'] and cfg['LMK_GMAIL_PASSWORD'] and cfg['LMK_DESTINATION']:
            pass
        else:
            _missing_creds()
    except IOError:
        _missing_creds()

    echo_last_command = subprocess.Popen(('echo', '"!:-1"'), stdout=subprocess.PIPE)
    print echo_last_command.stdout.read()



