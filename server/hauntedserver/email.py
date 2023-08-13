import ssl

from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.utils.functional import cached_property


class UnsafeSSLEmailBackend(SMTPBackend):
    @cached_property
    def ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context
