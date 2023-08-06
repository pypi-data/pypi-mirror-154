"""
loz main module.
"""
from getpass import getpass
from loz import cry
from os import path
import click
import json
import logging
import loz as app
import secrets
import sys
from click_aliases import ClickAliasedGroup

logging.basicConfig()
logger = logging.getLogger('loz')
logger.setLevel(logging.WARNING)

loz_file = path.expanduser("~/.loz")

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def multiline_input(text):
    print(text)
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)

def load(warn=True):
    if not path.isfile(loz_file):
        logger.debug(f"no loz file found at {loz_file}")
        if warn:
            print(f"{color.RED}First time use. Run init command.{color.END}")
        sys.exit(1)
    entities = None
    logger.debug(f"opening {loz_file}")
    with open(loz_file, 'r') as f:
        entities = json.loads(f.read())
        logger.debug(f"loaded entities from {loz_file}")
    return entities

def save(entities):
    logger.debug(f"opening {loz_file}")
    with open(loz_file, 'w') as f:
        f.write(json.dumps(entities))
        logger.debug(f"entities written to {loz_file}")


def validate_password(entities):
    while True:
        password = getpass("enter password:")
        try:
            logger.debug("validating password")
            cry.dec(entities['c'], password)
            return password
        except:
            print(f"{color.RED}bad password{color.END}")


@click.group(cls=ClickAliasedGroup)
@click.version_option(version=app.__version__,
    message=f"%(prog)s %(version)s - {app.__copyright__}")
@click.option('-d', '--debug', is_flag=True,
        help="Enable debug mode with output of each action in the log.")
@click.option('-f', '--file', type=str, default=loz_file,
        help=f"Specify custom loz file. Defaults to: {loz_file}")
@click.pass_context
def cli(ctx, **kwargs):
    global loz_file
    loz_file=ctx.params.get('file')
    if ctx.params.get('debug'):
        logger.setLevel(logging.DEBUG)
        logger.info("debug mode is on")


@cli.command()
def init():
    "Initialize secret storge with master password."
    if path.isfile(loz_file):
        logger.error(f"{loz_file} already exists")
        sys.exit(1)
    password = None
    while password == None:
        password = getpass("enter password:")
        if password != getpass("repeat:"):
            print(f"{color.RED}passwords do not match{color.END}")
            password = None
    token = secrets.token_bytes(64)
    enc_token = cry.enc(token, password)
    entities = {"c":enc_token, "e":{}}
    save(entities)
    print(f"{color.GREEN}{color.BOLD}{loz_file}{color.END}{color.GREEN} initialized with password{color.END}")
 

def add_secret(entity, username, multi=False):
    "Add secret as single or multiline."
    entities = load()
    password = validate_password(entities)
    secret = ""
    if multi:
        secret = multiline_input(f"{color.BOLD}Write multiline secret. Use CTRL+D to save:{color.END}")
    else:
        secret = input(f"{color.BOLD}secret: {color.END}")
    encrypted = cry.enc(secret.encode(), password)
    if not entity in entities["e"]:
        logger.debug(f"adding entity {entity} and adding username {username}")
        entities["e"][entity] = {username:encrypted}
    else:
        logger.debug(f"adding username {username} to existing entity {entity}")
        entities["e"][entity][username] = encrypted
    save(entities)

@cli.command(aliases=['set'])
@click.argument('entity')
@click.argument('username')
def add(entity, username):
    "Set secret for 'entity username' pair."
    add_secret(entity, username)

@cli.command(aliases=['mset'])
@click.argument('entity')
@click.argument('username')
def madd(entity, username):
    "Set multiline secret for 'entity username' pair."
    add_secret(entity, username, multi=True)

@cli.command()
@click.argument('entity')
@click.argument('username')
def get(entity, username):
    "Get secret for 'entity username' pair."
    entities = load()
    if entity not in entities["e"] or username not in entities["e"][entity]:
        print(f"{color.RED}{color.BOLD}{entity}/{username}{color.END}{color.RED} does not exist{color.END}")
        sys.exit(1)
    password = validate_password(entities)
    secret = entities["e"][entity][username]
    print(cry.dec(secret, password).decode("utf-8"))


@cli.command(aliases=['del'])
@click.argument('entity')
@click.argument('username', required=False, default="")
def rm(entity, username):
    "Delete username from entity or whole entity."
    entities = load()
    if entity not in entities["e"]:
        print(f"{color.RED}{color.BOLD}{entity}{color.END}{color.RED} does not exist{color.END}")
        sys.exit(1)
    if username and username not in entities["e"][entity]:
        rint(f"'{username}' not found in '{entity}'")
        sys.exit(1)
    if username:
        del(entities['e'][entity][username])
        print(f"{color.GREEN}{color.BOLD}{username}{color.END}{color.GREEN} deleted from {color.BOLD}{entity}{color.END}")
        if not entities['e'][entity]:
            del(entities['e'][entity])
            print(f"{color.GREEN}{color.BOLD}{entity}{color.END}{color.GREEN} deleted because it was left empty{color.END}")
    else:
        del(entities['e'][entity])
        print(f"{color.GREEN}{color.BOLD}{entity}{color.END}{color.GREEN} deleted{color.END}")
    save(entities)


@cli.command()
@click.argument('entity')
def all(entity):
    "List all secrets in one entity."
    entities = load()
    if entity not in entities["e"]:
        print(f"{color.RED}{color.BOLD}{entity}{color.END}{color.RED} does not exist{color.END}")
        sys.exit(1)
    password = validate_password(entities)
    for username in entities["e"][entity]:
        logger.debug("user found, decrypting secret")
        secret = entities["e"][entity][username]
        decrypted = cry.dec(secret, password).decode("utf-8")
        print(f"\n{color.BOLD}{entity}/{username}{color.END}\n{decrypted}")


@cli.command()
@click.argument('entity', required=False, default="")
def ls(entity):
    "List all entities or usernames under one entity."
    entities = load()
    if not entity:
        print("\n".join(entities['e'].keys()))
        return
    if entity not in entities["e"]:
        return
    print("\n".join(entities['e'][entity].keys()))
    return


@cli.command()
def bash_completion():
    "Lists available commands. Used for bash completion."
    print(" ".join([n for n, v in cli.commands.items()]))


if __name__ == '__main__':
    cli()

