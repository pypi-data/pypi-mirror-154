import os
from datetime import datetime


def update_project(project_list):
    os.chdir('../')
    for project_name in project_list:
        try:
            os.chdir(f'./{project_name}')
            os.system("git checkout .")
            os.system("git pull")
            os.chdir('../')
        except Exception as error:
            print(error)
    print(datetime.now(), f':: build {len(project_list)} project(s)')
