import requests
import time
import re

class Zanma():

    def __init__(self):
        self.token = self.get_token()
        print("token:",self.token)

    def get_token(self):
        url =  "http://47.107.130.26:9180/service.asmx/UserLoginStr?name=qiao5174&psw=qiao@5174"
        res = requests.get(url)
        token  = res.text
        return token


    def get_phone(self):
        url = "http://47.107.130.26:9180/service.asmx/GetHM2Str?token=" + self.token +"&xmid=931&sl=1&lx=0&a1=&a2=&pk=&ks=0&rj=0"
        res = requests.get(url)
        phone = res.text.split("=")[1]
        print("phone:",phone)
        return phone


    def get_smscode(self,phone):
        url = "http://47.107.130.26:9180/service.asmx/GetYzm2Str?token=" + self.token + "&hm=" + str(phone) + "&xmid=931&sf=0"
        # print(url)

        request_cnt = 0
        while True:
            res = requests.get(url)
            msg = res.text
            print("msg:",msg)
            request_cnt = request_cnt + 1
            if  len(msg) >6 :
                smscode = re.findall(r'\d+', msg)[-1]
                return smscode

            if request_cnt > 20 :
                print("max try times,but fail ....")
                return 0
            time.sleep(5)



    def release_phone(self,phone):
        url = "http://47.107.130.26:9180/service.asmx/sfHmStr?token=" + self.token + "&hm=" + phone
        res = requests.get(url)
        print(res.text)


    def main(self):

        phone = self.get_phone()
        while True:
            msg = self.get_smscode(phone)
            if len(msg)  > 1:
                print(msg)
                break
            time.sleep(6)

if __name__ == '__main__':
    zm = Zanma()
    # zm.get_token()
    # zm.get_phone()

    zm.main()

