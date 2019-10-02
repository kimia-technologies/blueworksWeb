class RbacMiddleware():
    def __init__(self, get_response):
        super.get_response = get_response

    def __call__(self, request):
        response = self.get_reponse(request)
        return response
