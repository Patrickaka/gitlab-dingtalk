import gitlab
from gitlab import GitlabGetError

from common import config

# 登陆
gl = gitlab.Gitlab(config.gitlab_url, config.gitlab_token)


def pipeline_create(project_id: int, rollback: bool, ref: str = 'dev'):
    project = gl.projects.get(project_id)
    if rollback:
        pipeline = project.pipelines.create({
            'ref': ref,
            'variables': [{'key': 'ROLLBACK', 'value': 'true'}]
        })
    else:
        pipeline = project.pipelines.create({
            'ref': ref,
            'variables': [{'key': 'ref', 'value': ref}]
        })
    return pipeline.asdict()


def tag_validate(project_id: int, ref: str):
    project = gl.projects.get(project_id)
    try:
        project.tags.get(ref)
        return True
    except GitlabGetError:
        return False


if __name__ == '__main__':
    tag_validate(13, "08010012")
