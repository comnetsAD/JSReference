from os import path
import sys
import requests
import jsbeautifier
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import colorsys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, Tag

colors = ["#efba43","ea8032","#f28791","#e55b3f","#f6ba78","#c6312d","#000000"]
index = random.randint(0,len(colors)-1)

def hex_to_rgb(hex):
	 hex = hex.lstrip('#')
	 hlen = len(hex)
	 return tuple(int(hex[i:i+hlen/3], 16) for i in range(0, hlen, hlen/3))

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
	global index

	c = colors[index]
	index = (index+1)%len(colors)

	return hex_to_rgb(c)

driver = webdriver.Chrome()
driver.get(sys.argv[1])

# files = ["http://yasirzaki.net/wp-content/plugins/contact-form-plugin/css/form_style.css?ver=4.0.9","http://yasirzaki.net/wp-content/plugins/gallery-plugin/css/frontend_style.css?ver=4.9.11","http://yasirzaki.net/wp-content/plugins/gallery-plugin/fancybox/jquery.fancybox.min.css?ver=4.9.11","http://yasirzaki.net/wp-content/plugins/google-analytics-for-wordpress/assets/js/frontend.min.js?ver=7.0.5","http://yasirzaki.net/wp-content/plugins/papercite/js/papercite.js?ver=4.9.11","http://yasirzaki.net/wp-content/plugins/papercite/papercite.css?ver=4.9.11","http://yasirzaki.net/wp-content/plugins/vertical-news-scroller/css/newsscrollcss.css","http://yasirzaki.net/wp-content/themes/identity/genericons/genericons.css?ver=3.3.0","http://yasirzaki.net/wp-content/themes/identity/js/identity.js?ver=20150504","http://yasirzaki.net/wp-content/themes/identity/js/navigation.js?ver=20120206","http://yasirzaki.net/wp-content/themes/identity/js/skip-link-focus-fix.js?ver=20130115","http://yasirzaki.net/wp-content/themes/identity/style.css?ver=4.9.11","http://yasirzaki.net/wp-includes/css/dashicons.min.css?ver=4.9.11","http://yasirzaki.net/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1","http://yasirzaki.net/wp-includes/js/jquery/jquery.js?ver=1.12.4","http://yasirzaki.net/wp-includes/js/wp-embed.min.js?ver=4.9.11"]
features = [".lookupPrefix",".prefix",".childNodes",".open",".isEqualNode",".documentURI",".lastChild",".nodeName",".title",".implementation",".normalizeDocument",".forms",".input",".anchors",".createCDATASection",".URL",".getElementsByTagName",".createEntityReference",".domConfig",".createElement",".xmlStandalone",".referrer",".textContent",".doctype",".namespaceURI",".strictErrorChecking",".xmlEncoding",".appendChild",".domain",".createAttribute",".links",".adoptNode",".Type",".nextSibling",".firstChild",".images",".close",".xmlVersion",".event",".form",".createComment",".removeChild",".nodeValue",".localName",".ownerDocument",".previousSibling",".body",".isDefaultNamespace",".nodeType",".track",".isSameNode",".cookie",".createDocumentFragment",".getElementsByName",".baseURI",".lookupNamespaceURI",".parentNode",".getElementById",".attributes",".createTextNode"]
results = {}

html_source = driver.page_source
html = BeautifulSoup(html_source, 'html.parser')

#Here is the part which extracts Scripts
scripts = driver.find_elements_by_tag_name("script")

for script in scripts:
	try:
		src = script.get_attribute("src")
	except:
		continue

	if src != "":
		try:
			req = requests.get(src)
			script_source = req.text
		except:
			continue
	else:
		script_source = script.get_attribute("outerHTML")

	content = script_source.encode('utf-8')

	for f in features:
		if f in content:
			cnt = content.count(f)
			if f in results:
				results[f] += 1
			else:
				results[f] = 1
	
driver.quit()

text = ""
for item in results:
	for i in range(results[item]):
		text += item + " "

alice_mask = np.array(Image.open("alice_mask.png"))

stopwords = set(STOPWORDS)
stopwords.add("said")

font_path ='pacifico.ttf'

wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=alice_mask,
			   stopwords=stopwords, random_state=42, collocations=False)

# generate word cloud
wc.generate(text)

plt.figure(figsize = (16, 9))
# show
# plt.imshow(wc, cmap=plt.cm.get_cmap('Pastel2'), interpolation='bilinear')
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")

plt.axis("off")
plt.savefig(sys.argv[1].replace("http://","").replace("https://","")+".png")
