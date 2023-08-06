import os
from datetime import datetime


def update_to_git(project_list):
    os.chdir('../')
    for project_name in project_list:
        try:
            os.chdir(f'./{project_name}')
            os.system("git add .")
            os.system("git commit -m 'auto: deploy'")
            os.system("git push")
            os.chdir('../')
        except Exception as error:
            print(error)
    print(datetime.now(), f':: build {len(project_list)} project(s)')
