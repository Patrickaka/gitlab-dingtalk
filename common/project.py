class Pipeline:
    def __init__(self, pipeline_id=None, pipeline_url=None, ref=None):
        self.pipeline_id = pipeline_id
        self.pipeline_url = pipeline_url
        self.ref = ref


class Project:
    def __init__(self):
        self.pipeline_dict = dict()

    def add_pipeline(self, project_id, pipeline_id, pipeline_url, ref):
        self.pipeline_dict[project_id] = Pipeline(pipeline_id, pipeline_url, ref)

    def remove_pipeline(self, project_id):
        self.pipeline_dict.pop(project_id)
