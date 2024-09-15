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
        raw_quests = json.load(file)
        print("成功解析到", len(raw_quests["questDatabase:9"]), "个任务")

# 如果文件不存在或无法以JSON格式加载，则捕获异常并打印错误信息
except FileNotFoundError:
    print(f"错误: 文件 {config['file']['input']} 未找到")
except json.JSONDecodeError:
    print(f"错误: 文件 {config['file']['input']} 的内容不是有效的 JSON 格式")
except Exception as e:
    print(f"一个未知的错误发生：{str(e)}")

def delay():
    time.sleep(float(config['api']['delay']) / 1000)

def translate(text):
    delay()
    return str(driver.translate(text, config['api']['key'], config['api']['secret'],config['api']['url']))

translated_quests = raw_quests
errorlist_title = []
errorlist_desc = []

for index, key in enumerate(raw_quests["questDatabase:9"].keys()):
    print(f"————————当前为第{index+1}个任务————————")
    title = raw_quests["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"].strip()
    desc = raw_quests["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"].strip()
    try:
        translated_quests["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"] = translate(title)
        print(f"标题:{title}->{translated_quests["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["name:8"]}")
    except Exception:
        errorlist_title.append(key)
        print(f"第{index+1}个任务,标题{key}错误,已加入错误列表")
    try:
        translated_quests["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"] = translate(desc)
        print(f"描述:{desc}->{translated_quests["questDatabase:9"][key]["properties:10"]["betterquesting:10"]["desc:8"]}")
    except Exception:
        errorlist_desc.append(key)
        print(f"第{index+1}个任务,描述{key}错误,已加入错误列表")
    print(f"————————第{index+1}个任务已完成————————")

with open(config["file"]['output'], 'w', encoding='utf-8') as f:
    json.dump(translated_quests, f)

print("————————执行完成————————")
