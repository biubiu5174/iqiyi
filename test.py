from upload import youtube_upload
import hashlib
yu = youtube_upload()
email = "jesusblaney3957@gmail.com"



password = hashlib.md5(email.strip().encode('utf-8')).hexdigest()[0:13]
print(password)

f_cookie = open("youtube_cookie", "r")
for line in f_cookie.readlines():
    if email == eval(line)["email"]:
        cookie = eval(line)['cookie']
        print("email:", email)
        yu.keep_login_alpha(cookie)