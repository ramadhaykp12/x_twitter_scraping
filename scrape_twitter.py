from selenium import webdriver
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import pandas as pd
import time

data = {}
user_name = []
tweets_text = []
date_time = []

driver = webdriver.Chrome()

# Isi formulir login
url = "https://twitter.com/i/flow/login"
driver.get(url)

username = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
username.send_keys("username")
username.send_keys(Keys.ENTER)

password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
password.send_keys("password")
password.send_keys(Keys.ENTER)

time.sleep(10)

# Open Twitter search page
driver.get("https://twitter.com/search?q=MBKM&src=typed_query")

# Scroll to load tweets
for _ in range(10):  # Adjust the range as needed
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait for new tweets to load

# Parse the page source with BeautifulSoup
# Ambil konten halaman setelah di-scroll
tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
users = driver.find_elements(By.XPATH, '//div[@data-testid="User-Name"]')  
#datetime_element = driver.find_element(By.CSS_SELECTOR, 'time')
for tweet in tweets:
    tweets_text.append(tweet.text)

for user in users:
    user_name.append(user.text)

#for date in datetime_element:
    #tweet_datetime = date.get_attribute('datetime')
    #date_time.append(tweet_datetime)

data['user'] = user_name
data['tweets'] = tweets_text
#data['date'] = date_time

df = pd.DataFrame(data)
df.to_csv('tweets_mbkm.csv')

driver.quit()
