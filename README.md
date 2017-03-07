# spider-men
This is a project that contains multi web crawlers and some useful tools such as email. Since my spiders are based on Python3, make sure you have installed Python3 in your system before you use these examples. Futhermore, you should installed these third party libraries: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#), [requests](http://docs.python-requests.org/en/master/), [Phantomjs](http://phantomjs.org/), [selenium](http://selenium-python.readthedocs.io/index.html) and [PyMongo](http://api.mongodb.com/python/current/).
*********************
# Install
* BeautifulSoup
```
pip install beautifulsoup4
```
* requests
```
pip install requests
```
* selenium
```
pip install selenium
```
* pymongo
```
pip install pymongo
```
If your system has installed py2 and py3 at the same time, please use `py -3 -m pip install` instead of `pip install` all the above. 
* phantomjs
In Windows system, download (phantomjs)[http://phantomjs.org/download.html] zip file, and unzip it, copy **phantomjs.exe** into the root path of py3.
# Usage
### KugouMusicSpider.py
First, make sure you have started local mongo server and have an empty database named **kugou**. Second, remember to modify your email information in method `send_mail`. Third, switch the annotation state in main method according to the craw phase.
Now, you can open a `cmd` window and run command `py KugouMusicSpider.py` at the root of this project. The console will print some info and that means this spider works. Wow!
