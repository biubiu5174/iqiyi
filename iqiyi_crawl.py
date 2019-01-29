from selenium import webdriver
import os
import time
from multiprocessing import Pool
import traceback
# from IqiyiParser.main import Download


# from langconv import *

class IQIYI():

    """
    抓取某一个系列的视频信息
    """

    driver = webdriver.Chrome()

    download_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "download")
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    f_log = open("log", "a+")

    def main(self,url):
        self.driver.implicitly_wait(30)
        self.driver.get(url)

        clip_info = []


        elements = self.driver.find_element_by_class_name("albumAllset-li").find_elements_by_tag_name("li")
        print(len(elements))



        for ele in elements:
            self.driver.find_element_by_class_name("albumAllset-btn").click()
            time.sleep(1)
            ele.click()
            time.sleep(3)

            item_list = self.driver.find_element_by_class_name("piclist-wrapper").find_elements_by_tag_name("li")

            for item in item_list:
                title = item.find_element_by_class_name("site-piclist_pic_link").get_attribute("title")
                link = item.find_element_by_class_name("site-piclist_pic_link").get_attribute("href")
                num_title = item.find_element_by_class_name("site-piclist_info_title").text

                name = "哆啦A梦" + "-" + title +" " + num_title
                # name = self.chs_to_cht(name)
                print(name)

                info = {"name":name,"link":link}
                # clip_info.append(info)
                self.f_log.write(str(info)+"\n")



    def download(self,name,link):
        cmd = """you-get -o %s -O "%s" %s""" % (self.download_dir,name,link)
        print(cmd)
        p = os.popen(cmd)
        print(p.read())


    def download_worker(self):
        f = open("log","r")

        pool = Pool(processes = 3)

        for line in f.readlines():
            name = eval(line)["name"]
            link = eval(line)["link"]
            print(name,link)
            pool.apply_async(self.download,(name,link,))

        pool.close()
        pool.join()


    # 简体转繁体
    def chs_to_cht(self,line):
        line = Converter('zh-hant').convert(line)
        line.encode('utf-8')
        return line



class CrawlByWords():
    """
    根据关键词 抓取对应的视频
    """


    driver = webdriver.Chrome()

    iqiyi_crawl_log = os.path.join(os.getcwd(),"iqiyi_crawl_log")
    f_log = open(iqiyi_crawl_log,"a+")


    def crawl_by_url(self, url):
        # url = "http://so.iqiyi.com/so/q_%E6%80%BB%E8%A3%81?source=history&sr=531967950092"

        self.driver.get(url)
        self.driver.implicitly_wait(30)

        # self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/a[3]").click()
        # self.driver.find_element_by_xpath('//*[@id="af-elem-trigger"]').click()
        # self.driver.find_element_by_xpath('//*[@id="af-elem-content"]/div[1]/div/ul[2]/li[2]/a').click()
        # self.driver.find_element_by_xpath('//*[@id="af-elem-content"]/div[2]/ul/li[2]/a').click()


        list_item = self.driver.find_elements_by_class_name("list_item")
        print("length:",len(list_item))

        for ele in list_item:

            ele_source = str(ele.get_attribute("innerHTML"))
            # print(str(ele_source))
            if "专辑" in ele_source or "导演:" in ele_source or "主演:" in ele_source  or "发布时间" not in ele_source:
                continue

            link = ele.find_element_by_tag_name("a").get_attribute("href")

            name = ele.get_attribute("data-widget-searchlist-tvname")
            print(name)

            summary = ""
            if "简介" in ele_source :
                summary = ele.find_element_by_class_name("result_info_txt").text

            duration_text = ele.find_element_by_class_name("icon-vInfo").text.split(":")
            duration = int(duration_text[0])*60 + int(duration_text[1])

            pic = ele.find_element_by_tag_name("img").get_attribute("src")

            # print(link,name,summary,duration,pic)

            res = {"link":link,"name":name,"summary":summary,"duration":duration,"pic":pic}
            print(res)
            self.f_log.write(str(res)+"\n")


    def crawl_worker(self):

        n =20
        f = open("key_word.txt","r")

        for line in f.readlines():
            word = line.strip()

            for page_num in range(1,n):
                url = "http://so.iqiyi.com/so/q_" + word + "_page_" +str(page_num) + "_site_iqiyi" + "_ctg_电视剧_"
                self.crawl_by_url(url)


# https://so.iqiyi.com/so/q_%E6%80%BB%E8%A3%81_ctg_%E7%94%B5%E8%A7%86%E5%89%A7_t_0_page_1_p_1_qc_0_rd__site_iqiyi_m_11_bitrate_?af=true



class IqiyiChannel():
    f_channel_info = open("channel_info", "a+")

    f_driver = webdriver.Chrome()
    s_driver = webdriver.Chrome()

    def get_all_channel(self):
        driver = self.f_driver


        info = []
        for i in range(1,10):
            url = "https://list.iqiyi.com/www/22/29139-------------24-%s--iqiyi--.html" % str(i)
            driver.get(url)
            driver.implicitly_wait(30)
            # init_len = len(info)
            elements = driver.find_elements_by_class_name("site-piclist_info_title")
            for ele in elements:
                title = ele.find_element_by_tag_name("a").get_attribute("title")
                link = ele.find_element_by_tag_name("a").get_attribute("href")
                print(title,link)
                item = {"title":title,"link":link}
                if item not in info:
                    info.append(item)
                self.get_channel_info(link)


    def get_channel_info(self,channel_url):

        driver = self.s_driver

        driver.get(channel_url)
        try:
            pages = driver.find_element_by_id("album_paging").find_elements_by_tag_name("a")
            print(len(pages))
            page_nums = []
            for item in pages:
                try:
                    txt = item.get_attribute("data-key")
                    print(txt)
                    page_nums.append(int(txt))
                except:
                    pass
            try:
                max_num = max(page_nums)
            except:
                max_num = 1

            print("page:",max_num)

            channel_title = driver.find_element_by_class_name("info-intro-title").text
            video_cnt = 0
            ele_info = []
            for i in range(0,max_num):
                ele_list = driver.find_element_by_id("albumpic-showall-wrap").find_elements_by_tag_name("li")
                for ele in ele_list:

                    video_link = ele.find_element_by_class_name("site-piclist_pic_link").get_attribute("href")
                    title = ele.find_element_by_class_name("site-piclist_pic_link").get_attribute("title")
                    img_link = ele.find_element_by_tag_name("img").get_attribute("src")
                    item_info = {"video_link":video_link,"title":title,"img_link":img_link}
                    if item_info not in ele_info:
                        ele_info.append(item_info)
                    video_cnt = video_cnt + 1

                try:
                    driver.find_element_by_link_text('下一页').click()
                except:
                    pass



            channel_info = {}
            channel_info["url"] = channel_url
            channel_info["info"] = ele_info
            channel_info["video_cnt"] = video_cnt
            channel_info["title"] = channel_title
            print(channel_info)
            print("video_cnt",video_cnt)
            self.f_channel_info.write(str(channel_info)+"\n")

        except Exception as e:
            print(e)
            traceback.print_exc()



    def analysis(self):
        info = open("channel_info","r")

        for line in info:
            line = eval(line)
            video_cnt = line["video_cnt"]
            title = line["title"]
            if video_cnt >80:
                print(title,video_cnt)

    def dl_channel_video(self):

        all_info = [] # 需要下载的url

        f = open("log","r")
        channel_title = []
        for line in f.readlines():
            channel_title.append(line.split(" ")[0])

        f_iqiyi_log = open("channel_info","r")
        for line in f_iqiyi_log.readlines():
            line = eval(line)
            title = line["title"]
            info = line["info"]
            if title in channel_title:
                print(title)
                for item in info:
                    single_item = {}
                    single_item["url"] =item["video_link"]

                    single_item["title"] = item["title"]
                    print(single_item)
                    all_info.append(single_item)

        dl = Download()
        dl.common_dl(all_info,"/mnt/d/DRIVE CAR/multi_channel_dl")







# /mnt/d/DRIVE CAR/multi_channel_dl


if __name__ == '__main__':
    # url = "https://www.iqiyi.com/a_19rrk25kq9.html"
    # qiyi = IQIYI()
    # qiyi.download_worker()
    # iqiyi.download("jahahd","https://www.iqiyi.com/v_19rrk32v68.html")

    # cbw = CrawlByWords()
    # cbw.crawl_worker()


    ic = IqiyiChannel()
    ic.get_all_channel()
    # ic.get_channel_info("https://www.iqiyi.com/a_19rrh5iao1.html#vfrm=2-4-0-1")
    # ic.analysis()
    # ic.dl_channel_video()