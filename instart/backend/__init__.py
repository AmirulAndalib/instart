# TESTù
# TESTù

# che cazzo devo fare o_o
# aiutarmi a inizare il backend e trovare un modo per "connetterlo" al frontend
# vabben
# graziella 2000
# di nulla
# *silenzio*

# sì ma deciditi o 4 o 2 blocchi di indentazione
# ne metto 1 perchè nano di default ha il tab e non ho voglia di cambiarlo a spazi
# ah

# @StuckDuck si mette un webserver? o cos'altro metto?
# sebwerver va bene
# okat
# flasko o cosa?
# idk
# hmm
# metto sanic o flask
# non ne so altri
# metti sanic the hedgehog
# lol ok

# sera chicco di caffùù
# dobbiamo applicare nel client quello che ho fatto, cioè mettere una lista di partizioni che il frontend chiederà al backend
# farro
# lol si


import asyncio
import json
import random
import sanic
import subprocess
from sanic import response
from websockets.legacy.protocol import WebSocketCommonProtocol
from asyncio import Event
from .responses import *
from .config import Config
from sanic import websocket


class instartBackend(sanic.Sanic):
    def __init__(self, name=None, *args, **kwargs):
        super().__init__(name or "instart", *args, **kwargs)
        self._ready = Event()
        self.status = "not_ready"


app = instartBackend(__name__)
config = Config()


@app.route("/")
async def ciao(request):  # hello word fatto
    return response.text(
        "test"
        + (
            random.choice(["ù", "à", "è", "ì", "ò", "+"])
            * random.choice(
                [
                    1,
                    random.randint(1, 1000),
                    random.randint(1, 1000),
                    random.randint(1, 1000),
                    1000,
                ]
            )
        )
    )


@app.websocket("/backend")
async def feed(request, ws: WebSocketCommonProtocol):
    # roba temporanea
    app._ready.set()
    result = "SEI UN MUSO MARSO"
    while True:
        data = await ws.recv()
        print(f"[v] {data}")
        print(f"[D] {config}")  # debuggete
        await asyncio.sleep(0.2)
        try:
            data = json.loads(data)
        except ValueError:
            if data == "start":
                config.clear()
                app.status = "ready"
                result = app.status
                app._ready.set()

            elif data == "status":
                result = app.status
            elif data == "waituntilready":
                await app._ready.wait()
                result = "ready"
            elif data == "languages":
                result = json.dumps(config.languages)
            elif data == "disks":
                disks = [
                    a
                    for a in (
                        await app.loop.run_in_executor(
                            None,
                            lambda: subprocess.run(
                                "lsblk -b -d -o NAME,SIZE",
                                shell=True,
                                capture_output=True,
                            ),
                        )
                    )
                    .stdout.decode()
                    .split("\n")
                    if "sd" in a
                ]
                result = {}
                for disk in disks:
                    result[disk.split()[0]] = int(disk.split()[1])
                result = json.dumps(result)
            elif data == "close":
                app.status = "not_ready"
                result = "closed"
        else:
            result = json.dumps(await responses.getResponse(app, config, data))

        await ws.send(result)
        print(f"[^] {result}")
        if result == "closed":
            await ws.close()
        print()


def start():
    app.run(host="127.0.0.1", port=7835)

    # io devo andare, fù
    # same
