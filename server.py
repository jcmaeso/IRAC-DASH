import tornado.web
import tornado.ioloop
import random
import string
import os
import subprocess
import mysql.connector 
import threading
import codecs

from base64 import b64encode

import secrets

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Irac123456789",
    database="videoserver"
) 

mycursor = mydb.cursor()
cond = threading.Condition()

class videoStack:
    def __init__(self):
        self.videos_to_process = []

class convertingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.videos = []

    def run(self):
        while(True):
            while(len(self.videos) != 0):
                self.List
 
class deleteHandler(tornado.web.RequestHandler):
    def get(self):

        print("do delete get")
        sql = "DELETE FROM video WHERE id=%s"
        id = self.get_argument('id','')
        print(id)
        mycursor.execute(sql, (id,))
        subprocess.Popen(['rm','-rf', './data/'+id])
        self.redirect('/')


    def post(self):
        print("do delete get")
        sql = "DELETE FROM video WHERE id=%s"
        id = self.get_argument('id','')
        print(id)
        mycursor.execute(sql, (id,))
        subprocess.Popen(['rm','-rf', './data/'+id])
        self.redirect('/')

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

            KEY = secrets.token_hex(16)
            KID = secrets.token_hex(16)
            KEY64 = codecs.encode(codecs.decode(KEY, 'hex'), 'base64') [:-1]
            KID64 = codecs.encode(codecs.decode(KID, 'hex'), 'base64') [:-1]
            
            print("KID: "+str(KID64))
            print("KEY: "+str(KEY64))


            subprocess.Popen(['./generator.sh', code, KEY, KID])
            sql = "INSERT INTO video (id, name, author, duration, key1, key2) VALUES (%s, %s, %s, %s,%s,%s)"
            val = (code, name, author, "00:00", KEY64, KID64)
            mycursor.execute(sql, val)
            mydb.commit()   

        self.redirect('/')

    def get(self):
        self.render("./public/form.html")

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

class drmService(tornado.web.RequestHandler):

    def get(self):
        print("Get the DRM Keys")
        key = list(self.request.arguments)[0]
        #print("KID::::"+ key)

        sql = "SELECT * from video where key2 like \"{}%\"".format(key)
        print(sql)
        mycursor.execute(sql)
        items = mycursor.fetchall()[0]
        print(items[4])
        print(items[5])
        self.write({
        "keys":
            [{
            "kty":"oct",
            "k":items[4],
            "kid":items[5],
            }],
        'type':"temporary"
        })


class indexHandler(tornado.web.RequestHandler):
    def post(self):
        print("do post")
        self.render("./public/index.html")

    def get(self):
        print("do get")
        mycursor.execute("SELECT * FROM video")
        items = mycursor.fetchall()
        self.render("./public/index2.html", items = items)

if (__name__ == "__main__"):
    app = tornado.web.Application([
        ("/", indexHandler),
        ("/upload", uploadVideo),
        ("/video", videoHandler),
        ("/drm/",drmService),
        (r"/data/(.*)", tornado.web.StaticFileHandler, {'path': "./data/"}),
        ("/js/(.*)", tornado.web.StaticFileHandler, {'path': "./public/js/"}),
        ("/css/(.*)", tornado.web.StaticFileHandler, {'path': "./public/css/"}),
        ("/delete",deleteHandler)
    ])



    app.listen(8080, max_body_size=200 * 1024 * 1024)
    print("Listening on port 8080")
    tornado.ioloop.IOLoop.instance().start()
