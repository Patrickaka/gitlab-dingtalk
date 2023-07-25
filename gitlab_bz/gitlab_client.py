import gitlab

from common import config

# 登陆
gl = gitlab.Gitlab(config.gitlab_url, config.gitlab_token)


def pipeline_create(project_id: int, rollback: bool, ref: str = 'master'):
    project = gl.projects.get(project_id)
    if rollback:
        pipeline = project.pipelines.create({
            'ref': ref,
            'variables': [{'key': 'ROLLBACK', 'value': 'true'}]
        })
    else:
        pipeline = project.pipelines.create({
            'ref': ref
        })
    print(pipeline.asdict())


if __name__ == '__main__':
    pipeline_create(13, True, '0721008_lcz')
