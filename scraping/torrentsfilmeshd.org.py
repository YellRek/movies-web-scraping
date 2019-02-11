import selenium_service
from movie import movie, download_link_info
import time

current_url = "https://torrentsfilmeshd.org/"
driver = selenium_service.get_chrome_driver(current_url)
current_page = 1

articles = driver.find_elements_by_tag_name("article")

all_movies = []
current_movies = []
for _article in articles:
    driver.get(current_url)
    title = _article.find_element_by_class_name("entry-header").text
    __link = _article.find_element_by_class_name("entry-header").find_element_by_tag_name("a").get_attribute("href")
    mov = movie(title, __link)
    mov.image_url = _article.find_elements_by_tag_name("img")[0].get_attribute("data-lazy-src")

    driver.get(mov.link_page)
    article = driver.find_element_by_tag_name("article")
    content = article.find_element_by_class_name("entry-content")

    page_content_info = content.find_elements_by_tag_name("p")[0].text + "\r\n\r\n"
    page_content_info += content.find_elements_by_tag_name("p")[1].text + "\r\n\r\n"
    page_content_info += content.find_elements_by_tag_name("p")[2].text + "\r\n\r\n"

    mov.descriptions = page_content_info
    _links = content.find_elements_by_tag_name("a")
    links = []
    for el in _links:
        link = str(el.get_attribute("href"))
        if link is not None and link.find("link-download.in") > 0:
            links.append(el)

    div_parents = []
    for link in links:
        if link.find_element_by_xpath('..').tag_name == "div":
            _div = link.find_element_by_xpath('..')
        elif link.find_element_by_xpath('..').find_element_by_xpath('..').tag_name == "div":
            _div = link.find_element_by_xpath('..').find_element_by_xpath('..')
        elif link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').tag_name == "div":
            _div = link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        elif link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').tag_name == "div":
            _div = link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        if _div not in div_parents and _div != None:
            div_parents.append(_div)
            

    div_parent_childs = []
    for div_parent in div_parents:
        for _p in div_parent.find_elements_by_tag_name("p"):
            div_parent_childs.append(_p)

    def get_link_child(previus):
        try:
            if previus.find_elements_by_xpath(".//*")[0].tag_name == "a":
                return previus.find_elements_by_xpath(".//*")[0]
            elif previus.find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0].tag_name == "a":
                return previus.find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0]
            else:
                return previus.find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0]
        except:
            return None

    class link_info():
        def __init__(self, title, link):
            self.title = title
            self.link = link
            
    links_info = []
    links_link = []

    for link_el in links:
        previus_text = ""
        for previus in div_parent_childs:
            if get_link_child(previus) == link_el:
                links_info.append(link_info(previus_text, link_el.get_attribute("href")))
                links_link.append(link_el.get_attribute("href"))
            else:
                previus_text = previus.text

    for link in links:
        if link not in links_link:
            links_info.append(link_info("mirror", link_el.get_attribute("href")))

    mov.download_links = links_info
    print(mov.title + "\r\n")
    print(mov.descriptions + "\r\n")
    print(mov.image_url + "\r\n")
    for _link in mov.download_links:
        print(_link.title)
        print(_link.link)

    current_movies.append(mov)
    
for movie in current_movies:
    print(movie.title + "\r\n")
    print(movie.descriptions + "\r\n")
    print(movie.image_url + "\r\n")
    for _link in movie.download_links:
        print(_link.title)
        print(_link.link)

    print(" ----------------------- ","\r\n\r\n")