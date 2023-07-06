import logging
import time

# Create and configure logger
"""
To write the log into a specific file.
"""
# LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
# logging.basicConfig(
#     filename="/home/nadeem/Desktop/file.log",
#     level=logging.DEBUG,
#     format=LOG_FORMAT,
#     filemode="w",
# )
logger = logging.getLogger()


class APITrackingMiddleware:
    """
    Middleware to track all the APIs and gives,
    error status, response time, no of requests and no of errors

    Returns JSON response
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.error_count = 0

    def __call__(self, request):
        # To get the response time
        start_time = time.time()

        response = self.get_response(request)
        response_time = time.time() - start_time
        status_code = response.status_code

        self.request_count += 1
        if status_code >= 400:
            self.error_count += 1

        # Log the API request details
        print("\n")
        logger.info(f"API Request: localhost{request.path}")
        logger.info(f"Method Type: {request.method}")
        logger.info(f"Status Code: {status_code}")
        logger.info(f"Response Time: {response_time:.2f} seconds")
        logger.info(f"Total number of requests : {self.request_count}")
        logger.info(f"Total number of error counts : {self.error_count}\n")

        return response
