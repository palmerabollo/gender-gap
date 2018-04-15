import os, sys, time, itertools, json, random

from bs4 import BeautifulSoup

import scrapy
import gender_guesser.detector as gender

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LinkedinUser(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    gender = scrapy.Field()
    region = scrapy.Field()
    search = scrapy.Field()

    def serialize(self):
        return json.dumps(dict(self))

def beautify(client, url):
    response = client.get('https://www.linkedin.com' + url)
    return BeautifulSoup(response.text, "html.parser")

def get_by_xpath(driver, xpath, wait_timeout=5):
    return WebDriverWait(driver, wait_timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

def get_by_xpath_or_none(driver, xpath, wait_timeout=5, logs=True):
    try:
        return get_by_xpath(driver, xpath, wait_timeout=wait_timeout)
    except (TimeoutException, StaleElementReferenceException, WebDriverException) as e:
        if logs:
            print("Exception Occurred:")
            print(f"XPATH:{xpath}")
            print(f"Error:{e}")
    return None

def extracts_linkedin_users(driver, region, search):
    for i in range(1, 11):
        last_result_xpath = f'//li[{i}]/div/div[@class="search-result__wrapper"]'

        result = get_by_xpath(driver, last_result_xpath)
        if result is not None:
            name_elem = get_by_xpath_or_none(result, './/*[@class="name actor-name"]')
            name = name_elem.text if name_elem is not None else None

            gender = genderDetector.get_gender(name.split(" ")[0], u'spain')

            title_elem = get_by_xpath_or_none(result, './/p')
            title = title_elem.text if name_elem is not None else None

            user = LinkedinUser(name=name, title=title, gender=gender, region=region, search=search)
            yield user

            focus_elem_xpath = './/figure[@class="search-result__image"]/img'
            focus_elem = get_by_xpath_or_none(result, focus_elem_xpath, wait_timeout=1)
            if focus_elem is not None:
                driver.execute_script("arguments[0].scrollIntoView();", focus_elem)

            time.sleep(0.1)

def login(driver):
    driver.get('https://www.linkedin.com')
    get_by_xpath(driver, '//*[@class="login-email"]').send_keys(os.environ['LINKEDIN_USERNAME'])
    get_by_xpath(driver, '//*[@class="login-password"]').send_keys(os.environ['LINKEDIN_PASSWORD'])
    get_by_xpath(driver, '//*[@id="login-submit"]').click()
    time.sleep(10)

def debug(msg):
    print(f'DEBUG {msg}')
    sys.stdout.flush()

genderDetector = gender.Detector()

debug('start')

driver = webdriver.Firefox() # webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true']).
login(driver)

# TODO use env var or arg to pass these info from cli
terms=terms=['founder', 'docker', 'java', 'python', 'scala', 'javascript', 'frontend', 'backend', 'scrum master', 'ux designer', 'rrhh', 'maker', 'manager', 'enfermeria']
region='es%3A5154'

# some useful regions
# es%3A5154 = Valladolid Area, Spain
# es%3A0 = Spain

for search in terms:
    debug(f'search term {search}')
    try:
        for page in itertools.count(): # TODO restrict to the first 20 pages?
            debug(f'page {page + 1}')
            driver.get(f'https://www.linkedin.com/search/results/people/?facetGeoRegion=["{region}"]&keywords={search}&origin=FACETED_SEARCH&page={page + 1}')
            users = extracts_linkedin_users(driver, 'Valladolid Area, Spain', search)
            for user in users:
                print(user.serialize())
            sys.stdout.flush()
            time.sleep(random.uniform(2, 15))
    except Exception as e:
        debug(f'exception {str(e)}')
        continue

driver.close()
