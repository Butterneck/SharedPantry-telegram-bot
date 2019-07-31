from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
from tqdm import tqdm

heroku_loggin_url = "https://id.heroku.com/login"

def get_pg_url_from_heroku(email, pwd, prject_name, path_to_geckodriver, project_index):
    #heroku_settings_url = "https://dashboard.heroku.com/apps/cianostavernabot/settings"
    pbar = tqdm(total=100, postfix="Apertura login page")

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=path_to_geckodriver)

    driver.get(heroku_loggin_url)
    pbar.update(16)#print("Login page aperta")
    pbar.set_postfix_str("Inserimento campi dati")
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("password").send_keys(pwd)
    driver.find_element_by_name("commit").click()

    pbar.set_postfix_str("Log in in corso")
    WebDriverWait(driver, 30).until(EC.title_contains("Personal apps | Heroku"))
    pbar.update(16)#print("Loggin avvenuto con successo")

    pbar.set_postfix_str("Apertura dashboard")
    #driver.find_element_by_id("ember35").click()
    driver.find_elements_by_class_name("apps-list-item")[project_index].click()
    WebDriverWait(driver, 10).until(EC.title_contains(prject_name + " | Heroku"))
    pbar.update(16)#print("Dashboard aperta")

    pbar.set_postfix_str("Apertura Setting")
    driver.find_elements_by_class_name("sub-nav-item")[-1].click()
    WebDriverWait(driver, 10).until(EC.title_contains(prject_name + " · Settings | Heroku"))
    pbar.update(16)#print("settings aperti")

    pbar.set_postfix_str("Ricezione URL")
    div_config_var = driver.find_elements_by_class_name("config-vars")[0]
    div_config_var.find_element_by_class_name("async-button").click()
    pbar.update(16)#print("url visualizzato")

    time.sleep(3)

    url = div_config_var.find_elements_by_tag_name("textarea")[0].get_attribute("value")
    pbar.update(20)
    pbar.set_postfix_str("Completato")
    print("URL=",url)
    driver.quit()
    pbar.close()
    return url
