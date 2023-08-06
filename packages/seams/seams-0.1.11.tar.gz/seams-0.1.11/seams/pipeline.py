#!/usr/bin/env python
from seams import Seams
from abc import ABC, abstractmethod
import os
import tempfile

class Pipeline(object):

    @abstractmethod
    def run(**argsv):
        print("in run")
        pass
    
    def __init__(self, vertex_id, EMAIL, PASSWORD):
        self.vertex_id = vertex_id
        self.seams = Seams()
        self.seams.connect(EMAIL, PASSWORD)

    def update_status(self, tenant_id, vertex_id, status):
        vertex = self.seams.update_vertex(tenant_id, vertex_id, 'status', status)
        print(vertex)

    def run_pipeline(self, tenant_id, vertex_id):
        vertex = self.seams.get_vertex_by_id(tenant_id, vertex_id)
        return vertex['runParameters']

    def get_test_from_pipeline(self, tenant_id, vertex_id):
        vertex = self.seams.get_vertex_by_id(tenant_id, vertex_id)
        return vertex

    def update_pipeline_status_in_progress(self, tenant_id, vertex_id):
        status_update = self.seams.update_vertex(tenant_id, vertex_id, 'PipelineRun', {"status":"IN PROGRESS"})
        print(status_update)
    
    def update_pipeline_status_done(self, tenant_id, vertex_id):
        status_update = self.seams.update_vertex(tenant_id, vertex_id, 'PipelineRun', {"status":"DONE"})
        print(status_update)

    def update_pipeline_status_error(self, tenant_id, vertex_id):
        status_update = self.seams.update_vertex(tenant_id, vertex_id, 'PipelineRun', {"status":"ERROR"})
        print(status_update)

    def download_files(self, tenant_id, vertex_id):
        download = self.seams.download_files(tenant_id, vertex_id)
        files = []
        for item in download:
            temp_file_full_path = os.path.join(tempfile.gettempdir(), item)
            files.append(temp_file_full_path)
            f = open(temp_file_full_path, 'w', encoding="utf-8")
            f.write(download[item])
            f.close()
        return files
