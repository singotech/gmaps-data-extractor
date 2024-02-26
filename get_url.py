from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, random, re

def is_target_text_present(driver, target_text):
    return target_text in driver.page_source

print('--- Execute get_url.py ---')
print('--- Opening Browser ---')
# Set the path to your Driver executable
driver_path = '/Users/7noob/Project/Singo/project/internal/gmaps-data-extractor/driver/geckodriver'

# Create a new instance of the driver
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Optional: Run in headless mode (no browser window)

service = webdriver.FirefoxService(executable_path=driver_path)

driver = webdriver.Firefox(service=service, options=options)

keyword = 'toko patung malang'

target_text_to_stop_scroll = "Anda telah mencapai akhir daftar"

# Open Google homepage
driver.get('https://www.google.com/maps/search/' + keyword.replace(' ', '+'))

print('--- Scrolling page ---')
while not is_target_text_present(driver, target_text_to_stop_scroll):
    # Scroll down using keyboard keys (simulating Page Down)
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.PAGE_DOWN)

    # Find the div element with role="feed"
    feed_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

    # Scroll down using JavaScript
    driver.execute_script("arguments[0].scrollIntoView();", feed_div)

    # Optional: You can add some delay to let the content load
    time.sleep(random.randrange(1, 4))

    # Scroll down further using keyboard keys (simulating Page Down)
    feed_div.send_keys(Keys.PAGE_DOWN)
print('--- Scroll done ---')

page_source = driver.page_source

print('--- Get URL ---')
regex = r"https\:\/\/www\.google\.com\/maps\/place\/(\S+)"
matches = re.finditer(regex, page_source, re.MULTILINE)
for match in matches:
    url = match.group().replace('"', '')
    print(url)
    with open("output/urls.txt", "a") as filetowrite:
        filetowrite.write(url + "\n")

print('--- Close Browser ---')

# Close the browser window
driver.quit()
