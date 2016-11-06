ajax_header = "X-Requested-With"
ajax_request_type = "XMLHttpRequest"


def is_ajax(request):
    """
    Returns a value indicating whether the given request is an AJAX request.
    """
    return ajax_header in request.headers and request.headers[ajax_header] == ajax_request_type