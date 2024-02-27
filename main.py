from get_url import *
from get_data import *
import os

if __name__ == '__main__':
    if not os.path.exists('./driver/geckodriver'):
        print("please download geckodriver and put it in driver folder")
        exit()

    parser = argparse.ArgumentParser("main")
    parser.add_argument("--kw", help="Keyword should be 2 or more words, you can add city name to be more specific", type=str)
    args = parser.parse_args()
    kw = args.kw
    if kw == None or len(kw) < 5 or len(kw.split(' ')) < 2:
        print('Keyword too short, please add more than a word')
    else:
        get_url(kw)
        get_data('output/' + kw +'_urls.txt', kw)
