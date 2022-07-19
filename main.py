import os, shutil
from WebApp import WebApp, render_template


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
app = WebApp()

routeid, routes = 0, []
temprouteid = 0
class Createroute:
    def __init__(self, route, file):
        routes.append([route, file])
        global routeid
        self.id = routeid


        @app.route(routes[self.id][0])
        def newroute():
            return render_template(routes[self.id][1])


        routeid += 1

def into_new_dir(full_path):
    for i in os.listdir(full_path):
        if os.path.isdir(f"{full_path}/{i}"):
            return into_new_dir(f"{full_path}/{i}")

        elif i.endswith(".html"):
            shutil.copy(f"{full_path}/{i}", "templates")
            Createroute(f"/{full_path[-len(config['sitedirectory']):]}/{i.split('.html')[0]}", i)
        else:
            shutil.copy(f"{full_path}/{i}", "static")



if __name__ == '__main__':
    if not os.path.exists("templates"): os.mkdir("templates")
    if not os.path.exists("static"): os.mkdir('static')

    for i in os.listdir(f"{config['sitedirectory']}"):
        full_path = f"{config['sitedirectory']}/{i}"

        if os.path.isdir(full_path):
            into_new_dir(full_path)

        elif i.endswith(".html"):
            shutil.copy(full_path, "templates")
            Createroute(f"/{i.split('.html')[0]}" if i != "index.html" else "/", i)
        else:
            shutil.copy(full_path, "static")


    try:
        app.start(config["ip"], int(config["port"]), debug=True if config["debug"] == "True" else False)
    finally:
        if os.path.exists("static"): os.rmdir('static')
        if os.path.exists("static"): os.rmdir('templates')
