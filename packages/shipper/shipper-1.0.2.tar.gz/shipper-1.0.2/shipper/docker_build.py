import os
from datetime import datetime


def docker_build(project_list):
    os.chdir('../')
    for project_name in project_list:
        try:
            os.chdir(f'./{project_name}')
            os.system("yarn --silent")
            os.system("yarn build --quite")
            os.chdir('../')
        except Exception as error:
            print(error)
    print(datetime.now(), f':: build {len(project_list)} project(s)')
