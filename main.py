#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4
from os import environ
import subprocess


class Query(BaseModel):
    token: str
    zone: str
    record: str
    record_type: str
    ttl: int = 60
    value: str


if "TOKEN" not in environ:
    environ["TOKEN"] = str(uuid4())
token = environ["TOKEN"]
app = FastAPI()


def apply_nsupdate(nsupdate: str):
    tmp = NamedTemporaryFile()
    with open(tmp.name, "w") as f:
        f.write(nsupdate)

    process = subprocess.Popen(
        ["nsupdate", "-k", "/run/named/session.key", tmp.name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    return stdout, stderr


@app.put("/")
async def update_zone_record(query: Query):
    if query.token != token:
        return

    nsupdate = """
server dns
zone {zone}
update delete {record}. {record_type}
update add {record}. {ttl} {record_type} {value}
show
send
    """.format(
        zone=query.zone,
        record=query.record,
        record_type=query.record_type,
        value=query.value,
        ttl=query.ttl,
    )

    stdout, stderr = apply_nsupdate(nsupdate)
    return stdout, stderr


@app.delete("/")
async def delete_zone_record(query: Query):
    if query.token != TOKEN:
        return

    nsupdate = """
server dns
zone {zone}
update delete {record}. {record_type}
show
send
    """.format(
        zone=query.zone,
        record=query.record,
        record_type=query.record_type,
        value=query.value,
        ttl=query.ttl,
    )

    stdout, stderr = apply_nsupdate(nsupdate)
    return stdout, stderr
