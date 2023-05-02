<div>
    <h1 align="center">WEB TVOD</h1>
</div>

<br>

Simple example app of [TVOD](https://github.com/retouching/tvod)

<h2>Requirements</h2>

- **Python** (up to 3.9)

<h2>Installation</h2>

```shell
$ git clone "https://github.com/retouching/web-tvod.git"
```

```shell
$ cd web-tvod
```

```shell
$ python -m venv ./venv 
```

```shell
$ . .venv/bin/activate
```

```shell
$ pip install -r requirements.txt
```

<h2>Usage</h2>

If you are not in the venv
```shell
$ . .venv/bin/activate
```

```shell
$ flask run
```

To pass requests in a proxy, set the PROXY environment variable

You can also proxy segments stream by set CFW_PROXY_URL environment variable with your [cfw-proxy](https://github.com/retouching/cfw-proxy) URL

<h2>Demo</h2>

![](./.github/assets/example.gif)

<h2>Todolist</h2>

- [ ] Add auth system to limit who can have access the service

<h2>Warning: Some things need to be considered</h2>

 - This project is not approved by Twitch
