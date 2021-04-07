import re
import os
import pickle
import sqlite3
import urllib.request
from time import sleep
from sqlite3 import Error
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def db_create_connection():
    path = "C:\\Users\\hjh\\PycharmProjects\\memes_bot\\assets\\sm_app.sqlite"
    connection = None
    try:
        connection = sqlite3.connect(path)
        connection.execute(
            'CREATE TABLE posts ( id INTEGER PRIMARY KEY AUTOINCREMENT , post_id TEXT NOT NULL , name TEXT NOT NULL, author TEXT NOT NULL , type TEXT NOT NULL , added INTEGER NOT NULL,deleted INTEGER NOT NULL, caption TEXT NOT NULL )')
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    connection.commit()
    connection.close()


def db_updateToAdded(id):
    connection = sqlite3.connect("C:\\Users\\hjh\\PycharmProjects\\memes_bot\\assets\\sm_app.sqlite")
    connection.execute("UPDATE `posts` SET  `added` = 1 WHERE `post_id`='" + str(id) + "'")
    connection.commit()
    connection.close()


def db_Exe_query(query):
    connection = sqlite3.connect("C:\\Users\\hjh\\PycharmProjects\\memes_bot\\assets\\sm_app.sqlite")
    connection.execute(query)
    connection.commit()
    connection.close()


def db_insertdata(data):
    postid = data["postid"]
    name = data["name"]
    type = data["type"]
    caption = data["caption"]
    author = data["author"]
    connection = sqlite3.connect("C:\\Users\\hjh\\PycharmProjects\\memes_bot\\assets\\sm_app.sqlite")
    connection.execute(
        str(
            "INSERT INTO posts ( `post_id`, `name`, `author`,`type`,`added`,`deleted`, `caption`) VALUES ( '" + str(
                postid) + "', '" + str(name) + "', '" + str(author) + "', '" + str(type) + "',0 ,0,'" + str(
                caption) + "')"))
    connection.commit()
    connection.close()


def db_rowTolist(postdetail):
    data = {
        "id": postdetail[0],
        "postid": postdetail[1],
        "name": postdetail[2],
        "type": postdetail[4],
        "deleted": postdetail[6],
        "author": postdetail[3],
        "caption": postdetail[7],
        "added": postdetail[5]

    }
    return data


def db_select(query):
    connection = sqlite3.connect("C:\\Users\\hjh\\PycharmProjects\\memes_bot\\assets\\sm_app.sqlite")
    data = list()
    cur = connection.cursor()
    cur.execute(query)
    datalists = cur.fetchall();
    for datalist in datalists:
        data.append(db_rowTolist(datalist))

    return data;


def db_GetAll():
    return db_select("SELECT * FROM posts WHERE `added`= 0")


def db_deleteAddedData():
    data = db_select("SELECT * FROM posts WHERE `added`= 1 &`deleted` = 0 ")
    for mdata in data:
        print(mdata['name'])
        if os.path.exists(str("row/") + mdata['name']):
            id = mdata['id']
            os.remove(str("row/") + mdata['name'])
            db_Exe_query("UPDATE `posts` SET  `deleted` = 1 WHERE  `id`='" + str(id) + "'")

        else:
            print("The file does not exist")
        print("")


def db_DeleteAnPost(postid):
    query = "DELETE FROM `posts` WHERE `post_id`='" + str(postid) + "';"
    db_Exe_query(query)


def DeleteFile(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


def lately_savecoockies():
    url = 'https://inter.latelysocial.com/auth/login'
    options = Options()
    options.headless = True

    browser = webdriver.Chrome(chrome_options=options, executable_path="assets/chromedriver89.exe")
    browser.get(url)
    user = browser.find_element_by_xpath('/html/body/section/div/form/div/div[1]/input')

    passw = browser.find_element_by_xpath('/html/body/section/div/form/div/div[2]/input')
    rmbercb = browser.find_element_by_xpath('/html/body/section/div/form/div/div[3]/label[1]/span[1]')

    user.send_keys('jay916622@gmail.com')
    passw.send_keys('NcJ4cEAz*_8[3LDJ')
    rmbercb.click()
    login_button_ = browser.find_element_by_xpath('/html/body/section/div/form/div/button')

    login_button_.click()
    sleep(5)

    pickle.dump(browser.get_cookies(), open("assets/lately_cookies.pkl", "wb"))
    browser.quit()


def lately_post(filename, caption_text):
    url = 'https://www.google.com/'
    options = Options()
    options.headless = True
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.headless = True
    browser = webdriver.Chrome(executable_path="assets/chromedriver89.exe")
    browser.get(url)
    cookies = pickle.load(open("assets/lately_cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get('https://inter.latelysocial.com/instagram/post')
    sleep(5)
    slectac = browser.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[2]/ul/li/a/div[2]/label')
    slectac.click()
    uploadinput = browser.find_element_by_xpath('//*[@id="fileupload"]')
    path = os.path.abspath(filename)
    uploadinput.send_keys(path)
    sleep(13)
    caption = browser.find_element_by_xpath(
        '//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/div[4]/div[2]/div[1]')

    caption.send_keys(str(caption_text.encode()))
    submit = browser.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/button[1]')
    sleep(3)
    browser.execute_script(
        'm = document.querySelector("#body-main > div.wrap-main > div.app-content.open.container-fluid > form > div > div.am-wrapper > div.am-content.col-md-6.am-scroll.pl15.pr15");m.scroll(100, 500)')
    submit.click()
    sleep(4)
    browser.quit()
    print("all done bro")


def lately_addstatus(filename):
    url = 'https://www.google.com/'
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(chrome_options=options, executable_path="assets/chromedriver89.exe")
    browser.get(url)
    cookies = pickle.load(open("assets/lately_cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
    browser.get('https://inter.latelysocial.com/instagram/post')
    sleep(5)
    slectac = browser.find_element_by_xpath('//*[@id="body-main"]/div[2]/div[4]/form/div/div[2]/ul/li/a/div[2]/label')
    slectac.click()
    story = browser.find_element_by_xpath(
        '//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/div[1]/div/a[2]')
    story.click()
    uploadinput = browser.find_element_by_xpath('//*[@id="fileupload"]')
    path = os.path.abspath(filename)
    uploadinput.send_keys(path)
    sleep(20)
    submit = browser.find_element_by_xpath(
        '//*[@id="body-main"]/div[2]/div[4]/form/div/div[3]/div[1]/div[3]/button[1]')
    submit.click()
    sleep(4)
    browser.quit()
    print("all done bro")


def Enquiry(lis1):
    if not lis1:
        return 1
    else:
        return 0


def AlreadyExist(id):
    query = "SELECT * FROM `posts` WHERE `post_id`='" + str(id) + "';"
    a = db_select(query)
    if Enquiry(a):
        return False
    else:
        return True


def filter_caption(stri):
    Tweet = re.sub('@[^\s]+', '', stri)
    Tweet = re.sub('#s[^\s]+', '', Tweet)
    return Tweet


def IsVideo(webdriver):
    sleep(2)
    allright = 0
    try:
        webdriver.find_element_by_tag_name("video")
        allright = allright + 1
    except NoSuchElementException:
        try:
            webdriver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div/div/video')
            allright = allright + 1
        except NoSuchElementException:
            allright = allright - 1

    if allright >= 1:
        return True
    else:
        return False


def DownloadVideo(browser, id):
    video = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/div/article/div[2]/div/div/div[1]/div/div/video')
    uri = video.get_property("src")
    ids = str("row/") + str(id) + str(".mp4")

    urllib.request.urlretrieve(uri, ids)


def DownloadImage(browser, id):
    image = browser.find_element_by_class_name('FFVAD')
    # '//*[@id="react-root"]/section/main/div/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img'
    uri = image.get_property("src")
    ids = str("row/") + str(id) + str(".jpg")
    urllib.request.urlretrieve(uri, ids)


def AddPost(url):
    post = list();
    options = Options()
    # options.headless = True
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.headless = True
    browser = webdriver.Chrome(executable_path="assets/chromedriver89.exe")

    browser.get(url)
    id = url.split("/")[4]
    if AlreadyExist(id):
        pass
    else:
        name = ""
        type = ""
        caption = ""
        author = ""
        try:
            author = browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a').text
        except NoSuchElementException:
            author = ' '
        try:
            browser.find_element_by_tag_name("video")
            DownloadVideo(browser, id)
            type = "video"
            name = str(url.split("/")[4]) + str(".mp4")
            try:
                caption_block = browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')

                caption = filter_caption(caption_block.text)
            except NoSuchElementException:
                caption = " "
        except NoSuchElementException:
            DownloadImage(browser, id)
            type = "picture"
            name = str(url.split("/")[4]) + str(".jpg")

            try:
                caption_block = browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span')
                caption = filter_caption(caption_block.text)
            except NoSuchElementException:
                caption = " "

        post.append({
            "postid": id,
            "author": author,
            "name": name,
            "type": type,
            "caption": caption
        })
        db_insertdata(post[0])
        browser.quit()


def GetUrlToId(url):
    id = str(url.split("/"))
    return id[4]


def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return round(size / pow(2, 20), 2)


def DeleteMore2Mb():
    posts = db_select("SELECT * FROM posts")
    for post in posts:
        id = post['postid']
        name = post["name"]
        size = get_file_size("row/" + str(name))
        if size > 1.99:
            DeleteFile("row/" + str(name))
            db_DeleteAnPost(id)
            print("Deleted :" + str(id))


def CaptionBuilder(id):
    query = "SELECT * FROM posts WHERE `post_id`= '" + str(id) + "'"
    posts = db_select(query)
    post = posts[0]
    author = post["author"]
    caption = post['caption']
    rcation = "                   Credit :- @" + str(author) + "" + "" + str(
        caption) + "" + "                              Follow For More Memes    @memes_wala_bot         @memes_wala_bot    @memes_wala_bot" + "" + "#memes #mamas #memesdaily #dankmemes #funnymemes #dailymemes #offensivememes #memes😂 #edgymemes #memestagram #animememes #followforfollow #likeforlike #f4f #l4l #fortnitememes #spicymemes #memesespañol #memesbrasil #indianmemes #instamemes #adultmemes #memesforlife #lovememes #newmemes #funny #lol #meme #memestagramm #memespages #qualitymemes #stupidmemes #memesforfun" + " #instamemes #funny #funnymemes #dankmemes #offensivememes #edgymemes #spicymemes #nichememes #memepage #funniestmemes #dank #memesdaily #jokes #memesrlife #memestar #memesquad #humor #lmao #igmemes #lol #memeaccount #memer #relatablememes #funnyposts #sillymemes #nichememe #memetime"
    return rcation


def AutoPost():
    posts = db_GetAll()
    for post in posts:
        id = post['postid']
        name = post["name"]
        lately_post("row/" + str(name), CaptionBuilder(id))
        db_updateToAdded(id)
