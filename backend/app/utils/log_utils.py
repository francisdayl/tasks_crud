import logging


def log_request(request):
    logging.info("Incoming Request")
    logging.info(
        {
            "headers:": request.headers,
            "path": request.path,
            "body": request.get_json() if request.is_json else {}
        }
    )


def log_response(response):
    logging.info("Response")
    logging.info(response)
