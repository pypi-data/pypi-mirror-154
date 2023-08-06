import os
import shutil
from datetime import datetime

from shipper.check_and_create_folder import check_and_create_folder
from shipper.get_project_config import get_project_config


def create_run_script(project_list, configs):
    for project_name in project_list:
        project_config = get_project_config(project_name, configs)

        docker_output_folder = f'./result/{project_name}'
        docker_script_output_folder = f'./result/{project_name}/_docker'
        check_and_create_folder(docker_output_folder)
        check_and_create_folder(docker_output_folder + '/nginx')
        check_and_create_folder(docker_script_output_folder)
        check_and_create_folder(docker_script_output_folder + '/pem')

        with open(f'{docker_output_folder}/Dockerfile', "w+") as writer:
            writer.write('FROM node:14.16-alpine as build-stage\n')
            writer.write('WORKDIR /app\n')
            writer.write('COPY ./nginx ./nginx\n')
            writer.write('COPY ./build ./build\n')
            writer.write('FROM nginx:stable-alpine as deploy-stage\n')
            writer.write('COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf\n')
            writer.write('COPY --from=build-stage ./app/build /usr/share/nginx/html\n')
            writer.write('EXPOSE 80\n')
            writer.write('CMD ["nginx", "-g", "daemon off;"]\n')

        with open(f'{docker_output_folder}/nginx/default.conf', "w+") as writer:
            writer.write('server {')
            writer.write('  listen 80;')
            writer.write('  location / {')
            writer.write('    root /usr/share/nginx/html;')
            writer.write('    index index.html index.htm;')
            writer.write('    try_files $uri /index.html;')
            writer.write('  }')
            writer.write('  error_page 500 502 503 504 /50x.html;')
            writer.write('  location = /50x.html {')
            writer.write('    root /usr/share/nginx/html;')
            writer.write('  }')
            writer.write('}')

        with open(f'{docker_script_output_folder}/push.sh', "w+") as writer:
            writer.write('docker buildx create --name armbuilder\n')
            writer.write('docker buildx use armbuilder\n')
            writer.write(f'docker buildx build --platform linux/amd64 -t jaytrairat/{project_name}:dev . --push\n')

        with open(f'{docker_script_output_folder}/{project_name}.sh', "w+") as writer:
            writer.write('docker rmi $(docker images -f "dangling=true" -q)\n')
            writer.write(f"docker stop $(docker ps -a | grep {project_name} | awk '{{print $1}}')\n")
            writer.write(f"docker rm $(docker ps -a | grep {project_name} | awk '{{print $1}}')\n")
            writer.write(f'docker pull jaytrairat/{project_name}:dev\n')
            writer.write(f'docker run -dp {project_config["port"]} jaytrairat/{project_name}:dev\n')
            writer.write('read -p "Press any key to continue"')

        with open(f'{docker_script_output_folder}/upload.sh', "w+") as writer:
            writer.write(f"scp -i './_docker/pem/zenalyse_seeset.pem' './_docker/{project_name}.sh' ubuntu@ec2-54-179-47-137.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/\n")
            writer.write("ssh -i './_docker/pem/zenalyse_seeset.pem' ubuntu@ec2-54-179-47-137.ap-southeast-1.compute.amazonaws.com\n")
    print(datetime.now(), f':: create run scripts with {len(project_list)} project(s)')
