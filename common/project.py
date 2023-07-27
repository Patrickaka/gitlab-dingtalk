class Pipeline:
    def __init__(self, pipeline_id, pipeline_url):
        self.pipeline_id = pipeline_id
        self.pipeline_url = pipeline_url


class Project:
    def __init__(self):
        self.pipeline_dict = dict()

    def add_pipeline(self, project_id, pipeline_id, pipeline_url):
        self.pipeline_dict[project_id] = Pipeline(pipeline_id, pipeline_url)

    def remove_pipeline(self, project_id):
        self.pipeline_dict.pop(project_id)
