from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

# driver setup
chrome_options = Options()
chrome_options.add_experimental_option(
    "prefs", {'profile.managed_default_content_settings.javascript': 2})
PATH = "/home/garv/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

# search for tournament
driver.get("https://www.tabroom.com/index/index.mhtml")
searchQuery = driver.find_element_by_name("search")
tournamentName = "James Logan"
searchQuery.send_keys(tournamentName)
searchQuery.send_keys(Keys.RETURN)

# find tournament
teamData = {}
main = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_results")))
divTags = main.find_elements_by_tag_name("tr")

divTag = divTags[1]  # index 1 not 0. 0 is the titlebar
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
            try:
                preSeeds = driver.find_element_by_xpath(
                    "/html/body/div/div[2]/div/div[1]/div[2]/a[1]")
                preSeeds.click()
                url = driver.current_url
                driver.close()
                driver = webdriver.Chrome(PATH)
                driver.get(url)
                tableHead = driver.find_element_by_tag_name(
                    "table")
                tableRow = tableHead.find_element_by_tag_name("tr")
                tableCol = tableRow.find_elements_by_tag_name("th")
                i = 0
                for col in tableCol:
                    i += 1
                    #print(col.text)
                    if "OSd" in col.text:
                        col.click()
                        col.click()
                        print("true")
                        break
                    else:
                        continue
                tableHead = driver.find_element_by_tag_name(
                    "table")
                tableHead = tableHead.get_attribute('innerHTML')
                tableHead = BeautifulSoup(tableHead, 'html.parser')
                j = 0
                for row in tableHead.tbody.findAll('tr'):
                    if (j >= 32):
                        break
                    place_col = row.findAll('td')[0].get_text(strip=True)
                    name_col = row.findAll('td')[1].get_text(strip=True)
                    oppseed_col = row.findAll('td')[i-1].get_text(strip=True)
                    teamData[name_col] = {}
                    if (j >= 0):
                        if(j > 1):
                            if (j > 3):
                                if (j > 7):
                                    if (j > 15):
                                        teamData[name_col]['Expected'] = 1
                                    else:
                                        teamData[name_col]['Expected'] = 2
                                else:
                                    teamData[name_col]['Expected'] = 3
                            else:
                                teamData[name_col]['Expected'] = 4
                        else:
                            teamData[name_col]['Expected'] = 5
                    if int(place_col) > 32:
                        teamData[name_col]['Variance'] = teamData[name_col]['Expected']
                    teamData[name_col]['Place'] = place_col
                    teamData[name_col]['OppSeed'] = oppseed_col
                    j += 1
                try:
                    recordButton = driver.find_element_by_partial_link_text(
                        "Prelim Records")
                    recordButton.click()

                    table = driver.find_element_by_tag_name(
                        "table")
                    head = table.get_attribute('innerHTML')
                    head = BeautifulSoup(head, 'html.parser')
                    #print(head)
                    k = 0
                    addPerson = True
                    for row in head.tbody.findAll('tr'):
                        if(k >= 32):
                            #print("breaking")
                            break
                        name = row.findAll('td')[2]
                        nameButton = driver.find_element_by_link_text(
                            name.get_text(strip=True))
                        nameButton.click()
                        teamTable = driver.find_element_by_xpath(
                            '/html/body/div[1]/div[2]/div/div[3]')
                        teamTable = BeautifulSoup(
                            teamTable.get_attribute('innerHTML'), 'html.parser')
                        actual = 0
                        for each in teamTable.select('div[class*="row"]'):
                            if "Triples" in each.findAll('span')[0].get_text(strip=True):
                                break
                            if "Round" not in each.findAll('span')[0].get_text(strip=True):
                                #print("round name: ")
                                #print(each.findAll('span')[
                                #      0].get_text(strip=True))
                                actual += 1
                            else:
                                break

                        name = name.get_text(strip=True)
                        #print(actual)

                        if any(name in d for d in teamData):

                            teamData[name]['Actual'] = actual

                        else:
                            if (actual == 0):
                                addPerson = False
                            else:
                                teamData[name] = {}
                                teamData[name]["Expected"] = 0
                                teamData[name]["actual"] = actual
                        if addPerson == True:
                            teamData[name]['Variance'] = abs(
                                int(actual) - int(teamData[name]['Expected']))
                            #print("here")
                            #print(actual)
                            k += 1
                        addPerson = True
                        driver.back()
                    #print(k)
                    with open(tournamentName.strip()+".json", "w") as outfile:
                        json.dump(teamData, outfile, indent=3)
                    total = 0
                    for teamName in teamData:
                        total += int(teamData[teamName]["Variance"])
                    #print(len(teamData))
                    print(total/len(teamData))
                    time.sleep(1000)
                except:
                    print("hi")
                #print(teamData
            except:
                print()
                #driver.quit()
        except:
            print()
            #driver.quit()
    except:
        print()
        #driver.quit()
except:
    print()
    #driver.quit()
