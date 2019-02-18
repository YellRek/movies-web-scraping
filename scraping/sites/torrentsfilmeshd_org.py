from services import selenium_service, imdb_service
from models.movie import movie
from infra.firebase_manager import firebase_manager
from utilities import json_util, links_util
import time
import json

fb = firebase_manager()

def _get_link_child(previus):
    try:
        if previus.find_elements_by_xpath(".//*")[0].tag_name == "a":
            return previus.find_elements_by_xpath(".//*")[0]
        elif previus.find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0].tag_name == "a":
            return previus.find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0]
        else:
            return previus.find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0].find_elements_by_xpath(".//*")[0]
    except:
        return None

def _get_original_title(description):
    try:
        lines = description.splitlines()
        line_with_original_title = list(filter(lambda x: x.startswith("Título Original:"), lines))

        if len(line_with_original_title) <= 0:
            line_with_original_title = list(filter(lambda x: x.startswith("Titulo Original:"), lines))
            original_title = line_with_original_title[0][len("Titulo Original: "):]
            return original_title

        original_title = line_with_original_title[0][len("Título Original: "):]
        return original_title
    except Exception as error:
        print("Error: _get_original_title - ", description)
        return ""

def _scrape_page_of_movie(link_page, title, image_url):
    try:
        driver_page = selenium_service.get_chrome_driver(link_page)
        article = driver_page.find_element_by_tag_name("article")
        content = article.find_element_by_class_name("entry-content")

        # Informaçoes sobre o filme em texto puro
        page_content_info = content.find_elements_by_tag_name("p")[0].text + "\r\n\r\n"
        page_content_info += content.find_elements_by_tag_name("p")[1].text + "\r\n\r\n"
        page_content_info += content.find_elements_by_tag_name("p")[2].text + "\r\n\r\n"

        mov = movie(title, link_page) 
        mov.image_url = image_url
        mov.descriptions = page_content_info
        mov.original_title = _get_original_title(page_content_info)
        mov.imdb_info = imdb_service.get_movie_info(mov.original_title)
        mov.imdb_info['Ratings'] = dict()

        try:
            iframes = driver_page.find_elements_by_tag_name("iframe")
            for ifram in iframes:
                if "youtube" in ifram.get_attribute("src"):
                    mov.trailer = ifram.get_attribute("src")
        except:
            pass

        # Pega todas as tags do tipo "a" para buscar os links de download
        _links = content.find_elements_by_tag_name("a")
        links = []

        # Percorre todos os links da pagina, e busca apenas aqueles links que forem do 
        # site link-download.in, pois esse é o site do protetor de link dos links de download
        # e adiciona a variavel links apenas os links de download.
        for el in _links:
            link = str(el.get_attribute("href"))
            if link is not None and link.find("link-download.in") > 0:
                links.append(el)


        # # Os links ficam agregados como filhos(normalmente não sao filhos diretos) de divs que 
        # # contem algumas tags P ou outras DIVs que possuem o link de download e a descrição
        # # do link, nesse for varremos todos os links, e vamos buscando as tags pai, até chegar na
        # # tag div, pois essa representa a tag pai que contem os links e as descrições.
        # div_parents = []
        # for link in links:
        #     if link.find_element_by_xpath('..').tag_name == "div":
        #         _div = link.find_element_by_xpath('..')
        #     elif link.find_element_by_xpath('..').find_element_by_xpath('..').tag_name == "div":
        #         _div = link.find_element_by_xpath('..').find_element_by_xpath('..')
        #     elif link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').tag_name == "div":
        #         _div = link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        #     elif link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').tag_name == "div":
        #         _div = link.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..')
        #     if _div not in div_parents and _div != None:
        #         div_parents.append(_div)
                

        # # Guarda todos os elementos com tag P que são filhas das divs do for anterior
        # div_parent_childs = []
        # for div_parent in div_parents:
        #     for _p in div_parent.find_elements_by_tag_name("p"):
        #         div_parent_childs.append(_p)

        # links_info = dict()
        # links_link = []

        # # Cria os links com suas descrições, as descriçoes dos links ficam normalmente
        # # em uma tag P que fica lado a lado com a tag P que contem o link, porem fica acima
        # # da tag P do link, por isso ela é a tag anterior (previus). Alguns links não 
        # # seguem essa estrutura, para esses links eles entram como "Mirror", pois não sabemos
        # # a descrição. TODO: contemplar paginas que não seguem essa estrutura.
        # for link_el in links:
        #     previus_text = ""
        #     for previus in div_parent_childs:
        #         if _get_link_child(previus) == link_el:
        #             links_info[links_util.decrip_link_download_in_protetion(link_el.get_attribute("href"))] = previus_text
        #             links_link.append(links_util.decrip_link_download_in_protetion(link_el.get_attribute("href")))
        #         else:
        #             previus_text = previus.text

        # # Verifica se todos os links de downloads foram encontrados com suas descrições, caso
        # # sua descriçao não tenha sido localizada, ele entra com a descrição "Mirror".
        # for index, link in enumerate(links):
        #     if links_util.decrip_link_download_in_protetion(link.get_attribute("href")) not in links_link:
        #         links_info[links_util.decrip_link_download_in_protetion(link.get_attribute("href"))] = "mirror " + str(index)

        # mov.download_links = {v: k for k, v in links_info.items()} 
        links_info = dict()
        for index, link in enumerate(links):
            links_info[str(index)] = links_util.decrip_link_download_in_protetion(link.get_attribute("href"))
        
        mov.download_links = links_info
        driver_page.close()
        return mov
    except Exception as error:
        print('Um erro ocorreu: ' + repr(error))

def _link_in_all_movies(link, all_movies):
    if all_movies != None:
        for _movie in all_movies:
            if all_movies[_movie]["link_page"] == link:
                return True
    return False   
        
def get_movies(max_pages):
    fb.initialize_firebase_db()
    all_movies = fb.get_table("movies2")

    current_url = "https://torrentsfilmeshd.org/"
    driver = selenium_service.get_chrome_driver(current_url)
    current_page = 1

    while current_page <= max_pages:
        articles = driver.find_elements_by_tag_name("article")
        for article in articles:
            title = article.find_element_by_class_name("entry-header").text
            link_page = article.find_element_by_class_name("entry-header").find_element_by_tag_name("a").get_attribute("href")
            
            if  not _link_in_all_movies(link_page, all_movies):
                # Capa do filme
                image_url = article.find_elements_by_tag_name("img")[0].get_attribute("data-lazy-src")
                mov = _scrape_page_of_movie(link_page, title, image_url)
                if mov != None:
                    fb.store_to_db("movies2", mov.__dict__)

        current_page += 1
        current_url = "https://torrentsfilmeshd.org/page/" + str(current_page)
        driver.get(current_url)
