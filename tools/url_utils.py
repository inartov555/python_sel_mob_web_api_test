import re
from urllib.parse import urlparse


def get_base_url_and_port(url_string, is_port_pointed):
    """
    Expected URL may look like this: www.some-host.com

    Args:
        url_string (str): Either parsed.netloc or parsed.path (if parsed.netloc param is not set),
                          basically it should be URL
        is_port_pointed (bool): Use condition e.g. port_regex.search(parsed.netloc) is None

    Returns:
        tuple, (b_url, p_port)
    """
    b_url = ""
    p_port = ""
    url_string_u = url_string.replace("https://", "").replace("http://", "")
    if is_port_pointed:
        b_url, p_port = re.compile(r"(^(.*):(\d+).*$)").search(url_string_u).groups()[1:]
    else:
        b_url = url_string_u[0:url_string_u.find("/")] if url_string_u.find("/") > 0 else url_string_u
        p_port = ""
    return (b_url, p_port)


def get_http_prot_url_port_separately(url: str) -> tuple:
    """
    Args:
        url (str): e.g. http://some-host:80

    Returns:
        tuple, (http_protocol, base_url, port, path_uri, query_params)
    """
    port_regex = re.compile(r"(^.*:(\d+).*$)")
    parsed = urlparse(url)
    # When HTTP protocol is not provided, URL is placed to urlparse.path param
    if not parsed.scheme and port_regex.search(parsed.path) is None:
        raise ValueError(f"URL should contain at least HTTP protcol (http/https); current value: {url}")
    base_url, port = get_base_url_and_port(
        parsed.netloc or parsed.path,
        port_regex.search(parsed.netloc) is not None or port_regex.search(parsed.path) is not None)
    if parsed.scheme:
        http_protocol = parsed.scheme
    else:
        http_protocol = "https" if port in ("443", "8443") else "http"
    query_params = parsed.query
    if parsed.netloc:
        path_uri = parsed.path
    else:
        path_uri = parsed.path[parsed.path.find("/"):len(parsed.path)] if parsed.path.find("/") > 0 else ""
    if not port:
        port = "443" if http_protocol == "https" else "80"
    return (http_protocol, base_url, port, path_uri, query_params)
