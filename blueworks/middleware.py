
import re


class RbacMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        regex_http_ = re.compile(r'^HTTP_.+$')
        regex_content_type = re.compile(r'^CONTENT_TYPE$')
        regex_content_length = re.compile(r'^CONTENT_LENGTH$')

        self.request_headers = {}
        for header in request.META:
            if regex_http_.match(header) or regex_content_type.match(header) or regex_content_length.match(header):
                self.request_headers[header] = request.META[header]
        # if hasattr(self, 'process_request'):
        #     print('request')
        #     response = self.process_request(request)
        # if not response:
        #     print(self.request_headers)
        #     response = self.get_response(request)
        # if hasattr(self, 'process_response'):
        #     print('response')
        #     response = self.process_response(request, response)
        print('avant')
        response = self.get_response(request)
        print('apres')
        return self.get_response(request)
