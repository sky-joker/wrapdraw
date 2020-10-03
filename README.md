# wrapdraw

[![](https://img.shields.io/github/license/sky-joker/wrapdraw?style=for-the-badge)](https://github.com/sky-joker/wrapdraw/blob/master/LICENSE.txt)
[![](https://img.shields.io/docker/image-size/skyjokerxx/wrapdraw?sort=date&style=for-the-badge)](https://hub.docker.com/r/skyjokerxx/wrapdraw)

This tool can automatically render and download a network diagram from [drawthe](https://github.com/cidrblock/drawthe.net).

## Requirements

* Python >= 3.6

## Usage

You can do to start the wrapdraw container the following procedure.

**If using docker**

```
# docker run -itd --name wrapdraw --rm skyjokerxx/wrapdraw:latest
# docker ps
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS               NAMES
bd550e0bb9e6        skyjokerxx/wrapdraw:latest   "/bin/sh -c 'pytho..."   38 seconds ago      Up 37 seconds                           wrapdraw
```

**If using podman**

```
# podman run -itd --name wrapdraw --rm skyjokerxx/wrapdraw:latest
# podman ps
CONTAINER ID  IMAGE                                 COMMAND               CREATED         STATUS             PORTS  NAMES
3138419da952  docker.io/skyjokerxx/wrapdraw:latest  /bin/sh -c python...  30 seconds ago  Up 29 seconds ago         wrapdraw
```

**The example of when using Ansible**

Please see the following sample.

[https://github.com/sky-joker/wrapdraw/tree/master/sample/ansible](https://github.com/sky-joker/wrapdraw/tree/master/sample/ansible)

## Environment variable

The following environment variables are available to set when starting a container.

|        env         |                                 default                                 |              description              |
|--------------------|-------------------------------------------------------------------------|---------------------------------------|
| URL                | http://go.drawthe.net/                                                  | URL of drawthe to use                 |
| UPLOAD_FOLDER      | upload                                                                  | A save path of a YAML file uploaded   |
| SAVE_FOLDER        | save                                                                    | A save path of an NW diagram rendered |
| DRIVER_PATH        | /usr/local/lib/python3.6/site-packages/chromedriver_binary/chromedriver | A save path of chromedriver           |
| CHROME_WINDOW_SIZE | 1920,1080                                                               | Window size of Google Chrome          |
| LISTEN_PORT        | 8080                                                                    | The app listen port                   |

If you want to use locally constructed drawthe, set the URL environment the following procedure.

```
# docker run -itd --name wrapdraw --rm -e URL='http://172.17.0.3' skyjokerxx/wrapdraw:latest
```

If you felt an NW diagram small, you can change its size the following procedure.

```
# docker run -itd --name wrapdraw --rm -e CHROME_WINDOW_SIZE='2560,2048' skyjokerxx/wrapdraw:latest
```

## License

[MIT](https://github.com/sky-joker/wrapdraw/blob/master/LICENSE.txt)
