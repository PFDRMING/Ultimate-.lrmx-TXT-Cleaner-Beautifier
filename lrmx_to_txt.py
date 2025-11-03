#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸 国关哥 V6 ProMax Ultra
- 终极清理乱码 + 美化 TXT
- 支持递归文件夹
- 输出桌面并自动打开
"""

import os
import re
import html
import random
import subprocess

# ------------------------------
# 基本清理函数
# ------------------------------
def clean_text_basic(s):
    s = html.unescape(s)
    s = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', s)
    s = s.replace('\uFFFD','')
    s = s.replace('\r\n','\n').replace('\r','\n')
    s = re.sub(r'\n{3,}','\n\n', s)
    s = re.sub(r'[ \t]{2,}', ' ', s)
    return s.strip() + '\n'

def remove_english_letters(text):
    return re.sub(r'[A-Za-z]', '', text)

# ------------------------------
# 删除 / + 并清理超长数字
# ------------------------------
def remove_slash_plus_and_superlong_numbers(text, length_threshold=10):
    text = text.replace('/', '').replace('+', '')

    def replace_long(match):
        num = match.group()
        if 6 <= len(num) <= 8:
            return num
        else:
            return ''
    pattern = r'\d{' + str(length_threshold + 1) + r',}'
    return re.sub(pattern, replace_long, text)

# ------------------------------
# 删除尖括号标签
# ------------------------------
def remove_angle_brackets(text):
    return re.sub(r'<.*?>', '', text)

# ------------------------------
# 美化文本
# ------------------------------
EMOJI_LIST = ["🌸","🌹","✨","💠","🗓️","💐","🔥","🎉","📄"]

def beautify_text(text):
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = re.sub(r'[ \t]+', ' ', line.strip())
        if not line:
            cleaned_lines.append('')
            continue
        emoji = random.choice(EMOJI_LIST)
        line = f"{emoji} {line}"
        cleaned_lines.append(line)
    final_text = '\n'.join(cleaned_lines)
    final_text = re.sub(r'\n{2,}', '\n\n', final_text)
    return final_text

# ------------------------------
# 单文件处理
# ------------------------------
def process_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

    text = clean_text_basic(text)
    text = remove_english_letters(text)
    text = remove_slash_plus_and_superlong_numbers(text, length_threshold=10)
    text = remove_angle_brackets(text)
    text = beautify_text(text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"✅ 已生成 {output_path}")

# ------------------------------
# 递归处理文件夹
# ------------------------------
def process_folder(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        rel_path = os.path.relpath(root, input_folder)
        out_dir = os.path.join(output_folder, rel_path)
        for file in files:
            if file.lower().endswith('.lrmx'):
                in_path = os.path.join(root, file)
                out_file = f"✅{os.path.splitext(file)[0]}.txt"
                out_path = os.path.join(out_dir, out_file)
                process_file(in_path, out_path)

# ------------------------------
# 主程序
# ------------------------------
if __name__ == "__main__":
    print("🌸 欢迎使用 国关哥 V6 ProMax Ultra 🌸")
    folder = input("💬 请输入包含 .lrmx 文件的文件夹路径：").strip()
    if not folder or not os.path.isdir(folder):
        print("⚠️ 路径不存在，请检查")
        exit(1)

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_base = os.path.join(desktop, os.path.basename(folder))
    os.makedirs(output_base, exist_ok=True)

    process_folder(folder, output_base)

    print(f"🎉 所有文件已处理完毕，输出在：{output_base}")
    # 自动打开新生成文件夹
    subprocess.run(["open", output_base])
    print("🚀 已自动打开输出文件夹，国关哥可以直接查看啦 🌸🌹✨")
