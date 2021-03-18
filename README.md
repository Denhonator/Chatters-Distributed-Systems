### Start the server

`python3 main.py`

### Init DB

`python3 init_db.py` to populate db -> server ports 7501, 7502, 7503, 7504

### Docker

Build server image: "docker build -t server ." in app/server
Build client image: "docker build -t client ." in app/client

Run server: "docker run -it --rm -p <hostport>:7500/tcp -p <hostport>:7500/udp server <ownaddress> <hostport>"
Run client: "docker run -i --rm client <serveraddress> <serverport> <nickname>"