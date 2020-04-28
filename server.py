import tornado.web
import tornado.ioloop
import random
import string
import os
import subprocess
import mysql.connector 

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Irac123456789",
    database="videoserver"
) 

mycursor = mydb.cursor()

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class uploadVideo(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('vname', '')
        author = self.get_argument('aname', '') 

        print(name)
        files = self.request.files["fileVideo"]
        for f in files:
            code = randomString()
            os.mkdir(f"video/"+ code)
            fh = open(f"video/"+code+"/"+code+".mp4", "wb")
            fh.write(f.body)
            fh.close()
            subprocess.Popen(['./generator.sh', code])
            sql = "INSERT INTO video (id, name, author, duration) VALUES (%s, %s, %s, %s)"
            val = (code, name, author, "00:00")
            mycursor.execute(sql, val)
            mydb.commit()   


class videoHandler(tornado.web.RequestHandler):
    def put(self):
        print("video put")
        id = self.get_argument('id','')
        self.render("./public/video.html", id = id)

    def get(self):
        print("video get")
        id = self.get_argument('id','')
        sql = "SELECT * FROM video WHERE id = %s"
        mycursor.execute(sql, (id,))
        items = mycursor.fetchall()[0]

        print(items[1])
        self.render("./public/video.html", items=items)


class indexHandler(tornado.web.RequestHandler):
    def post(self):
        print("do post")
        self.render("./public/index.html")

    def get(self):
        print("do get")
        mycursor.execute("SELECT * FROM video")
        items = mycursor.fetchall()
        self.render("./public/index.html", items = items)

if (__name__ == "__main__"):
    app = tornado.web.Application([
        ("/", indexHandler),
        ("/upload", uploadVideo),
        ("/video", videoHandler),
        (r"/data/(.*)", tornado.web.StaticFileHandler, {'path': "./data/"}),
        ("/js/(.*)", tornado.web.StaticFileHandler, {'path': "./public/js/"}),
    ])



    app.listen(8080, max_body_size=200 * 1024 * 1024)
    print("Listening on port 8080")
    tornado.ioloop.IOLoop.instance().start()
