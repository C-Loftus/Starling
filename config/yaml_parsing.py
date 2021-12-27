import yaml

def parse_yaml_config():
    with open('config/config.yaml') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

        for key, value in config.items():
            print(key, value)



if __name__ == '__main__':
    parse_yaml_config()