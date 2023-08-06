import shutil
from datetime import datetime


def place_env(project_list):
    for project_name in project_list:
        shutil.copy('./.env.production', f'../{project_name}')
    print(datetime.now(), f':: place .env.production to {len(project_list)} project(s)')


if __name__ == '__main__':
    place_env()
