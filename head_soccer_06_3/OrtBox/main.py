__author__ = 'Dylan'

import urllib , urllib2 , urllib3 , cookielib , json

cookieJar = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))


def login(username,password):
    url = "http://campus.almagro.ort.edu.ar/ajaxactions/LogearUsuario"
    form = {"u" : username,"c" : password}

    encodedForm = urllib.urlencode(form)
    request = urllib2.Request(url, encodedForm)
    page = opener.open(request)
    return page.read()

def request(url):
    form = {}
    encodedForm = urllib.urlencode(form)
    request = urllib2.Request(url, encodedForm)
    page = opener.open(request)
    return page.read()

def main():

    data = login(41396500,"1221dylan")
    print data

    datason = json.loads(data)

    print request("http://campus.almagro.ort.edu.ar/ajaxactions/GetLoggedInData")
main()