import os


def print_config_template(sub_url):
    configs = [
        {
            "name": name,
            "port": "5000:80",
            "url": f"/seeset/{sub_url}/{name}"
        }
        for name in os.listdir("../")
    ]
    for config in configs:
        print(config)
