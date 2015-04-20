from flask import Flask
from flask import request
from flask import render_template
from flask import Markup
from HTMLParser import HTMLParser
from collections import Counter
from operator import itemgetter
import requests
import json


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.container = []
        self.div_wrap = Markup("")

    def handle_starttag(self, tag, attrs):
        self.container.append("<%s>" % tag)
        attrs_string = ''
        if attrs:
            for attr in attrs:
                str = '%s="%s" ' % (attr[0], attr[1])
                attrs_string = attrs_string + str
            if attrs_string and attrs_string[-1] == " ":
                attrs_string = attrs_string[:-1]
            tag_string =  Markup.escape('<%s %s>' % (tag, attrs_string))
        else:
            tag_string = Markup.escape('<%s>' % tag)
        self.div_wrap = self.div_wrap + Markup('<span class="slack-%s">' % tag) + \
                        tag_string + Markup('</span>')

    def handle_data(self, data):
        self.div_wrap = self.div_wrap + Markup.escape(data)

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    url = request.form['text']
    r = requests.get(url)
    page_source = r.text
    parser = MyHTMLParser()
    parser.feed(page_source)
    tag_counter = Counter(parser.container)
    return render_template('tags.html', tags=sorted(tag_counter.items(), key=itemgetter(0)),
                       content=parser.div_wrap)


if __name__ == '__main__':
    app.run()