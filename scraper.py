import pycurl # used to execute curl in python
import urllib # used to format parameters into a http url
import StringIO # library used to store curl results\
from bs4 import BeautifulSoup #library for parsing html content

people = []

for x in range(0, 3):

    c = pycurl.Curl() # curl object
    url = 'http://10.254.10.164/owaspbricks/content-1/index.php?' # url we are calling
    attr = urllib.urlencode({'id': x }) # set id to 1
    url = url + attr # Get request append urlencoded parameters to url
    c.setopt(c.URL, url) # set url n curl object
    c.setopt(c.CONNECTTIMEOUT, 5) # set time call timeout to 5 secounds
    c.setopt(pycurl.FOLLOWLOCATION, 1) # if we get a location header response follow it.
    c.setopt(c.TIMEOUT, 8) # maximum amount of seconds curl is allowed to run
    b = StringIO.StringIO() # String io object
    c.setopt(c.COOKIEFILE, '') # the file to sotre the cookie data
    c.setopt(c.HTTPHEADER, ['Accept: application/html', 'Content-Type: application/x-www-form-urlencoded'])
    c.setopt(pycurl.WRITEFUNCTION, b.write)


    try:
        c.perform() # run pycurl
        html_doc = b.getvalue() #get html from StrinIO
        soup = BeautifulSoup(html_doc)
        fieldset = soup.find_all('fieldset')

        for feild in fieldset:
            user_id = feild.find_next('b').string
            user_name = feild.find_next('b').find_next('b').string
            user_email = feild.find_next('b').find_next('b').find_next('b').string
            person = {'user_id':user_id,'user_email':user_email,'user_name':user_name}
            people.append(person)

    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr

print people
