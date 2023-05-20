from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def connection(addr):
    try:
        print("开始连接chrome，chromedriver地址：" + addr)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        wd = webdriver.Chrome(service=Service(addr), options=chrome_options)
        print("连接chrome成功")
        return wd
    except Exception as e:
        print("请确保使用调试模式打开chrome，并重启程序%s" % e)
wd = connection(addr = r"D:\accessDatabase\chromedriver.exe",)
wd.implicitly_wait(10)
def is_homepage():
    try:
        elements = WebDriverWait(wd, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-901oao'))
        )
        print("具有类名'css-901oao'的元素数量:", len(elements))
        found_element = None
        for element in elements:
            if element.text == "主页":
                found_element = element
                break
        if found_element:
            print("找到文本内容为'主页'的元素")
        else:
            print("未找到文本内容为'主页'的元素")
    except:
        print("Twitter is not open")

def article():
    pass
    article_tags = wd.find_elements(By.TAG_NAME, "article")
    print("找到的<article>标签数量:", len(article_tags))
    def check(text, strings):
        for string in strings:
            if string in text:
                return True
        return False

    for article in article_tags:
        # print(article.text)
        # 推文中是否有空投信息
        drop = check(article.text, ("抽奖","Airdrop","泵"))
        # 判断推文是否点赞"
        like_status = article.find_elements(By.CSS_SELECTOR,"[role='button']")
        if len(like_status) >0:
            like = like_status[3]
            data_testid = like.get_attribute("data-testid")
            print(data_testid)
        else:
            print("未找到喜欢")
        # 根据文本内容，筛选出空投信息，并点击进入推文
        try:
            if drop:
                if data_testid == "like":
                    #点赞
                    like.click()
                    #转载
                    like_status[2].click()
                    wd.find_element(By.XPATH,"//*[text()='转推']").click()
                    #点击进入推文
                    article.find_element(By.CSS_SELECTOR,'data-testid="tweetText"').click()
                    #关注相关用户
                    related = wd.find_element(By.XPATH,"//*[text()='相关用户']").find_element(By.XPATH,"../../../..")
                    follow = related.find_element(By.XPATH,"//*[text()='关注']")
                    follow.click()
                    #关注右边栏提供的推特
                else:
                    print("已点过赞")
            else:
                print("没有空投信息")
        except:
            print("点击进入推文出错")
        print("---")

is_homepage()
article()