import os

import httpx
from flask import Blueprint, Response, redirect
from tvod.helpers.exceptions import TwitchException

from app.helpers import twitch

router = Blueprint('streams', __name__, url_prefix='/streams')


@router.route('/<vod_id>/<quality>/master.m3u8', methods=['GET'])
def stream(vod_id, quality):
    data = twitch.cache.get(f'stream:{vod_id}:{quality}')

    if not data:
        try:
            data = twitch.get_vod_data(vod_id)
        except TwitchException:
            return {'error': 'VOD not found'}, 400

        current_stream = next(filter(
            lambda s: s.get('id') == quality,
            [
                {
                    'url': s.url,
                    'id': f'{s.resolution}{f"{s.fps}fps" if s.fps else ""}'
                }
                for s in data.streams
            ]
        ), None)

        if not current_stream:
            return {'error': 'Stream quality not found'}, 400

        with httpx.Client(proxies=str(twitch.proxy) if twitch.proxy else None) as client:
            req = client.get(current_stream.get('url'))

        if req.status_code != httpx.codes.OK:
            return {'error': 'Unable to fetch stream'}, 500

        twitch.cache.set(f'stream:{vod_id}:{quality}', req.content, twitch.KEEP_IN_CACHE)
        data = req.content

    return Response(data, mimetype='application/vnd.apple.mpegurl')


@router.route('/<vod_id>/<quality>/<fragement>.ts', methods=['GET'])
def fragment(vod_id, quality, fragement):
    try:
        data = twitch.get_vod_data(vod_id)
    except TwitchException:
        return {'error': 'VOD not found'}, 400

    current_stream = next(filter(
        lambda s: s.get('id') == quality,
        [
            {
                **s.dict(),
                'id': f'{s.resolution}{f"{s.fps}fps" if s.fps else ""}'
            }
            for s in data.streams
        ]
    ), None)

    if not current_stream:
        return {'error': 'Stream fragement not found'}, 400

    current_master_stream = current_stream.get('url').split('/')[-1]
    ts_url = f'{current_stream.get("url").replace(current_master_stream, "")}{fragement}.ts'

    with httpx.Client(proxies=str(twitch.proxy) if twitch.proxy else None) as client:
        req = client.head(ts_url)

    if req.status_code != httpx.codes.OK:
        return {'error': 'Stream fragement not found'}, 400

    if os.environ.get('CFW_PROXY_URL'):
        return redirect(f'{os.environ.get("CFW_PROXY_URL")}?url={ts_url}&content_type=application/octet-stream')

    def generate_response():
        with httpx.stream('GET', ts_url) as content_stream:
            for chunk in content_stream.iter_bytes(chunk_size=8192):
                yield chunk

    return Response(generate_response(), mimetype='video/MP2T')
