# GMAPS DATA EXTRACTOR

## Step by step:
- Download and install firefox
    - https://support.mozilla.org/en-US/kb/install-firefox-linux
- Download geckodriver from official page here
    - https://github.com/mozilla/geckodriver/releases
- Clone this repo & go to project `git clone https://github.com/singotech/gmaps-data-extractor.git && cd gmaps-data-extractor`
- Create venv for python then activate it `python3 -m venv .venv && source .venv/bin/activate`
- Run `pip install -r requirements.txt`
- Check your keyword
    `https://www.google.com/maps/search/your+keyword+here`
- If the keyword show you some businesses the you can run the app `python main.py --kw="you keyword here"`

## Tested on:
- Darwin
    - v 21.6.0 Darwin Kernel Version 21.6.0
    - Python 3.11.6
- Linux
    - 6.5.0-9-generic #9-Ubuntu x86_64 x86_64 x86_64 GNU/Linux
    - Python 3.11.6
