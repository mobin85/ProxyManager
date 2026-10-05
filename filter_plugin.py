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
]

class DomainFilterPlugin(HttpProxyBasePlugin):
    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        return self.handle_client_request(request)

    def handle_client_request(self, request: HttpParser) -> Optional[HttpParser]:
        blocked_ips = ['45.139.10.229']
        
        # Check client IP
        client_ip = self.client.address[0] if self.client and self.client.address else None
        
        # Check X-Forwarded-For just in case
        x_forwarded_for = request.header(b'x-forwarded-for') if request.has_header(b'x-forwarded-for') else None
        client_ips = [client_ip] if client_ip else []
        if x_forwarded_for:
            client_ips.extend([ip.strip().decode('utf-8', errors='ignore') for ip in x_forwarded_for.split(b',')])

        if any(ip in blocked_ips for ip in client_ips if ip):
            logger.warning("[DomainFilter] BLOCKED IP: %s", client_ips)
            raise HttpRequestRejected(
                status_code=403,
                reason=b'Forbidden',
                body=b'403 Forbidden: Your IP is blocked.'
            )

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