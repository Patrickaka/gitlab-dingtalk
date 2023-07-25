from typing import Union

from pydantic.main import BaseModel


class Author(BaseModel):
    name: str
    email: str


class User(BaseModel):
    id: int
    name: str
    username: str
    avatar_url: str
    email: str


class Project(BaseModel):
    id: int
    name: str
    description: str
    web_url: str
    avatar_url: Union[str, None] = None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    homepage: str
    url: str
    ssh_url: str
    http_url: str


class Repository(BaseModel):
    name: str
    url: str
    description: str
    homepage: str
    git_http_url: str
    git_ssh_url: str
    visibility_level: int


class Commit(BaseModel):
    id: str
    message: str
    title: str
    timestamp: str
    url: str
    author: Author
    added: list[str]
    modified: list[str]
    removed: list[str]
