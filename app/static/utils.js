function _toast(color, message) {
    return Toastify({
        text: message,
        duration: 3000,
        close: true,
        gravity: 'top',
        position: 'center',
        stopOnFocus: true,
        style: {
            background: color,
            boxShadow: '0 3px 6px -1px rgba(0,0,0,.12), 0 10px 36px -4px rgba(0,0,0,.3)'
        }
    }).showToast();
}

function error(message) {
    return _toast('#c0392b', message);
}

function success(message) {
    return _toast('#27ae60', message);
}

function parseURL(url) {
    const parsed = /https?:\/\/(www\.|m\.)?twitch\.tv\/([^\/]+\/)?(videos|clip)\/([^? ]+)/g.exec(url);

    if (!parsed) return null;
    if (parsed[3] !== 'videos') return null;

    return parsed[4];
}

function toggleLoading(formSelector, isLoading) {
    const form = document.querySelector(formSelector);
    if (!form) return;

    const inputs = form.querySelectorAll('input');
    const buttons = form.querySelectorAll('button');

    for (const input of [...inputs, ...buttons]) {
        input.disabled = !!isLoading;
        if (input.tagName === 'BUTTON') input.classList[isLoading ? 'add' : 'remove']('is-loading');
    }
}

async function loadingFetch(formSelector, ...args) {
    toggleLoading(formSelector, true);

    const req = await fetch(...args)
        .catch(() => null);

    toggleLoading(formSelector, false);

    return req;
}
