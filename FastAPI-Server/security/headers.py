# security/headers.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from secure import SecureHeaders

# Настройка лимитера
limiter = Limiter(key_func=get_remote_address)

# Безопасные заголовки
secure_headers = SecureHeaders(
    hsts="max-age=31536000; includeSubDomains",
    csp="default-src 'self'; frame-ancestors 'none'",
    xfo="DENY",
    referrer="no-referrer, strict-origin-when-cross-origin",
)

def setup_security_middlewares(app: FastAPI, settings):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Secure headers middleware
    @app.middleware("http")
    async def set_secure_headers(request, call_next):
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response