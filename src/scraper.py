from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option(
    "prefs", {'profile.managed_default_content_settings.javascript': 2})


PATH = "/home/garv/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

driver.get("https://www.tabroom.com/index/index.mhtml")
searchQuery = driver.find_element_by_name("search")
tournamentName = "James Logan"
searchQuery.send_keys(tournamentName)
searchQuery.send_keys(Keys.RETURN)

main = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_results")))
divTags = main.find_elements_by_tag_name("tr")

divTag = divTags[1]
try:
    tag = divTag.find_element_by_tag_name("td")
    tourneyName = tag.find_element_by_tag_name(
        "a")
    driver.get(tourneyName.get_attribute('href'))
    try:
        tourneyResults = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div[2]/div/div[1]/ul/li[6]/a"))
            )
        tourneyResults.click()
        try:
            select = Select(
                driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[1]/form/div/span[1]/select"))
            select.select_by_visible_text("Parliamentary Debate")
            button = driver.find_element_by_xpath(
                "/html/body/div/div[2]/div/div[1]/div[1]/form/div/span[2]/input")
            button.click()
            #selector.click()
        except:
            driver.quit()
    except:
        driver.quit()
except:
    driver.quit()
