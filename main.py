import configparser
import importlib
import json
import time

config = configparser.ConfigParser()
config.read('config.ini')

input_name = config.get('file', 'input')
output_name = config.get('file', 'output')

driver_name = config.get('api', 'driver')
api_delay = int(config.get('api', 'delay'))
api_key = config.get('api', 'key')
api_secret = config.get('api', 'secret')

driver = importlib.import_module('api.' + driver_name)
try:
    # 尝试打开和读取文件
    with open(input_name, 'r') as file:
        data = json.load(file)
        print("成功解析到", len(data["questDatabase:9"]), "个任务")

# 如果文件不存在或无法以JSON格式加载，则捕获异常并打印错误信息
except FileNotFoundError:
    print(f"错误: 文件 {input_name} 未找到")
except json.JSONDecodeError:
    print(f"错误: 文件 {input_name} 的内容不是有效的 JSON 格式")
except Exception as e:
    print(f"一个未知的错误发生：{str(e)}")
count = 1
new_data = data
for key in data["questDatabase:9"].keys():
    name = data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"].strip()
    desc = data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"].strip()
    print("————————当前为第", count, "个任务————————")
    result_1 = driver.translate(name, api_key, api_secret)
    new_data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"] = result_1
    print("标题:", name, "->", result_1)
    time.sleep(api_delay / 1000)
    result_2 = driver.translate(desc, api_key, api_secret)
    print("描述:", desc, "->", result_2)
    new_data["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"] = result_2
    time.sleep(api_delay / 1000)
    print("————————第", count, "个任务已完成————————")
    count = count + 1

with open(output_name, 'w', encoding='utf-8') as f:
    json.dump(new_data, f)

print("————————执行完成————————")
