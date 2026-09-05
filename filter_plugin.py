import logging
from typing import Optional
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.parser import HttpParser
from proxy.http.exception import HttpRequestRejected

logger = logging.getLogger(__name__)

ALLOWED_DOMAINS = [
    b'exitlag.com',
    b'exitlag.net',
    b'r2.dev',
    b'cloudflare.com',
    b'challenges.cloudflare.com',
    b'cloudflareinsights.com',
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
            logger.warning("[DomainFilter] BLOCKED domain: %s", host.decode('utf-8', errors='ignore'))
            raise HttpRequestRejected(
                status_code=403,
                reason=b'Forbidden',
                body=b'403 Forbidden: Domain is not allowed by this proxy.'
            )
        
        logger.info("[DomainFilter] ALLOWED domain: %s", host.decode('utf-8', errors='ignore'))
        return request