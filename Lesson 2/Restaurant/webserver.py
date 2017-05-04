from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sqlite3
conn = sqlite3.connect("restaurantmenu.db")
c = conn.cursor()
class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                c.execute('SELECT * FROM restaurant')
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                #print(c.fetchall())
                # for row in c.fetchall():
                #     print(row[1])
                output = ""
                output += "<html><body>"
                for row in c.fetchall():
                    output +='<h1>'+row[1]+'</h1>'
                    output += "<h2><a href=restaurant/%s/edit>Edit</a></h2>" %row[0]
                    output += "<h2><a href=restaurant/%s/delete>Delete</a></h2>" %row[0]
                    output += '<br><br>'
                output += "<h2><a href=/restaurant/new>Create new restaurant</a></h2>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                #print(output)

                return
            if self.path.endswith("/edit"):
                restaurantId = self.path.split("/")
                #print(restaurantId)
                restaurantId = restaurantId[2]
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += '<h2> Enter the restaurant name </h2>'
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'><input name='newName' type='text'><input type='submit' value='Rename'></form>" %restaurantId
                output += "</body></html>"
                self.wfile.write(output.encode())
                #print(output)
                return
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                restaurantId = self.path.split("/")[2]
                c.execute("SELECT name FROM restaurant WHERE id="+restaurantId)
                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/%s/delete'><h2>Are you sure you want to delete %s<br><input type='submit' value='Delete'></h2.</form>" % (restaurantId , c.fetchall()[0][0])
                output += "</body></html>"
                print("done /delete")
                self.wfile.write(output.encode())
                #print(output)
                return
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Location', '/restaurant')
                # self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Create new restaurant"
                output += '<h2> Enter the restaurant name </h2>'
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><input name='restaurantName' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                #print(output)
                return
        except IOError:
            self.send_error(404, 'File not found: %s'% self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/new"):
                print("do_post")
                self.send_response(301)
                self.send_header('Location', '/restaurant')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Create new restaurant"
                output += '<h2> Enter the restaurant name </h2>'
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant'><input name='restaurantName' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurantName')[0].decode('utf-8')
                print("Passed if")
                c.execute('INSERT into restaurant(name) VALUES ("'+messagecontent+'")')
                conn.commit()
                print(messagecontent)
                self.wfile.write(output.encode())
                print(output)
            if self.path.endswith('/edit'):
                self.send_response(301)
                self.send_header('Location', '/restaurant')
                self.end_headers()
                restaurantId = self.path.split("/")[2]
                print(restaurantId)
                output = ""
                output += "<html><body>"
                output += '<h2> Enter the restaurant name </h2>'
                output += "<form method='POST' enctype='multipart/form-data' action='/edit'><input name='newName' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('newName')[0].decode('utf-8')
                print("Passed if")
                print(name)
                c.execute('UPDATE restaurant SET name = "'+name+'" where id ='+restaurantId)
                #print("Executed")
                conn.commit()
                self.wfile.write(output.encode())

            if self.path.endswith("/delete"):
                self.send_response(301)
                self.send_header('Location', '/restaurant')
                self.end_headers()
                restaurantId = self.path.split("/")

                c.execute("DELETE FROM restaurant WHERE id="+restaurantId[1])
                conn.commit()

        except Exception as e:
            print(e)

if __name__ == '__main__':
    try:
        c.execute('SELECT * FROM restaurant')
        # for row in c.fetchall():
        #     print(row)
        c.execute('SELECT * FROM menu_item')
        # for row in c.fetchall():
        #     print(row)
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Webserver running on port %s" % port)
        server.serve_forever()


    except(KeyboardInterrupt):
        print('^C entered, stopping web server...')
        server.socket.close()

