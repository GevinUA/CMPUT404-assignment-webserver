#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



notFound404= '''
        <!DOCTYPE html>
        <html>
            <body>404 Not Found</body>
        </html>
'''

notAllowed405 = '''
        <!DOCTYPE html>
        <html>
            <body>Method Not Allowed</body>
        </html>
'''

class MyWebServer(socketserver.BaseRequestHandler):

    pathName = ''
    fileName = ''
    preName = ''
    formatName = ''
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        #to store the request
        contentRequest = self.data.decode('utf-8').split()

        requestMethod = contentRequest[0]
        requestObject = contentRequest[1]



        if(requestMethod != "GET"):
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n"+notAllowed405,'utf-8'))

        if("../" in requestObject or "~" in requestObject):
            self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\nContent-Type: text/html\r\n\r\n"+notFound404,'utf-8'))


        if(os.path.isfile("./www"+requestObject)): #if the file exists
            self.splitPath_and_File(requestObject)
            self.splitNameandFormat(self.fileName)
            
            self.send("./www"+requestObject)
            
        else:  #if the file does not exist
            if self.validDir("./www"+requestObject): #if this is not file, but a valid dir

                if(requestObject[-1] != '/'):
                    newLocation = "http://127.0.0.1:8080"+requestObject+'/'

                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: " + newLocation + "\r\nContent-Type: text/html\r\n\r\n",'utf-8'))
                else:
                    self.formatName = "html" #reset the format name bacause self.format is empty
                    self.send("./www"+requestObject+"index.html")

            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not FOUND\r\nContent-Type: text/html\r\n\r\n"+notFound404,'utf-8'))


    def validDir(self,dir):
        return os.path.isdir(dir)


    def splitPath_and_File(self,requestObject):
        self.pathName, self.fileName = os.path.split(requestObject)

        #/index.html ->   /   index.html


    def splitNameandFormat(self, fileName):
        self.preName, self.formatName = os.path.splitext(fileName)
        self.formatName = self.formatName[1:]

        #index.html  ->  index

    def send(self, openFile):
        with open(openFile,'r') as f:
                self.request.sendall(bytearray(f"HTTP/1.1 200 OK\r\nContent-Type: text/{self.formatName}\r\n\r\n"+f.read(),'utf-8'))
        return
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
