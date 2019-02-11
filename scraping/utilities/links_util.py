import base64

def decrip_link_protetion(link):
    encoded = str(link.split("/?v=")[1])
    decoded = base64.b64decode(str.encode(encoded))
    return decoded