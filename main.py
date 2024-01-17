import json


def read_config(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_config(file_path, config):
    with open(file_path, 'w') as file:
        file.writelines(config)

def modify_hostname(config, old_hostname, new_hostname):
    return [line.replace(f"hostname {old_hostname}", f"hostname {new_hostname}") for line in config]

def main():
    config_file_path = 'example.cfg'
    old_hostname = 'R2'
    new_hostname = 'R1'

    # 读取配置文件
    config = read_config(config_file_path)

    # 修改配置
    modified_config = modify_hostname(config, old_hostname, new_hostname)

    # 保存修改后的配置
    write_config(config_file_path, modified_config)

    print(f"Configuration updated: Hostname changed from {old_hostname} to {new_hostname}")

if __name__ == "__main__":
    main()
