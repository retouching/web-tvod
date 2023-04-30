async function fetchVOD(evt) {
    evt.preventDefault();

    const player = document.querySelector('#player');
    if (!player) return;

    const streamSelectForm = document.querySelector('#formPlayer');
    if (!streamSelectForm) return;

    const form = document.querySelector('#formVOD');
    if (!form) return;

    const input = form.querySelector('input');
    if (!input) return;

    streamSelectForm.style.display = 'none';

    const playerInner = player.querySelector('vm-player');
    if (playerInner) playerInner.remove();

    const vodID = parseURL(input.value);

    if (!vodID) return error('Invalid VOD URL');

    const req = await loadingFetch('#formVOD', `/api/vod/${vodID}`);

    if (!req || req.status !== 200) return error('Invalid VOD URL');

    const { data } = await req.json();

    const select = streamSelectForm.querySelector('select');
    if (!select) return;

    select.innerHTML = '';

    for (const stream of data.streams) {
        const option = document.createElement('option');

        option.value = stream.url;
        option.text = `${stream.height}p`;
        if (stream.fps) option.text += ` ${stream.fps}fps`;

        select.add(option);
    }

    streamSelectForm.style.display = 'flex';

    success(`You can select quality for:\n${data.title} by ${data.streamer}`);
}

async function submitStream(evt) {
    evt.preventDefault();

    const form = document.querySelector('#formPlayer');
    if (!form) return;

    const select = form.querySelector('select');
    if (!select || !select.value) return;

    let player = document.querySelector('vm-player');
    if (player) player.remove();

    player = document.querySelector('#player');
    player.innerHTML = generatePlayer(select.value);
}
