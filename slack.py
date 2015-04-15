from flask import Flask
from flask import request
from flask import render_template
from HTMLParser import HTMLParser
from collections import Counter
import urllib2
from bs4 import BeautifulSoup


class MyHTMLParser(HTMLParser):
    container = []

    def handle_starttag(self, tag, attrs):
        return self.container.append("<%s>" % tag)

    def handle_endtag(self, tag):
        return self.container.append("</%s>" % tag)


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    response = urllib2.urlopen(text)
    page_source = response.read()
    soup = BeautifulSoup(page_source)
    pretty_html = soup.prettify()
    parser = MyHTMLParser()
    parser.feed(page_source)
    c = Counter(parser.container)
    return render_template('tags.html', tags=c, content=pretty_html)


if __name__ == '__main__':
    app.run(debug=True)