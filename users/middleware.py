from django.conf import settings
from django.http import HttpResponseRedirect

def login_url(next_path):
    return '%s?next=%s' % (settings.LOGIN_URL, next_path)

class RestrictAccessMiddleware(object):
    def __init__(self):
        self.excluded = settings.EXCLUDED_URLS
        self.restricted = settings.RESTRICTED_URLS
        self.restricted_by_default = len(self.excluded) > 0

    def process_request(self, request):
        if request.user.is_authenticated():
            return None

        path = request.path

        for url in self.excluded:
            if path.startswith(url):
                return None

        redirection = HttpResponseRedirect(login_url(path))
        if self.restricted_by_default:
            return redirection

        for url in self.restricted:
            if path.startswith(url):
                return  redirection

        return None
