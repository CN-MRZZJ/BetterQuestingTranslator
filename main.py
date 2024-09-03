import configparser
import importlib
import json
import time

config = configparser.ConfigParser()
config.read('config.ini')

try:
    driver = importlib.import_module('api.' + config['api']['driver'])
except ModuleNotFoundError:
    print(f'错误: 未找到API驱动: {config['api']['driver']}')
except Exception as e:
     print(f"一个未知的错误发生：{str(e)}")

try:
    # 尝试打开和读取文件
    with open(config['file']['input'], 'r') as file:
        data = json.load(file)
        print("成功解析到", len(data["questDatabase:9"]), "个任务")

# 如果文件不存在或无法以JSON格式加载，则捕获异常并打印错误信息
except FileNotFoundError:
    print(f"错误: 文件 {config['file']['input']} 未找到")
except json.JSONDecodeError:
    print(f"错误: 文件 {config['file']['input']} 的内容不是有效的 JSON 格式")
except Exception as e:
    print(f"一个未知的错误发生：{str(e)}")
count = 1
new_data = data
for key in data["questDatabase:9"].keys():
    name = data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"].strip()
    desc = data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"].strip()
    print("————————当前为第", count, "个任务————————")
    result_1 = driver.translate(name, config['api']['key'], config['api']['secret'],config['api']['url'])
    new_data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"] = result_1
    print("标题:", name, "->", result_1)
    time.sleep(config['api']['delay'] / 1000)
    result_2 = driver.translate(desc, config['api']['key'], config['api']['secret'],config['api']['url'])
    print("描述:", desc, "->", result_2)
    new_data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"] = result_2
    time.sleep(config['api']['delay'] / 1000)
    print("————————第", count, "个任务已完成————————")
    count = count + 1

with open(config["file"]['output'], 'w', encoding='utf-8') as f:
    json.dump(new_data, f)

print("————————执行完成————————")
