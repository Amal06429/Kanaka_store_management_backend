from django.utils.deprecation import MiddlewareMixin


class MediaCorsMiddleware(MiddlewareMixin):
    """Add CORS headers to media file responses"""
    
    def process_response(self, request, response):
        if request.path.startswith('/media/'):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Cross-Origin-Resource-Policy'] = 'cross-origin'
            response['Cross-Origin-Embedder-Policy'] = 'unsafe-none'
        return response
