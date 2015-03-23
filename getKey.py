import sys;
import urllib;
from html.parser import HTMLParser
from pip._vendor.requests.packages import urllib3
import zlib;
class JavFreeTag_Parser(HTMLParser):
    def __init__(self):
        self.url=[];
        self.nextUrl='';
        self.page_start=False;
        self.title_start=False;
        self.post_start=False;
        HTMLParser.__init__(self);
    def handle_starttag(self, tag, attrs):
        if tag=='ul' and len(attrs)>0:
            if 'hfeed posts-default clearfix' in attrs[0]:
                self.post_start=True;
        if tag=='h3' and self.post_start:
            self.title_start=True;
        if tag=='a' and self.title_start:
            self.url.append(attrs[0][1]);
        if tag=='div' and 'wp-pagenavi' in attrs[0]:
            self.page_start=True;
        if tag=='a' and self.page_start:
            if 'nextpostslink' in attrs[1]:
                self.nextUrl=(attrs[0][1]);
    def handle_endtag(self, tag):
        if tag=='ul' and self.post_start:
            self.post_start=False;
        if tag=='h3' and self.title_start:
            self.title_start=False;
        if tag=='div' and self.page_start:
            self.page_start=False;
    def reinit(self):
        self.url=[];
        self.nextUrl='';
        self.page_start=False;
        self.title_start=False;
        self.post_start=False;
def getKeysFromJavFree(url):
    jftp=JavFreeTag_Parser();
    html=urllib.request.urlopen(url).read();
#     html=zlib.decompress(html, 16+zlib.MAX_WBITS);
    jftp.feed(html.decode());
    urls=jftp.url;
    while len(jftp.nextUrl)!=0:
        response=urllib.request.urlopen(jftp.nextUrl);
        html=response.read();
        if response.info().get('Content-Encoding')=='gzip':
            html=zlib.decompress(html, 16+zlib.MAX_WBITS);
        jftp.url=[];
        jftp.nextUrl='';
        jftp.feed(html.decode());
        urls+=jftp.url;
    return urls;
def getKey(url):
    urls=getKeysFromJavFree(url);
    keys=[];
    for l in urls:
        cutPos=l.rfind('/');
        keys.append(l[cutPos+1:]);
    return keys;