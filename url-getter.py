from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time


heroku_loggin_url = "https://id.heroku.com/login"

def get_pg_url_from_heroku(email, pwd, prject_name, path_to_geckodriver):
    #heroku_settings_url = "https://dashboard.heroku.com/apps/cianostavernabot/settings"

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=path_to_geckodriver)

    driver.get(heroku_loggin_url)
    #print("Login page aperta")
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("password").send_keys(pwd)
    driver.find_element_by_name("commit").click()

    WebDriverWait(driver, 30).until(EC.title_contains("Personal apps | Heroku"))
    #print("Loggin avvenuto con successo")

    driver.find_element_by_id("ember35").click()
    WebDriverWait(driver, 10).until(EC.title_contains(prject_name + " | Heroku"))
    #print("Dashboard aperta")

    driver.find_elements_by_class_name("sub-nav-item")[-1].click()
    WebDriverWait(driver, 10).until(EC.title_contains(prject_name + " · Settings | Heroku"))
    #print("settings aperti")

    div_config_var = driver.find_elements_by_class_name("config-vars")[0]
    div_config_var.find_element_by_class_name("async-button").click()
    #print("url visualizzato")

    time.sleep(3)

    url = div_config_var.find_elements_by_tag_name("textarea")[0].get_attribute("value")
    #print(url)
    driver.quit()
    return url
