import json
import os
import pandas as pd

def extract_text(data):
    text = ""

    # 处理 section_title
    section_title = data["section_title"]
    if section_title:
        text += section_title + "\n"

    # 处理 paragraphs
    paragraphs = data["paragraphs"]
    if paragraphs:
        text += "\n".join(paragraphs) + "\n"

    # 递归处理 subsections
    subsections = data["subsections"]
    for subsection in subsections:
        subsection_text = extract_text(subsection)
        text += subsection_text

    return text

def json_to_text(data):
    # 将 JSON 解析为 Python 数据结构
    # data = json.loads(json_data)

    # 提取文本内容
    text = extract_text(data)

    return text

# # 示例 JSON 数据
# json_data = '''
# {
#     "section_title": "Introduction",
#     "paragraphs": ["This is the introduction paragraph."],
#     "subsections": [
#         {
#             "section_title": "Background",
#             "paragraphs": ["This is the background paragraph."],
#             "subsections": [
#                 {
#                     "section_title": "Background2",
#                     "paragraphs": ["This is the background paragraph."]
#                 },
#                 {
#                     "section_title": "Methods",
#                     "paragraphs": ["This is a method paragraph."]
#                 }
#             ]
#         },
#         {
#             "section_title": "Methods",
#             "paragraphs": ["This is a method paragraph."]
#         }
#     ]
# }
# '''

# 将 JSON 转换为纯文本
# text = json_to_text(json_data)
# print(text)

# 定义数据集的空列表，用于存储数据
data = []

# 指定包含 JSON 文件的目录
json_dir = './gov-report/crs'

# 遍历目录下的所有 JSON 文件
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as file:

            json_data = json.load(file)
            
            # 提取 section_title、highlight 和 report 字段的内容
            id = json_data['id']
            title = json_data['title']
            released_date = json_data['released_date']
            summary = json_data['summary']
            # print(json_data['reports'])
            report_text = json_to_text(json_data['reports'])
            
            # 将数据添加到数据集列表中
            data.append({'input': f"File id: {id}\n released date: {released_date}\n {title}\n {report_text}", 'output': summary})
            # print({'input': f"File id: {id}\n released date: {released_date}\n {title}\n {report_text}", 'output': summary})
            # exit(0)

# 将数据集列表转换为 Pandas DataFrame
dataset = pd.DataFrame(data)

# 可选择将数据集保存为 CSV 文件
dataset.to_csv('llama_dataset.csv', index=False)

