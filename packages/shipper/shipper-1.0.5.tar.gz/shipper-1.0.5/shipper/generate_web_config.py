from datetime import datetime

from shipper.check_and_create_folder import check_and_create_folder
from shipper.get_project_config import get_project_config


def generate_web_config(project_list, configs):
    if len(project_list) != 0:
        check_and_create_folder('./result')
        with open('./result/web.config', 'w+') as writer:
            writer.write(f' <rewrite>\n')
            writer.write(f'     <rules>\n')
            for project_name in project_list:
                project_config = get_project_config(project_name, configs)
                writer.write(f'         <rule name="{project_name}" stopProcessing="true">\n')
                writer.write(f'             <match url="^{project_config["url"][1:]}/(.*)" />\n')
                writer.write(f'             <action type="Rewrite" url="http://127.0.0.1:{project_config["port"].split(":")[0]}/{{R:1}}" />\n')
                writer.write(f'         </rule>\n')
            writer.write(f'     </rules>\n')
            writer.write(f' </rewrite>\n')
    print(datetime.now(), f':: create web.configs with {len(project_list)} project(s)')
