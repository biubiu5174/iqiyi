import os
import sys
from selenium import webdriver
import requests
import time
from datetime import datetime
import traceback
import hashlib
from selenium.webdriver.support.ui import Select
from zanma import Zanma


class youtube_upload():
    # driver = webdriver.Chrome()

    def __init__(self):
        # self.keep_login()
        # self.driver.implicitly_wait(30)
        pass

    def login_to_get_cookie(self, url):
        '''手动输入账号密码，登录获取cookie'''

        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.delete_all_cookies()
        self.driver.refresh()
        cookieBefore = self.driver.get_cookies()

        print("type:", type(cookieBefore))
        # 打印登录前的cookie
        print(cookieBefore)

        print("please enter name and code.............")
        time.sleep(90)
        print("登录后！")
        cookiesAfter = self.driver.get_cookies()
        print("type:",type(cookiesAfter))
        print(cookiesAfter)

        # 讲cookie 写入文件
        with open("cookie_file","w") as cookie_file:
            cookie_file.write(str(cookiesAfter))
        return cookiesAfter


    def keep_login(self):
        url = "https://www.youtube.com/upload"
        # 输入 cookie
        with open ("cookie_file","r") as cookie_file:
            for line in cookie_file:
                cookie = eval(line)
                print("cookie_type:",type(cookie))
                break
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        # 清除一下cookie
        self.driver.delete_all_cookies()
        time.sleep(3)
        self.driver.get(url)

        for line in cookie:
            self.driver.add_cookie(line)
        self.driver.get(url)
        self.driver.refresh()


    def keep_login_alpha(self,cookie):
        url = "https://www.youtube.com/upload"
        # 输入 cookie
        # with open ("cookie_file","r") as cookie_file:
        #     for line in cookie_file:
        #         cookie = eval(line)
        #         print("cookie_type:",type(cookie))
        #         break

        try:
            self.driver.quit()
        except:
            print("driver not exist ...")

        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        # self.driver.maximize_window()
        # 清除一下cookie
        self.driver.delete_all_cookies()
        time.sleep(3)
        self.driver.get(url)

        for line in cookie:
            self.driver.add_cookie(line)
        self.driver.get(url)
        self.driver.refresh()

        time.sleep(4)

        if self.driver.current_url == "https://www.youtube.com/upload":
            print("login in success...")
            return True
        else:
            print("login fail...")
            return False


    def upload(self,file_path,title,des,tag,thumbnail_path):
        try:
            ele = self.driver.find_element_by_css_selector('input[type ="file"]')
            self.driver.implicitly_wait(5)
        except:
            try:
                self.driver.switch_to_alert().accept()
                self.driver.refresh()
            except:
                pass

            try:
                self.driver.switch_to_alert().accept()
            except:
                pass

            self.driver.implicitly_wait(10)
            ele = self.driver.find_element_by_css_selector('input[type ="file"]')
            self.driver.implicitly_wait(10)

        try:
            ele.send_keys(file_path)

            title_ele = self.driver.find_element_by_name("title")
            title_ele.clear()
            title_ele.send_keys(title)

            desc_ele = self.driver.find_element_by_css_selector('textarea[aria-label="说明"]')
            desc_ele.clear()
            desc_ele.send_keys(des)


            tag_ele = self.driver.find_element_by_css_selector('input.video-settings-add-tag')
            tag_ele.clear()
            tag = tag.replace("[","").replace("]","").replace("'","")
            tag_ele.send_keys(tag)

        except Exception as e:
            print(e)


        is_completed = False
        start_time = datetime.now()
        thumbnail_upload = 0
        pic_chosen = 0
        while True:
            current_time = datetime.now()
            if (current_time - start_time).seconds > 1200:
                break




            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[2]/div[2]/div[1]').text
                if "正在上传您的视频" in tip:
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),tip)
                    time.sleep(3)
                    continue
            except Exception as e:
                print("big fuck....",e)
                print(traceback.print_exc())


            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[2]/div[2]/div[1]').text
                if "正在处理您的视频" in tip:
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),tip)
                    time.sleep(3)
                    continue
            except Exception as e:
                print("big fuck....",e)
                print(traceback.print_exc())

            try:
                # //*[@id="upload-item-0"]/div[2]/div[2]/div[1]
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[2]/div[2]/div[1]').text
                if "上传完毕！" in tip:
                    # try:
                    #     if pic_chosen == 0:
                    #         self.driver.find_element_by_xpath(
                    #             '//*[@id="upload-item-0"]/div[3]/div[2]/div/div/div[1]/div[3]/form/div[1]/fieldset[3]/div/span[2]/div[1]').click()
                    #         print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "chosing picture.....")
                    #         pic_chosen = 1
                    # except:
                    #     pass

                    try:
                        if thumbnail_upload == 0 and os.path.exists(thumbnail_path) == True:
                            thumbnail_btn = self.driver.find_element_by_css_selector('input[type ="file"]')
                            thumbnail_btn.send_keys(thumbnail_path)
                            thumbnail_upload = 1
                            print("上传缩略图...")

                    except Exception as e:
                        print(e)



                    self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[3]/div[1]/div[1]/div/div/button').click()
                    time.sleep(5)
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"publishing.....")
                    is_completed = True

            except:
                time.sleep(2)

            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[3]/div[1]/button/span').text
                if "返回编辑模式" in tip:
                    break
            except:
                pass

            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[1]').text
                if "该视频与您已上传的某个视频相同" in tip :
                    is_completed = True
                    print(tip)
                    print("already upload ....")
                    break
            except:
                pass


            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[3]/div[1]/div[8]/div[1]/div[2]/div').text
                if "这是私享视频" in tip:
                    is_completed = True
                    print(tip)
                    print("already upload ....")
                    break
            except:
                pass


            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[1]').text
                if "服务器拒绝了该文件" in tip:
                    is_completed = "-1"
                    print(tip)
                    print("upload limit ...")
                    break

            except:
                pass


            try:
                tip = self.driver.find_element_by_xpath('//*[@id="upload-item-0"]/div[1]').text
                if "视频处理失败" in tip:
                    is_completed = "-2"
                    print(tip)
                    print('视频处理失败')
                    break

            except:
                pass

        self.driver.refresh()
        return is_completed


    def img_download(self,img_url):
        try:
            os.remove(os.path.join(os.getcwd(),'img.jpg'))
        except:
            pass

        import requests
        try:
            r = requests.get(img_url)
            with open('img.jpg', 'wb') as f:
                f.write(r.content)
        except:
            print("there is an erro downloading picture....")
        return os.path.join(os.getcwd(),'img.jpg')


class YoutubePassport():

    #
    zm = Zanma()

    def build_channel(self,email,channel_title):
        self.driver = webdriver.Chrome()
        url = "https://www.youtube.com/upload"
        self.driver.delete_all_cookies()
        self.driver.get(url)
        self.driver.implicitly_wait(30)
        # self.driver.find_element_by_id("text").click()

        # email = "BCeSHl8D@gmail.com"
        password = hashlib.md5(email.strip().encode('utf-8')).hexdigest()[0:13]
        print(email,password)

        self.login(email,password)

        time.sleep(5)

        try:
            first_name_input = self.driver.find_element_by_xpath('//*[@id="create-channel-first-name"]')
            first_name_input.clear()
            first_name_input.send_keys(channel_title)

            last_name_input = self.driver.find_element_by_xpath('//*[@id="create-channel-last-name"]')
            last_name_input.clear()
            last_name_input.send_keys("haha")

            create_button = self.driver.find_element_by_xpath('//*[@id="create-channel-submit-button"]')
            create_button.click()

        except:
            print("there is a fuck....")
            traceback.print_exc()

        # save cookie
        time.sleep(5)
        if self.driver.current_url == "https://www.youtube.com/upload":
            print("channel created....")
            cookie = self.driver.get_cookies()

            item ={}
            item["email"] = email
            item['cookie'] = cookie
            f_cookie = open("youtube_cookie", "a+")
            f_cookie.write(str(item)+"\n")
            f_cookie.close()

        else:
            print("not the upload page")

        self.driver.quit()



    def login(self,email,password):

        # self.driver.get("https://accounts.google.com/")

        email_input = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email_input.send_keys(email)

        next_step = self.driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span')
        next_step.click()

        time.sleep(2)

        password_input = self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
        password_input.send_keys(password)

        next_step = self.driver.find_element_by_class_name('CwaK9')
        next_step.click()

        time.sleep(2)
        # self.driver.find_element_by_xpath("//*[contains(text(), '个人信息')]").click()
        # self.driver.find_element_by_xpath(
            # '//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/c-wiz/c-wiz/div/div[3]/c-wiz/div/a[2]/div[2]').click()
        # time.sleep(2)


    def account_vertify(self,email):

        # open url
        options = webdriver.ChromeOptions()
        options.add_argument('lang=en-US.UTF-8')
        self.driver = webdriver.Chrome(chrome_options=options)
        # self.driver = webdriver.Chrome()
        url = "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fapp%3Ddesktop%26hl%3Dzh-CN%26action_handle_signin%3Dtrue%26next%3D%252F&hl=zh-CN&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
        self.driver.delete_all_cookies()

        self.driver.get(url)
        self.driver.implicitly_wait(30)

        # self.driver.find_element_by_xpath('//*[@id="button"]').click()
        password = hashlib.md5(email.strip().encode('utf-8')).hexdigest()[0:13]

        print("email:",email)
        print("password:",password)

        # login in account
        self.login(email,password)

        self.driver.get("https://www.youtube.com/features")

        time.sleep(3)
        if "已验证" in self.driver.page_source:
            return 0

        try:
            self.driver.find_element_by_xpath('//*[@id="creator-page-content"]/div[2]/div[1]/div[1]/div[2]/div[2]/a').click()

        except:
            print("element not found ...")
            self.driver.quit()
            return 0

        select = Select(self.driver.find_element_by_id("country-code-select"))
        select.select_by_value("CN")

        self.driver.find_element_by_xpath('//*[@id="input-phone-number-form"]/fieldset/ul/li[2]/label').click()


        # phone input
        phone = self.zm.get_phone()

        self.driver.find_element_by_id("phone-number-input").send_keys(phone)

        self.driver.find_element_by_xpath('//*[@id="verification-submit-section"]/button').click()

        smscode = self.zm.get_smscode(phone)

        # enter smscode
        self.driver.find_element_by_xpath('//*[@id="verification-code-input"]').send_keys(smscode)
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="verification-submit-section"]/button').click()   # submit smscode

        time.sleep(5)
        self.driver.quit()





    def main(self):

        f_cr = open("channel_relation")
        i = 0
        for line in f_cr.readlines():
            # if i <= 14 :
            #     i = i + 1
            #     continue
            title = eval(line)['title']
            email = eval(line)['email']
            # password = hashlib.md5(email.strip().encode('utf-8')).hexdigest()[0:13]
            # self.build_channel(email,title)

            self.account_vertify(email)





class upload_worker():

    videos_path = os.path.abspath(os.path.join(os.getcwd(), "..", "multi_channel_dl"))
    print(videos_path)

    yu = youtube_upload()

    def main(self):
        f_cookie = open("youtube_cookie","r")
        for line in f_cookie.readlines():
            email = eval(line)["email"]
            cookie = eval(line)['cookie']
            print("email:",email)

            login_result = self.yu.keep_login_alpha(cookie)
            # 判断是否登录成功
            if login_result != True:
                continue


            print()
            result = ""
            upload_cnt = 0

            f_channel_relation = open("channel_relation","r")
            for item in f_channel_relation.readlines():
                if eval(item)["email"] == email:
                    print("yes",email)
                    channel_url = eval(item)['url']



                    f_channel_info = open("channel_info","r")
                    for s_line in f_channel_info.readlines():
                        #  check up load times
                        if upload_cnt > 90:
                            continue

                        if result == "-1":
                            print("hahah")
                            break

                        if eval(s_line)["url"] not in  channel_url:
                            continue

                        info = eval(s_line)["info"]
                        for video_item in info:
                            video_name = video_item["title"]
                            video_link = video_item['video_link']
                            img_link = video_item['img_link']
                            full_video_name = self.get_title_by_url(video_link)   # get title from download log
                            if full_video_name is not None:
                                video_path = os.path.join(self.videos_path,full_video_name + ".f4v")
                                new_video_name = os.path.join(self.videos_path, "(upload)" + full_video_name +".f4v")


                                # 判断文件是否已经上次
                                if os.path.exists(new_video_name):
                                    print(email ,"already upload....")
                                    continue

                                # 判断文件是否存在
                                if not os.path.exists(video_path):
                                    print(video_path)
                                    print("video not exist...")
                                    continue



                                img_path = self.yu.img_download(img_link)
                                dec = ""
                                title = full_video_name.replace("高清正版视频在线观看–爱奇艺","").replace("-搞笑-","")
                                tag = "电影解说,电视剧解说,电影,电视剧,搞笑"
                                print(video_path,img_link,title)


                                result = self.yu.upload(video_path,title,dec,tag,img_path)

                                print("result:" ,result)

                                # 改变文件名
                                #
                                if result == True or result == "-2":
                                    # new_video_name = os.path.join(self.videos_path, "(upload)"+full_video_name)
                                    os.rename(video_path,new_video_name)
                                    upload_cnt = upload_cnt + 1


                                # 服务器拒绝 当天上传限制
                                if result == "-1":

                                    break

                                if result == "-2":
                                    continue

                            else:
                                print('fuck')

                    break

            f_channel_relation.close()
        f_cookie.close()



    def get_title_by_url(self,video_url):

        dl_log_path = os.path.join(os.getcwd(),"IqiyiParser","main_dl_log")

        f_log = open(dl_log_path,"r")
        for line in f_log.readlines():
            url = line.strip().split("####")[0]
            video_title = line.strip().split("####")[1]
            if url == video_url:
                f_log.close()
                return video_title
        return None

if __name__ == '__main__':
    # upload = youtube_upload()
    # yp = YoutubePassport()
    # yp.build_channel("omyatd@gmail.com","")
    # yp.account_vertify("BCeSHl8D@gmail.com")

    # yp.main()
    #
    uw = upload_worker()
    uw.main()
