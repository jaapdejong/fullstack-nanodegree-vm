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
            output = ""
            output += "<html>"
            output += " <body>"

            restaurants = session.query(Restaurant).all()
            for restaurant in restaurants:
                output += restaurant.name
                output += "  <a href='#'>Edit</a>"
                output += "  <a href='#'>Delete</a>"
                output += "</br>"

            output += " </body>"
            output += "</html>"
            self.wfile.write(output)
            print output
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

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
