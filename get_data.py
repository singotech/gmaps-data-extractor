from selenium import webdriver
from selenium.webdriver.common.by import By
import re, argparse, os, concurrent.futures

MAX_THREADS = 5  # Adjust this value based on your preference

def crawl(url):
    if url == '':
        return
    print('--- Opening Browser ---')
    # Set the path to your Driver executable
    driver_path = './driver/geckodriver'

    # Create a new instance of the driver
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Optional: Run in headless mode (no browser window)

    service = webdriver.FirefoxService(executable_path=driver_path)

    driver = webdriver.Firefox(service=service, options=options)

    url = url.replace('\n', '')
    urlTitle = url.split('=', 1)
    print('--- Visit URL ' + urlTitle[0] + '  ---')
    driver.get(url)

    page_source = driver.page_source

    # Get star
    # input             : <span class="ceNzKf" role="img" aria-label="Bintang 4,8 "><span class="rFrJzc"></span><span class="rFrJzc"></span><span class="rFrJzc"></span><span class="rFrJzc"></span><span class="rFrJzc"></span></span>
    # pattern           : role=\"img\" aria-label=\"Bintang (\S+)
    # expected output   : role="img" aria-label="Bintang 4,8
    star = '-'
    patternStar = r"role=\"img\" aria-label=\"Bintang (\S+)"
    matches = re.search(patternStar, page_source)
    if matches != None:
        star = matches.group()
        star = star.replace('role="img" aria-label="', '')
        star = star.replace(',', ';')
    print(star)

    # Get Review
    # input             : <span aria-label="8.073 ulasan">(8.073)</span>
    # pattern           : aria-label=\"(\S+) ulasan
    # expected output   : aria-label="8.073 ulasan
    review = '-'
    patternReview = r"aria-label=\"(\S+) ulasan"
    matches = re.search(patternReview, page_source)
    if matches != None:
        review = matches.group()
        review = review.replace('aria-label="', '')
        review = review.replace(',', ';')
    print(review)

    # Get Business Category
    # input             : <button class="DkEaL " jsaction="pane.wfvdle8.category">Taman Hiburan</button>
    # pattern           : jsaction\=\"pane\.(\S+)\.category\"\>[\w\s]+\<\/button\>
    # expected output   : jsaction="pane.wfvdle8.category">Taman Hiburan</button>
    businessCategory = '-'
    patternbusinessCategory = r"jsaction\=\"pane\.(\S+)\.category\"\>[\w\s]+\<\/button\>"
    matches = re.search(patternbusinessCategory, page_source)
    if matches != None:
        businessCategory = matches.group()
        businessCategory = businessCategory.split('>', 1)[1]
        businessCategory = businessCategory.replace('</button>', '')
        businessCategory = businessCategory.replace(',', ';')
    print(businessCategory)

    # Get Business Address
    # input             : <meta content="Predator Fun Park Batu · Jl. Raya Tlekung No.315, Tlekung, Kec. Junrejo, Kota Batu, Jawa Timur 65327" property="og:title">
    businessTitle = urlTitle[0]
    addrProperty = 'og:title'
    css_selector = f'meta[property="{addrProperty}"]'
    meta_element = driver.find_element(By.CSS_SELECTOR, css_selector)
    businessAddress = meta_element.get_attribute('content')
    businessSplit = businessAddress.split(' · ')
    if len(businessSplit) > 1:
        businessTitle = businessSplit[0].replace(',', ';')
        businessAddress = businessSplit[1].replace(',', ';')
    print(businessTitle)
    print(businessAddress)

    # Get Phone Number
    # input             : data-item-id="phone:tel:00000000000"
    # pattern           : phone\:tel\:(\d+)
    # expected output   : 00000000000
    phoneNumber = '-'
    patternphoneNumber = r"phone\:tel\:(\d+)"
    matches = re.search(patternphoneNumber, page_source)
    if matches != None:
        phoneNumber = matches.group()
        phoneNumber = phoneNumber.replace('phone:tel:', '')
        print(phoneNumber)
    else :
        print("--- Phone number not found, skipped ---")
        return

    with open("output/data.csv", "a") as filetowrite:
        filetowrite.write(url.replace(',', '%2C') + ',' + businessTitle + ',' + businessCategory + ',' + star + ',' + review + ',' + businessAddress + ',' + phoneNumber + '\n')
    print("--- Save record ---")

    print('--- Close Browser ---')

    # Close the browser window
    driver.quit()

def get_data(input_file):
    print('--- Execute get_data.py ---')
    if input_file == '':
        input_file = './output/urls.txt'
    with open(input_file) as filetoread:
        urls = filetoread.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(lambda url: crawl(url), urls)

if __name__ == '__main__':
    if not os.path.exists('./driver/geckodriver'):
        print("please download geckodriver and put it in driver folder")
        exit()

    parser = argparse.ArgumentParser("get_data")
    parser.add_argument("--input_file", help="File that contains list of urls, ex: /full/path/to/urls.txt", type=str)
    args = parser.parse_args()
    input_file = args.input_file
    if input_file == None or len(input_file) <= 0:
        input_file = "./output/urls.txt"
    else:
        if not os.path.exists(input_file):
            print("file does not exist")
            exit()
    get_data(input_file)
