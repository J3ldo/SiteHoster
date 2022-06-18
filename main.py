from flask import Flask, render_template
import os, shutil


class Configreader:
    def __init__(self, splitwith="="):
        self.splitwith = splitwith

    def readfile(self, filepath):
        with open(filepath, 'r') as f:
            filecontents = [i.strip('\n') for i in f.readlines()]

        out = {}
        for line in filecontents:
            try:
                out[line.split('=')[0]] = line.split('=')[1]
            except IndexError:
                pass

        return out

config = Configreader().readfile("config.ini")
app = Flask(__name__)

routeid, routes = 0, []
temprouteid = 0
class Createroute:
    def __init__(self, route, file):
        routes.append([route, file])
        global routeid
        self.id = routeid
        temprouteid = routeid


        @app.route(routes[temprouteid][0])
        def newroute():
            with app.app_context():
                return render_template(routes[temprouteid][1])

        newroute()
        routeid += 1

if __name__ == '__main__':
    if not os.path.exists("templates"): os.mkdir("templates")
    if not os.path.exists("static"): os.mkdir('static')

    for i in os.listdir(f"{config['sitedirectory']}"):
        if os.path.isdir(f"{config['sitedirectory']}/{i}"):
            continue
        elif i.endswith(".html"):
            shutil.copy(f"{config['sitedirectory']}/{i}", "templates")
            Createroute(f"/{i.split('.html')[0]}" if i != "index.html" else "/", i)
        else:
            shutil.copy(f"{config['sitedirectory']}/{i}", "static")


    try:
        app.run(config["ip"], int(config["port"]), debug=True if config["debug"] == "True" else False)
    finally:
        if os.path.exists("static"): os.rmdir('static')
        if os.path.exists("static"): os.rmdir('templates')
