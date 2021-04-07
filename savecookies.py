import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome(executable_path="assets/chromedriver89.exe")
browser.get('https://www.instagram.com')

sleep(5)

user = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')

passw = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')

user.send_keys('zkrom1234@gmail.com')
passw.send_keys('NcJ4cEAz*_8[3LDJ')

login_button_ = browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]')

login_button_.click()
sleep(5)

pickle.dump(browser.get_cookies(), open("assets/cookies.pkl", "wb"))
