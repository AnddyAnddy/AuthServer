import enum
import json

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.haxball.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Access-Control-Allow-Origin, Content-Type"],
)


def create_json_if_not_exist():
    try:
        open("auths.json")
    except FileNotFoundError:
        with open("auths.json", "w") as f:
            json.dump({}, f)


create_json_if_not_exist()


class Role(enum.Enum):
    NOTHING = 0
    TEMP_ADMIN = 1
    ADMIN = 2
    MASTER = 3


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
        1: temp admin
        2: admin
        3: master
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


def filter_by_role(auths: dict[str, int], role: Role) -> list[str]:
    return [auth for auth, r in auths.items() if r == role.value]


@app.get("/admin/list")
async def list_admins() -> list[str]:
    """Send the auth list of all admins."""
    with open("auths.json") as f:
        return filter_by_role(json.load(f), Role.ADMIN)


@app.get("/master/list")
async def list_masters() -> list[str]:
    """Send the auth list of all masters."""
    with open("auths.json") as f:
        return filter_by_role(json.load(f), Role.MASTER)


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
