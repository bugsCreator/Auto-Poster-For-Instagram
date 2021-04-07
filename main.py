import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import scraper


def GetPageLinks(url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.headless = True
    browser = webdriver.Chrome( executable_path="assets/chromedriver89.exe")
    browser.get('https://www.google.com')
    cookies = pickle.load(open("assets/cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get(url)

    action = ActionChains(browser)
    action.key_down(Keys.SPACE).send_keys(Keys.SPACE).key_up(Keys.SPACE).perform()
    sleep(1)
    action.key_down(Keys.SPACE).send_keys(Keys.SPACE).key_up(Keys.SPACE).perform()
    sleep(2)
    action.key_down(Keys.SPACE).send_keys(Keys.SPACE).key_up(Keys.SPACE).perform()
    sleep(2)
    action.key_down(Keys.SPACE).send_keys(Keys.SPACE).key_up(Keys.SPACE).perform()
    sleep(2)
    divs = browser.find_elements_by_class_name('Nnq7C.weEfm')

    for div in divs:
        linkd = div.find_elements_by_tag_name("a")

        for linksing in linkd:
            urrl = linksing.get_property("href")
            scraper.AddPost(urrl)

    browser.quit()


urlset = [#"https://www.instagram.com/ghantaa/",
          "https://www.instagram.com/singles.society/",
          "https://www.instagram.com/shinchan.meme/",
          "https://www.instagram.com/_life.of.student_/"]

for urle in urlset:
    GetPageLinks(urle)
