from pydantic import BaseModel


class DeployRequest(BaseModel):
    project_name: str | None = None
    project_branch: str | None = None
