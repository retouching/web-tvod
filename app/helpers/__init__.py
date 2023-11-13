import os
from uuid import UUID

from tvod.twitch.client import Client

project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
twitch = Client(proxy=os.environ.get('PROXY') or None)


def get_current_domain():
    domain = os.environ.get('DETA_SPACE_APP_HOSTNAME')
    ssl = 'http://' if 'localhost' in domain else 'https://'

    return f'{ssl}{domain}'


def is_valid_uuid(raw_uuid, version=4):
    if type(raw_uuid) != UUID:
        try:
            UUID(raw_uuid, version=version)
        except ValueError:
            return False
    return True
