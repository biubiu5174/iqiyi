import os

class channel_relation():

    def get_channel_group(self):
        """
        channel title
        channel group
        channel
        :return:
        """
        gmail = []
        f_gmail_list = open("gmail_list","r")
        for line in f_gmail_list.readlines():
            email = eval(line)["email"]
            gmail.append(email)



        channel_item = {}
        i = 0
        temp_info = []
        f = open("qualified_log","r")
        for line in f.readlines():
            if  len(line) > 4:
                temp_info.append(line)
            else:
                channel_item['title'] = temp_info[0].split(" ")[0].split("，")[0]
                channel_item['url'] = []
                channel_item['email'] = gmail[0]
                gmail.remove(gmail[0])
                for item in temp_info:
                    channel_item['url'].append(item.split(" ")[1].strip())
                temp_info = []
                print(channel_item)
                channel_item = {}
                i = i + 1
                # print(i)






if __name__ == '__main__':
    cr = channel_relation()
    cr.get_channel_group()