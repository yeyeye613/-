# -*- coding: utf-8 -*-
import re  # 处理正则表达式
import time
from selenium.webdriver.support import expected_conditions as EC  # 提供了一组预定义的条件，
from selenium.webdriver.support.wait import WebDriverWait  # 上通常与WebDriverWait一起使用，用于等待某个特定条件成立后再继续执行代码
from selenium import webdriver
from selenium.webdriver.common.by import By  # 定位页面元素的方法
import os
import json


def print_table():
    """打印用户界面"""
    # 数据
    data = [
        ["序号", "选项"],
        ["1", "开始登录"],
        ["2", "用户设置"]
    ]

    # 计算每列的最大宽度
    col_widths = [max(len(str(cell)) for cell in column) for column in zip(*data)]

    # 绘制表格
    print("+" + "-+-" * len(data[0]) + "+")
    for row in data:
        print("|", end="")
        for i, cell in enumerate(row):
            print(" " + str(cell).center(col_widths[i]) + " |", end="")
        print()
    print("+" + "-+-" * len(data[0]) + "+")


def write_user():
    username = input("输入账号")
    password = input("输入密码")
    line = username + " " + password
    with open("data.json", "a", encoding='utf-8') as f:
        f.write(line)


def read_browser_path_from_config():
    """从配置文件中读取浏览器路径"""

    config_file_path = "config.txt"  # 定义配置文件的路径 config_file_path 并设置为 "config.txt"。
    if os.path.exists(config_file_path):  # 使用 os.path.exists 函数检查配置文件是否存在。
        with open(config_file_path, 'r') as file:  # 如果文件存在，使用 with open 语句以只读模式打开文件，并读取所有行到 lines 变量中
            lines = file.readlines()
            for line in lines:
                if line.startswith("browser_path:"):
                    return line.split("browser_path:")[1].strip()
                # 假设配置文件 config.txt 中有一行是以 "browser_path:" 开头的，后面跟着浏览器可执行文件的路径。例如：
                # browser_path: C:\Program Files\Google\Chrome\Application\chrome.exe
    return None


def login():
    with open('data.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
        n = 1
        for i in loaded_data:
            print(n, loaded_data[i][0])
            n += 1
        action = input()
        username = loaded_data[action][1]
        password = loaded_data[action][2]
    radio_button_selector = (
        "#app > div > div.tn-body__container > div > div.van-radio-group > "
        "div > div:nth-child(1) > div.van-cell__title > span"
    )


    # 打开网页并登录
    url = "https://skl.hduhelp.com/#/english/list"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.login-button'))
    )
    # if action == '0':
    #     write_user()
    # else:
    username_input = driver.find_element(By.NAME, 'username')
    username_input.send_keys(username)

    password_input = driver.find_element(By.CSS_SELECTOR, '.ant-input[type="password"]')  # 通过CSS选择器定位密码框
    password_input.send_keys(password)  # 输入密码

    login_button = driver.find_element(By.CSS_SELECTOR, '.login-button')  # 使用CSS选择器定位登录按钮
    login_button.click()  # 点击登录按钮


def tn_answer(tn_text, answer_option="tm找不到"):
    # 使用正则表达式提取问题和选项
    global question, found, i, radio_button_selector
    question_match = re.search(r'(\d+)\s*(.+?)\s*\.', tn_text)
    options_match = re.findall(r'([A-D])\.\s*(.+)', tn_text)

    if question_match:
        question = question_match.group(2).strip()
        for i in range(len(question)):
            if 122 >= ord(question[i]) >= 65 or '\u4e00' <= question[i] <= '\u9fff':
                break
        question = question[i:]
        if "，" in question:
            question = question.replace("，", " ")

    options = {}
    if options_match:
        for match in options_match:
            options[match[0]] = match[1].strip()

    with open('四级.txt', 'r', encoding='utf-8') as answer_file:
        tn_lines = answer_file.readlines()

    for line in tn_lines:
        found = False
        for ABCD in ["A", "B", "C", "D"]:
            if question in line and options[ABCD][:-2] in line:
                answer_option = ABCD
                found = True
                break

        if found:
            if answer_option == "A":
                radio_button_selector = (
                    "#app > div > div.tn-body__container > div > div.van-radio-group > "
                    "div > div:nth-child(1) > div.van-cell__title > span"
                )

            if answer_option == "B":
                radio_button_selector = (
                    "#app > div > div.tn-body__container > div > div.van-radio-group > "
                    "div > div:nth-child(2) > div.van-cell__title > span"
                )
            if answer_option == "C":
                radio_button_selector = (
                    "#app > div > div.tn-body__container > div > div.van-radio-group > "
                    "div > div:nth-child(3) > div.van-cell__title > span"
                )
            if answer_option == "D":
                radio_button_selector = (
                    "#app > div > div.tn-body__container > div > div.van-radio-group > "
                    "div > div:nth-child(4) > div.van-cell__title > span"
                )

            radio_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, radio_button_selector))
            )
            # 点击定位到的单选按钮
            radio_button.click()
            # print(f"答案为{answer_option}")

            break
    if not found:
        # button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/div[1]/div[3]/button')
        button = driver.find_element(By.CSS_SELECTOR,
            "#app > div > div.tn-body__container > div > div.van-radio-group > "
            "div > div:nth-child(3) > div.van-cell__title > span"
        )
        button.click()

web_options = webdriver.ChromeOptions()
web_options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
driver = webdriver.Chrome(options=web_options)
print_table()
i = int(input("请输入命令"))
if i == 1:
    login()
    with open('四级.txt', 'r', encoding='utf-8') as file:
        tn_lines = file.readlines()
    input("已读取题库,回车给出当前页面答案")
    for i in range(100):
        script = "return document.body.innerText;"
        text = driver.execute_script(script)
        tn_answer(text)
        time.sleep(1)
        # WebDriverWait(driver, 10).until(
        # EC.element_to_be_clickable((By.CLASS_NAME, "van-cell van-cell--clickable"))
        # )
    print("已经作答完毕大部分题目,可以点击提交了")
    for i in range(300, -1, -1):
        # 使用 '\r' 返回行首，不换行，'end='' 确保不追加新行
        print(f"\r剩余时间: {i} 秒", end='', flush=True)
        time.sleep(1) 
    submit_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/span')
    time.sleep(2)
    submit_button.click()
    confirm_button = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/button[2]')
    confirm_button.click()
    # driver.quit() # 下一题按钮Xpath://*[@id="app"]/div/div[3]/div/div[5]/div[1]/div[3]/button
    # /html/body/div[4]/div[2]/button[2]
    input("1111")
    driver.quit()
