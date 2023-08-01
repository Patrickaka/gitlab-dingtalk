import gitlab

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


def tag_create(project_id: int, ref: str = 'master'):
    project = gl.projects.get(project_id)
    tags = project.tags.list()
    if tags:
        last_tag = tags.asdict()
    project.tags.create({
        'tag_name': "",
        'ref': ref
    })


if __name__ == '__main__':
    tag_create(13)
