class movie:
    def __init__(self, title, link_page):
        self.title = title
        self.link_page = link_page

    download_links = []
    descriptions = ""
    image_url = "https://i.pinimg.com/originals/06/c3/cd/06c3cd34f01aa9fdf023eb1736e98496.jpg"


class download_link_info:
    def __init__(self, title, link):
        self.title = title
        self.link = link