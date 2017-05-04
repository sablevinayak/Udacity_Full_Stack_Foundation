from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "&#161Hola! "
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
        except IOError:
            self.send_error(404, 'File not found: %s'% self.path)

    # def do_POST(self):
    #     try:
    #         self.send_response(301)
    #         self.send_header("Content-Type", "text/html; charset=utf-8")
    #         self.end_headers()
    #         ctype, pdict = cgi.parse_header(self.headers['content-type'])
    #         print("Hello: " + ctype)
    #         pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
    #         print(pdict['boundary'])
    #         if ctype == 'multipart/form-data':
    #             print("In if")
    #             #fields = cgi.parse_multipart(self.rfile, pdict)
    #             fields = self.rfile.read(int(self.headers['content-length']))
    #             print("Field are: "+fields)
    #             messagecontent = fields.get('message')
    #         output = ""
    #         output += "<html><body>"
    #         output += " <h2> Okay, how about this: </h2>"
    #         output += "<h1> %s </h1>" % messagecontent[0]
    #         output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
    #         output += "</body></html>"
    #         print("out")
    #         self.wfile.write(output.encode())
    #         print(output)
    #
    #     except:
    #         pass
    #         print("Fail")

    def do_POST(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')[0].decode('utf-8')
        output = ''
        output += '<html><body>'
        output += '<h2> Okay, how about this: </h2>'
        output += '<h1> %s </h1>' % messagecontent
        output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
        output += '</html></body>'
        self.wfile.write(output.encode('utf-8'))

if __name__ == '__main__':
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Webserver running on port %s" % port)
        server.serve_forever()
    except(KeyboardInterrupt):
        print('^C entered, stopping web server...')
        server.socket.close()

