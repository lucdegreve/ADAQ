#!/usr/bin/env python3

import webbrowser
import subprocess
import http.server
import socketserver

port = 8000
Handler = http.server.SimpleHTTPRequestHandler

while True:
    try:
        httpd = socketserver.TCPServer(("", port), Handler)
        url = "http://localhost:"+str(port)+"/"
        
        webbrowser.open_new_tab(url+"monitoring/Temperatures1to4.html")
        webbrowser.open_new_tab(url+"monitoring/Temperatures5to8.html")
        webbrowser.open_new_tab(url+"monitoring/NH3Trap.html")
        webbrowser.open_new_tab(url+"monitoring/CVP.html")
        
        print("serving at port", str(port))
        httpd.serve_forever()
        
    except socketserver.socket.error as exc:
        print(exc.args[0])
        port+=1

