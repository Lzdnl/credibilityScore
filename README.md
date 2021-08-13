# credibilityScore

## Description
Automated credibility assessment for online news articles. Given an URL of an article, it returns a score from 0 to 10. Metrics pertaining to journalistic standards and ethics are grouped into 4 categories:
* Formality
* Neutrality
* Transparency
* Layout

## Installation (Linux):
Prerequisites:
* Python3 installed
* Pip installed: sudo apt-get install python3-pip

Necessary modules (for exact version see requirements.txt):
* Selenium: sudo python3 -m pip install -U selenium
* Autocorrect: sudo python3 -m pip install autocorrect
* Requests: sudo python3 -m pip install requests

Additional programs:
* Galen Framework, for layout testing: [official website](http://galenframework.com/docs/getting-started-install-galen/) for installation procedure
* Mozilla Firefox browser
* Geckodriver: [List of releases](https://github.com/mozilla/geckodriver/releases), [installation procedure](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)

## Usage (Linux)
* From terminal: python3 main.py
* You will be prompted for the URL of the article you want to analyze
* When the testing is complete, you will be shown the credibility score and subscores for different metrics.

### Known errors
1. Extension _I don't care about cookies_, for removing the cookie banners, is not installed anymore. Reason unclear, most probably because of Selenium update, otherwise nothing changed. Solution for now is to configure the browser to reject all cookies. Doesn't work as well as the extension did.

