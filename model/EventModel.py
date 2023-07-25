from typing import Union

from model.CommonModel import *


class PushEvent(BaseModel):
    object_kind: str
    event_name: str
    before: Union[str, None] = None
    after: Union[str, None] = None
    ref: Union[str, None] = None
    user_id: int
    user_name: str
    user_username: str
    project_id: int
    project: Project
    repository: Repository
    commits: list[Commit]
    total_commits_count: int


class DeploymentEvent(BaseModel):
    object_kind: str
    status: str
    status_changed_at: str
    deployment_id: int
    deployable_id: int
    deployable_url: str
    environment: str
    project: Project
    short_sha: str
    user: User
    user_url: str
    commit_url: str
    commit_title: str
