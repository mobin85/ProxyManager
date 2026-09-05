from typing import Optional
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from proxy.http.exception import HttpRequestRejected

ALLOWED_DOMAINS = [
    b'exitlag.com',
    b'exitlag.net',
    b'r2.dev'
]

class DomainFilterPlugin(HttpProxyBasePlugin):
    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        return self.handle_client_request(request)

    def handle_client_request(self, request: HttpParser) -> Optional[HttpParser]:
        if not request.host:
            return request

        host = request.host.lower()
        
        is_allowed = any(
            host == domain or host.endswith(b'.' + domain)
            for domain in ALLOWED_DOMAINS
        )

        if not is_allowed:
            raise HttpRequestRejected(
                status_code=403,
                reason=b'Forbidden',
                body=b'403 Forbidden: Domain is not allowed by this proxy.'
            )
        
        return request