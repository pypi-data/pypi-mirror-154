from datetime import datetime

from shipper.check_and_create_folder import check_and_create_folder
from shipper.get_project_config import get_project_config


def create_reversed_proxy(project_list, configs):
    if len(project_list) != 0:
        check_and_create_folder("./result")
        with open(f'./result/reverse_proxy.txt', "w+") as writer:
            for project_name in project_list:
                project_config = get_project_config(project_name, configs)
                writer.write(f'location {project_config["url"]} {{\n')
                writer.write(f'    proxy_pass http://localhost:{project_config["port"].split(":")[0]}/;\n')
                writer.write(f'}}\n\n')
    print(datetime.now(), f":: reversed proxy with {len(project_list)} project(s)")
