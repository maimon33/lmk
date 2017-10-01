import re
import sys
import smtplib

import click


def _isvalidemail(email):
    import re

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if match == None:
        print 'Bad Syntax - Invalid Email Address'
        sys.exit()


def _send_mail(destination, msg):
    subject = 'lmk service'
    msg = 'Let you know\n\n{}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(cfg["mailer_username"], cfg["mailer_password"])
    server.sendmail(cfg["mailer_username"], destination,
                    'Subject: {}\n\n{}'.format(subject, msg))
    server.quit()



CLICK_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda param: param.lower(),
    ignore_unknown_options=True)

@click.group(context_settings=CLICK_CONTEXT_SETTINGS, cls=AliasedGroup)
@click.pass_context
def _lmk(ctx):
    """Client to upload files to S3 easily
    """
    if os.environ.get('S3S_ACCESS_KEY_ID') and os.environ.get(
            'S3S_SECRET_ACCESS_KEY'):
        ctx.obj = {}
    else:
        print '''AWS credentials missing
        Please run: `lmk config`'''
        # Kill process, AWS credentials are missing. no point moving forward!
        sys.exit()


@_lmk.command('config')
def config():
    """Config lmk creds for email
    
    lmk messages will be sent via Gmail
    """
    client.list_s3_content(dimension)
