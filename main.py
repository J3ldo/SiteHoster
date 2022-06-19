from flask import Flask, render_template
import os
import shutil


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
    def __init__(self, route, file, fromdir=False):
        routes.append([route, file])
        global routeid
        self.id = routeid
        temprouteid = routeid

        try:
            if fromdir:
                print({}["test"])  #Crash intentionally to start the exception.

            @app.route(routes[temprouteid][0])
            def newroute():
                with app.app_context():
                    return render_template(routes[temprouteid][1])

            newroute()  #Create the app route
        except:
            @app.route(routes[temprouteid][0])
            def newroute2():
                with app.app_context():
                    return render_template(routes[temprouteid][1])

            newroute2() #Create the app route if its in an directory.

        routeid += 1


def go_into_dir(full_path):
    for i in os.listdir(full_path):
        old = full_path
        full_path +="/"+i
        all_dirs =  full_path[len(config['sitedirectory']):]
        all_dirs = all_dirs[:-len(i)]


        if os.path.isdir(full_path):
            go_into_dir(full_path)
            continue

        elif i.endswith(".html"):
            current_path = "templates/"
            template_path = ""
            for b in all_dirs.split("/"):
                if len(b) != 0:
                    try:
                        os.mkdir(current_path+b)
                        current_path += b+"/"
                        template_path += b + "/"
                    except FileExistsError:
                        current_path += b + "/"
                        template_path += b + "/"

            shutil.copy(full_path, "templates"+all_dirs)
            Createroute(f"{all_dirs}{i.split('.html')[0]}", template_path+i, True)

        else:
            current_path = "static/"
            for b in all_dirs.split("/"):
                if len(b) != 0 and not b.endswith(".html"):
                    try:
                        os.mkdir(current_path+b)
                        current_path += b+"/"
                    except FileExistsError:
                        current_path += b + "/"

            print(current_path, all_dirs)
            shutil.copy(full_path, "static"+all_dirs)

        full_path = old


if __name__ == '__main__':
    if not os.path.exists("templates"): os.mkdir("templates") #Create the directories template and static
    if not os.path.exists("static"): os.mkdir('static')

    for i in os.listdir(f"{config['sitedirectory']}"):
        full_path = f"{config['sitedirectory']}/{i}"

        if os.path.isdir(full_path):
            go_into_dir(full_path)

        elif i.endswith(".html"):
            shutil.copy(full_path, "templates")
            Createroute(f"/{i.split('.html')[0]}" if i != "index.html" else "/", i)
        else:
            shutil.copy(full_path, "static")

    try:
        app.run(config["ip"], int(config["port"]), debug=True if config["debug"] == "True" else False)  #Run the app using the prefered config.
    finally:
        if os.path.exists("static"):
            shutil.rmtree('static') #Remove the static and templates
        
        if os.path.exists("templates"):
            shutil.rmtree('templates')
