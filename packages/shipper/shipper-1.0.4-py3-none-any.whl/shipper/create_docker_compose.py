from datetime import datetime

from shipper.check_and_create_folder import check_and_create_folder
from shipper.get_project_config import get_project_config


def create_docker_compose(project_list, configs):
    if len(project_list) != 0:
        check_and_create_folder("./result")
        with open(f'./result/docker-compose.yaml', "w+") as writer:
            writer.write('version: "3.9"\n')
            writer.write('services:\n')
            for project_name in project_list:
                project_config = get_project_config(project_name, configs)
                writer.write(f'  {project_name}:\n')
                writer.write(f'    image: jaytrairat/{project_name}:dev\n')
                writer.write(f'    restart: always\n')
                writer.write(f'    ports:\n')
                writer.write(f'      - \"{project_config["port"]}\"\n')
                writer.write(f'    deploy:\n')
                writer.write(f'      resources:\n')
                writer.write(f'        limits:\n')
                writer.write(f'          memory: "32M"\n')
                writer.write(f'        reservations:\n')
                writer.write(f'          memory: "32M"\n')
    print(datetime.now(), f":: docker compose with {len(project_list)} project(s)")
