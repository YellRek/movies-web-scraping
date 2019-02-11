import os  
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

chrome_options = Options()  
#chrome_options.add_argument("--headless")  
# chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'
driver = webdriver.Chrome(executable_path="C:\\Users\\Jonatas\\Documents\\Python Scripts\\chromedriver.exe", chrome_options=chrome_options)
driver.get("https://torrentsfilmeshd.org/")

articles = driver.find_elements_by_tag_name("article")
for article in articles:
    # print(article)
    # print(article.find_element_by_class_name("entry-title"))
    title = article.find_element_by_class_name("entry-title").find_element_by_tag_name("a").text
    print(title)



# magnifying_glass = driver.find_element_by_id("js-open-icon")  
# if magnifying_glass.is_displayed():  
#   magnifying_glass.click()  
# else:  
#   menu_button = driver.find_element_by_css_selector(".menu-trigger.local")  
#   menu_button.click()`  

# search_field = driver.find_element_by_id("site-search")  
# search_field.clear()  
# search_field.send_keys("Olabode")  
# search_field.send_keys(Keys.RETURN)  
# assert "Looking Back at Android Security in 2016" in driver.page_source   driver.close()`  
