import os
from datetime import datetime


def docker_publish(project_list):
    os.chdir('../')
    for project_name in project_list:
        os.chdir(f'./{project_name}')
        os.system("docker buildx create --name armbuilder")
        os.system("docker buildx use armbuilder")
        os.system(f"docker buildx build --quiet --platform linux/amd64 -t jaytrairat/{project_name}:dev . --push\n")
        os.chdir('../')
    print(datetime.now(), f':: published {len(project_list)} project(s)')
