
def ErrorSerializer(req, resp, exception):
    """
    Error serialization to preferred format
    """
    resp.body = exception.to_json()
    resp.content_type = 'application/json'
    