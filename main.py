import netmiko
import telnetlib

from netmiko import ConnectHandler

# 路由器配置
router = {
    'device_type': 'cisco_c7200',  # 设备类型，根据你的设备调整
    'ip': '192.168.122.10',      # 路由器的管理IP
    'username': 'admin',         # 用户名
    'password': 'admin',         # 密码
}

# 连接到路由器
net_connect = ConnectHandler(**router)

# 配置命令列表
config_commands = [
    'ip route 0.0.0.0 0.0.0.0 192.168.122.1'
]

# 发送配置
output = net_connect.send_config_set(config_commands)
print(output)

# 断开连接
net_connect.disconnect()
