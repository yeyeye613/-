import re  # 处理正则表达式
import time
from selenium.webdriver.support import expected_conditions as EC  # 提供了一组预定义的条件，
from selenium.webdriver.support.wait import WebDriverWait  # 上通常与WebDriverWait一起使用，用于等待某个特定条件成立后再继续执行代码
from selenium import webdriver
from selenium.webdriver.common.by import By  # 定位页面元素的方法



def login():
    i_pause = input("在跳出的页面中自行输入账号密码并登录\n到考试页面开始考试后再回车")
    # # 定位用户名输入框并输入内容
    # username_input = driver.find_element(By.NAME, 'username')  # 通过name属性定位
    #
    # username_input.send_keys('学号')  # 输入学工号/绑定手机/证件号
    # #
    # #
    # # 定位密码输入框并输入内容
    # password_input = driver.find_element(By.CSS_SELECTOR, '.ant-input[type="password"]')  # 通过CSS选择器定位密码框
    # password_input.send_keys('密码')  # 输入密码
    # i_pause = input("回车点击登录")
    #
    # # 定位登录按钮并点击
    # login_button = driver.find_element(By.CSS_SELECTOR, '.login-button')  # 使用CSS选择器定位登录按钮
    # login_button.click()  # 点击登录按钮


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
        # 检查当前行是否同时包含两个变量
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
        # with open('output.txt', 'a', encoding='utf-8') as answer_file:
        #     answer_file.write(f"\nQuestion:{question}")
        #     for option, content in options.items():
        #         answer_file.write(f"\n{option}: {content}")
        # print("\n未找到答案")
        button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/div[1]/div[3]/button')
        button.click()


radio_button_selector = (
    "#app > div > div.tn-body__container > div > div.van-radio-group > "
    "div > div:nth-child(1) > div.van-cell__title > span"
)
web_options = webdriver.ChromeOptions()
web_options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
driver = webdriver.Chrome(options=web_options)
# 打开网页并登录
url = "https://skl.hduhelp.com/#/english/list"
driver.get(url)
timeout = 30
login()
with open('四级.txt', 'r', encoding='utf-8') as file:
    tn_lines = file.readlines()
# i_pause = input("已读取题库,回车给出当前页面答案")
for i in range(100):
    # 请求网页中所有文本
    script = "return document.body.innerText;"
    # 赋值给text
    text = driver.execute_script(script)
    # # 打印获取到的文本
    tn_answer(text)
    # button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/div[1]/div[3]/button')
    # button.click()

    # i_pause = input("回车下一题")
    time.sleep(1)
# time.sleep(240)
# submit_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[5]/div[1]/div[3]/button')
# submit_button.click()
i_pause = input("已经作答完毕大部分题目,可以点击提交了")

driver.quit()
