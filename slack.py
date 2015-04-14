import urllib2
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    container = []

    def handle_starttag(self, tag, attrs):
        return self.container.append("<%s>" % tag)

    def handle_endtag(self, tag):
        return self.container.append("</%s>" % tag)

response = urllib2.urlopen("http://google.com")
page_source = response.read()
parser = MyHTMLParser()
parser.feed(page_source)
print parser.container
