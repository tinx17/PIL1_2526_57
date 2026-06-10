from django.http import HttpResponse

class SimpleCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = self.get_response(request)

        origin = request.headers.get('Origin')
        # Allow requests from the frontend running locally (usually 8080 or other localhost ports)
        if origin and ('localhost' in origin or '127.0.0.1' in origin):
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken, Authorization, X-Requested-With"
            response["Access-Control-Allow-Credentials"] = "true"

        return response
