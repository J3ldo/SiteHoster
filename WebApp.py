import os
import socket
import datetime
import threading
import traceback

def render_template(template):
    with open(f"templates/{template}") as f:
        return "<h1></h1>" + f.read().strip('\n')

def get_file(file):
    if os.path.exists("./static/"+file):
        with open("./static/"+file, 'rb') as f:
            f_data = f.read()

        return True, f_data
    return False, 0

class WebApp:
    def __init__(self):
        self.routes = {}


    def route(self, *args):
        def inner(func):
            if len(args) <= 0:
                raise Exception('You need to pass the route of the url.')
            elif self.routes.get(args[0]) is not None:
                raise Exception("Route already exists")

            self.routes[args[0]] = {'func': func, 'methods': args[1] if len(args) > 1 else ['GET']}

        return inner


    #print(socket.gethostbyname(socket.gethostname()))
    def listen(self, clientdata, addr, debug):
        listening = True
        while listening:
            try:
                msg = clientdata.recv(4096).decode()
            except ConnectionAbortedError:
                print("Connection broken with:", addr)
                break

            if msg == "":
                continue


            msg = msg.split("\n")
            request_headers = {}
            for i in msg:
                try:
                    out = i.strip("\r").split(": ")
                    request_headers[out[0]] = out[1]
                except:
                    continue

            location = msg[0].split()[1]
            method = msg[0].split()[0]
            response_code = 500

            if self.routes.get(location) is not None:
                if method not in self.routes[location]['methods']:
                    response_code = 405
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Method not allowed'
                        '\n\n'
                        'Method not allowed'.encode()
                    )


                try:
                    response_code = 200
                    clientdata.send(
                        f'HTTP/1.0 {response_code} OK'
                        '\n\n'
                        f'{self.routes[location]["func"]()}'.encode()
                    )
                except Exception:
                    response_code = 500
                    if debug:
                        response_code = 500
                        clientdata.send(
                            f'HTTP/1.0 {response_code} Server error'
                            '\n\n'
                            f'<h1>Error log</h1>\n<h4>{traceback.format_exc()}<h4>'.encode()
                        )
                    elif not debug:
                        clientdata.send(
                            f'HTTP/1.0 {response_code} Server Error'
                            '\n\n'
                            f'Something went wrong.'.encode()
                        )
            else:
                is_file = get_file(location)
                if is_file[0]:
                    response_code = 200
                    clientdata.send(
                        f'HTTP/1.1 {response_code} OK\n'
                        f"Content-Type: image/jpeg\n"
                        "Accept-Ranges: bytes\n\n".encode()
                    )
                    clientdata.send(is_file[1])

                else:
                    response_code = 404
                    clientdata.send(
                        f'HTTP/1.0 {response_code} Not Found'
                        '\n\n'
                        '<h1>404 not found</h1>'.encode()
                    )

            print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - HTTP '{location}' {response_code} - {addr[0]}")
            clientdata.close()
            listening = False



    def start(self, ip , port, debug=False):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PORT = port  # 80
        IP = ip  # "0.0.0.0"
        s.bind((IP, PORT))
        print(f"Listening on: http://{socket.gethostbyname(socket.gethostname() if IP == '0.0.0.0' else IP)}:{PORT}")

        s.listen()
        while True:
            clientdata, addr = s.accept()

            thread = threading.Thread(target=self.listen, args=(clientdata, addr, debug,))
            thread.start()
