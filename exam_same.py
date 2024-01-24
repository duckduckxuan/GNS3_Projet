def are_files_identical(file1, file2):
    same = True
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                print(f"line {line1} and {line2}不相同")
                same = False

    """
    # 检查文件是否有不同长度
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        if f1.read() or f2.read():
            return False
    """

    return same

# 替换为实际的文件路径
file_path1 = 'config_final\i9_startup-config.cfg'
file_path2 = 'i9_startup-config-new.cfg'

if are_files_identical(file_path1, file_path2):
    print("文件内容完全相同。")
else:
    print("文件内容不相同。")
