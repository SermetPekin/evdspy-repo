def remove_api_key(url):
    if "key=" not in url:
        return url
    separator = "&"
    new_parts = (x for x in url.split(separator) if "key=" not in x)
    return separator.join(new_parts) + "&key=xxxOMITTEDforSec"
