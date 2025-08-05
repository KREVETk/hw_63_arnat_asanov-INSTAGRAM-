from urllib.parse import urlparse

class RedirectBackMixin:
    redirect_field_name = 'next'

    def get_redirect_url(self):
        next_url = self.request.POST.get(self.redirect_field_name) or self.request.GET.get(self.redirect_field_name)
        if next_url:
            netloc = urlparse(next_url).netloc
            if not netloc or netloc == self.request.get_host():
                return next_url
        return None

    def get_success_url(self):
        return self.get_redirect_url() or super().get_success_url()
