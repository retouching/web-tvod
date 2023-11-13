from flask import Blueprint
from tvod.helpers.exceptions import TwitchException
from tvod.models.stream import Stream

from app.helpers import twitch

router = Blueprint('vod', __name__, url_prefix='/api')


@router.route('/vod/<vod_id>', methods=['GET'])
def vod(vod_id):
    try:
        data = twitch.get_vod_data(vod_id)
    except TwitchException:
        return {'error': 'VOD not found'}, 400

    return {
        'data': {
            **data.dict(),
            'streams': [
                Stream(**{
                    **stream.dict(),
                    'url': f'/streams/'
                           f'{data.id}/{stream.resolution}{f"{stream.fps}fps" if stream.fps else ""}/master.m3u8'
                }).dict()
                for stream in data.streams
            ]
        }
    }
