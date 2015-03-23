__author__ = 'newtonis'
# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import cookielib
import hashlib
import json

def login(username,password,opener):
    action   = "http://trophymanager.com/qs"
    url = "http://trophymanager.com/ajax/login.ajax.php"
    form = {"user" : username,"password" : password}

    encodedForm = urllib.urlencode(form)
    request = urllib2.Request(url, encodedForm)
    page = opener.open(request)

def get_forum_topic_users(url,opener):
    form = {}
    encodedForm = urllib.urlencode(form)

    request = urllib2.Request(url, encodedForm)
    page = opener.open(request)

    contents = page.read()

    h = contents.rfind('var user_names') + 16
    h2 = contents.rfind("var timestamps")

    user_names = ""
    while (h < h2-2):
        user_names = user_names + contents[h]
        h+=1
    user_data_strings = []
    for x in range(2,len(user_names)):

        if user_names[x] == "{":
            x+=1

            user_data_strings.append("{")
            d = 1
            while (d != 0):
                if (user_names[x] == "{"):
                    d+=1
                elif (user_names[x] == "}"):
                    d-=1
                user_data_strings[len(user_data_strings)-1] = user_data_strings[len(user_data_strings)-1] + user_names[x]
                x+=1


    for x in range(len(user_data_strings)):
        print user_data_strings[x]
    return user_names

def main():
    cookieJar = cookielib.LWPCookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

    login("newtonis1.penguin1@gmail.com","lalala",opener)
    data = get_forum_topic_users("http://trophymanager.com/forum/ar/off-topic/212065/",opener)
    print data
main()