# 打开一个文本文件，如果不存在则创建
with open('example.cfg', 'w') as file:
    # 写入文本内容
    file.write('!\r'*3)
    file.write('\r')
    file.write('!\r')
    file.write('version 15.2\r')
    file.write('service timestamps debug datetime msec\r')
    file.write('service timestamps log datetime msec\r')
    file.write('!\r')
    

# 读取刚刚写入的文本文件
with open('example.cfg', 'r') as file:
    # 读取文件内容并打印
    content = file.read()
    print(content)
