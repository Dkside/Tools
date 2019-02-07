# WhatsApp Spammer

This is a simple python script one can use to spam WhatsApp contacts using the Google Chrome browser. It makes use of the Selenium library to do so. Quite simple, really. 

Make sure you have Selenium installed. If you don't have Selenium installed, using pip.

```
pip install selenium
```

Also, make sure you have the necessary webdrivers in your path. I've used chromedriver.

* Firefox - [geckodriver](https://github.com/mozilla/geckodriver/releases)
* Google - [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) 

Google the corresponding drivers for the browser you want to use. Replace the driver name in the following line - 

```
driver = webdriver.Chrome()
```

Rest is up to your experimentation. Just don't spam your boss.