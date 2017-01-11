#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output  = "<html>"
            output += " <body>"
            output += " <a href='/create'>Create</a>"
            output += " </br>"

            restaurants = session.query(Restaurant).all()
            for restaurant in restaurants:
                output += restaurant.name
                output += "  <a href='%d/update'>Update</a>" % restaurant.id
                output += "  <a href='%d/delete'>Delete</a>" % restaurant.id
                output += "  </br>"

            output += " </body>"
            output += "</html>"
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/create"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output  = "<html>"
            output += " <body>"

            output += "  <form method='POST' enctype='multipart/form-data' action='/restaurants/create'>"
            output += "   <h2>Restaurant to add</h2>"
            output += "   <input name='restaurant' type='text'>"
            output += "   <input type='submit' value='Add'>"
            output += "  </form>"

            output += " </body>"
            output += "</html>"
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/update"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            fields = self.path.split("/")
            restaurantId = fields[1]
            output  = "<html>"
            output += " <body>"

            output += "  <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/update'>" % restaurantId
            output += "   <h2>New name</h2>"
            output += "   <input name='restaurant' type='text'>"
            output += "   <input type='submit' value='Update'>"
            output += "  </form>"

            output += " </body>"
            output += "</html>"
            self.wfile.write(output)
            print output
            return

        if self.path.endswith("/delete"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            fields = self.path.split("/")
            restaurantId = fields[1]
            output  = "<html>"
            output += " <body>"

            output += "  <form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantId
            output += "   <h2>Are you sure?</h2>"
            output += "   <input type='submit' value='Yes'>"
            output += "  <input class='button' type='button' onclick=\"window.location.replace('/restaurants')\" value='Cancel' />"
            output += "  </form>"

            output += " </body>"
            output += "</html>"
            self.wfile.write(output)
            print output
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/create"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    newName = messagecontent[0]
                    print "newName =", newName

                    restaurant = Restaurant(name = newName)
                    session.add(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/update"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                    newName = messagecontent[0]
                    fields = self.path.split("/")
                    restaurantId = fields[2]
                    print "id =", restaurantId
                    print "newName =", newName

                    restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
                    restaurant.name = newName
                    session.add(restaurant)
                    session.commit() 

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    fields = self.path.split("/")
                    restaurantId = fields[2]
                    print "id =", restaurantId

                    restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
                    session.delete(restaurant)
                    session.commit() 

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
