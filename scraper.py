from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "/home/garv/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://www.tabroom.com/index/index.mhtml")
searchQuery = driver.find_element_by_name("search")
searchQuery.send_keys("James Logan")
searchQuery.send_keys(Keys.RETURN)

main = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_results")))
divTags = main.find_elements_by_tag_name("tr")

divTag = divTags[1]
try:
    tag = divTag.find_element_by_tag_name("td")
    tourneyName = tag.find_element_by_tag_name(
        "a")
    print("hello")
    driver.get(tourneyName.get_attribute('href'))
    try:
        tourneyResults = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/ul[1]/li[6]/a"))
            )
        tourneyResults.click()
    except:
        driver.quit()
except:
    print()
