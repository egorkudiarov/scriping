import json
import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pprint import pprint
from logger import logger

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
DELAY = 250 #Что бы исправить selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found in the current frame


chrome_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_path)
options = ChromeOptions()
#options.add_argument('--headless')
browser = Chrome(service=browser_service, options=options)

#Функция взята с вебинара по занятию
@logger('log_getting_web_elements.log')
def wait_element(browser, delay=5, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located((by, value))
    )


browser.get('https://habr.com/ru/articles/')
articles_list = browser.find_elements(by=By.CLASS_NAME, value='tm-article-body')

links = []
for article in articles_list:
    link = wait_element(browser=article, by=By.CLASS_NAME, value='tm-article-snippet__readmore') \
            .get_attribute('href')
    links.append(link)


parsed_data = []
for link in links:
    browser.get(link)  
    title = wait_element(browser=browser, delay=DELAY, by=By.CSS_SELECTOR, value='.tm-title.tm-title_h1 span').text.strip()
    post_time = wait_element(browser=browser, delay=DELAY, by=By.CSS_SELECTOR, value='.tm-article-datetime-published time').get_attribute('title')
    article = wait_element(browser=browser, delay=DELAY, by=By.CSS_SELECTOR, value='.article-formatted-body > div ')
    articles_list = article.find_elements(By.TAG_NAME, value='p')
    articles_list += article.find_elements(By.TAG_NAME, value='li')
    for element in articles_list:
        text = element.text.lower()
        if any([text.find(keyword) for keyword in KEYWORDS]):
            parsed_data.append({
                'title': title,
                'link': link,
                'time': post_time,
                'text': text
            })  
            break


for data in parsed_data:
    print(f'<{data.get("time").split(", ")[0]}>-<{data.get("title")}>-<{data.get("link")}>')