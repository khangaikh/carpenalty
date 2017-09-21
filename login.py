# -*- coding: utf-8 -*- 

import mechanize
import sys
import urllib2
from BeautifulSoup import BeautifulSoup
from pytesseract import image_to_string 
from PIL import Image


reload(sys)  
sys.setdefaultencoding('utf8')

br = mechanize.Browser()
response = br.open('https://torguuli.police.gov.mn/')
soup = BeautifulSoup(response.get_data())
img = soup.find('img', id='img')
image_response = br.open_novisit(img['src'])
image = image_response.read()

save = open("yourcaptcha.png", 'wb')
save.write(image)
save.close()

cap = image_to_string(Image.open('yourcaptcha.png'),config='digits -psm 7')

br.select_form(nr = 0)
br.form['plateNumber'] = str(sys.argv[1])
br.form['captcha'] = cap
response = br.submit()

form_result = response.read()
parsed_html = BeautifulSoup(form_result)
print parsed_html.body.find('ul', attrs={'class':'list-group'})
