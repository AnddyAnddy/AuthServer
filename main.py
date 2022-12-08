import enum
import json

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


def create_json_if_not_exist():
    try:
        open("auths.json")
    except FileNotFoundError:
        with open("auths.json", "w") as f:
            json.dump({}, f)


create_json_if_not_exist()


class Role(enum.Enum):
    NOTHING = 0
    ADMIN = 1
    MASTER = 2


class Auth(BaseModel):
    auth: str


class AuthUser(BaseModel):
    role: Role


@app.get("/")
async def root():
    return {"Root": "Check /docs if you're running from a web browser"}


@app.get("/{auth}")
async def get_role(auth: str) -> AuthUser:
    """Return code:
        0: No admin not master
        1: admin
        2: master
    """
    with open("auths.json", "r") as f:
        auths: dict[str, Role] = json.load(f)
    return AuthUser(role=auths.get(auth, Role.NOTHING))


@app.post("/admin/{auth}")
async def add_admin(auth: str):
    """Add an admin user."""
    save(auth, Role.ADMIN)
    return Auth(auth=auth)


@app.post("/master/{auth}")
async def add_master(auth: str):
    """Add a master user."""
    save(auth, Role.MASTER)
    return Auth(auth=auth)


@app.delete("/delete/{auth}")
async def delete(auth: str):
    """Delete an user user."""
    remove(auth)
    return Auth(auth=auth)


def save(auth: str, role: Role) -> None:
    with open("auths.json", "r") as f:
        auths: dict[str, Role.value] = json.load(f)
    auths[auth] = role.value
    with open("auths.json", "w") as writer:
        json.dump(auths, writer, indent=4, sort_keys=True)


def remove(auth: str) -> None:
    with open("auths.json", "r") as f:
        auths: dict[str, Role] = json.load(f)
    auths.pop(auth, None)
    with open("auths.json", "w") as writer:
        json.dump(auths, writer, indent=4, sort_keys=True)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", reload=True)
