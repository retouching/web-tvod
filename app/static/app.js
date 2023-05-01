async function fetchVOD(evt) {
    evt.preventDefault();

    const streamSelectForm = document.querySelector('#formPlayer');
    const vodForm = document.querySelector('#formVOD');
    const player = document.querySelector('#player');
    const input = vodForm.querySelector('input');
    const select = streamSelectForm.querySelector('select');

    streamSelectForm.style.display = 'none';
    player.style.display = 'none';

    if (window.hls) {
        window.hls.destroy();
        window.hls = null;
    }

    const vodID = parseURL(input.value);

    if (!vodID) return error('Invalid VOD URL');

    const req = await loadingFetch('#formVOD', `/api/vod/${vodID}`);

    if (!req || req.status !== 200) return error('Invalid VOD URL');

    const { data } = await req.json();

    select.innerHTML = '';

    for (const stream of data.streams) {
        const option = document.createElement('option');

        option.value = stream.url;
        option.text = `${stream.height}p`;
        if (stream.fps) option.text += ` ${stream.fps}fps`;

        select.add(option);
    }

    streamSelectForm.style.display = 'flex';
}

async function submitStream(evt) {
    evt.preventDefault();

    const form = document.querySelector('#formPlayer');
    const select = form.querySelector('select');

    if (window.hls) {
        window.hls.destroy();
        window.hls = null;
    }

    const player = document.querySelector('#player');

    if (Hls.isSupported()) {
        window.hls = new Hls();
        hls.loadSource(select.value);
        hls.attachMedia(player);
    } else if (player.canPlayType('application/vnd.apple.mpegurl')) {
        player.src = select.value;
    } else {
        error('HLS stream not supported on you device');
    }

    player.style.display = 'block';
}
