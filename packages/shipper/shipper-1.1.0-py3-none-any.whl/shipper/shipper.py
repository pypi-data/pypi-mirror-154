import os
import shutil
from datetime import datetime
import typer

app = typer.Typer()


@app.command()
def shipper(tag, mode):
    if mode == 'self':
        current_working_directory = os.getcwd()
        project_name = os.path.basename(current_working_directory)
        is_services = project_name.endswith('services') or project_name.endswith('service') or project_name.endswith('api')
        try:
            os.system("yarn --silent")
            if not is_services: os.system("yarn build --quite")
            os.system("docker buildx create --name armbuilder")
            os.system("docker buildx use armbuilder")
            os.system(f"docker buildx build --quiet --platform linux/amd64 -t jaytrairat/{project_name}:{tag} . --push\n")
            print(datetime.now(), ':: finished')
        except Exception as error:
            print(error)
            pass
    elif mode == 'global':
        try:
            lines = []
            is_contained_ignore = os.path.isfile('./.shipperignore')
            is_contained_env = os.path.isfile('./.env.production')
            if is_contained_ignore:
                with open('./.shipperignore') as file:
                    lines = file.readlines()
                    lines = [line.rstrip() for line in lines]

            exclude = lines + ['venv', '.idea', '.git', '__pycache__', 'shipper', 'lib', 'result', 'build', 'dist']
            main_folder = [str(name) for name in os.listdir(".") if
                           os.path.isdir(name) and name not in exclude]
            for target_folder in main_folder:
                os.chdir(f'./{target_folder}')
                if is_contained_env:
                    shutil.copy('../.env.production', f'./')
                try:
                    os.system("yarn --silent")
                    os.system("yarn build --quite")
                    os.system("docker buildx create --name armbuilder")
                    os.system("docker buildx use armbuilder")
                    os.system(f"docker buildx build --quiet --platform linux/amd64 -t jaytrairat/{target_folder}:{tag} . --push\n")
                except Exception as error:
                    print(error)
                    pass
                print(datetime.now(), f' :: {target_folder} is execute')
                os.chdir('../')
            print(datetime.now(), ':: finished')
        except Exception as error:
            print(error)
            pass


if __name__ == '__main__':
    app()
