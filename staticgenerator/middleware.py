import re
from django.conf import settings
from staticgenerator import StaticGenerator

class StaticGeneratorMiddleware(object):
    """
    This requires settings.STATIC_GENERATOR_URLS tuple to match on URLs.
    This fork uses the requests incoming host header to allow multiple site
    static generation.
    
    Example::
        
        STATIC_GENERATOR_URLS = (
            r'^/$',
            r'^/blog',
        )
        
    """
    urls = tuple([re.compile(url) for url in settings.STATIC_GENERATOR_URLS])
    gen = StaticGenerator()
    
    def process_response(self, request, response):
        if response.status_code == 200:
            for url in self.urls:
                if url.match(request.path_info):
                    self.gen.publish_from_path('%s%s'%(request.get_host(), request.path), response.content)
                    break
        return response
