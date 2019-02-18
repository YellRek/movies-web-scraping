import base64

def decrip_link_download_in_protetion(link):
    encoded = link.split("/?v=")[1]
    decoded = base64.b64decode(encoded).decode('ascii')
    return decoded