# -*- encoding: utf-8 -*-
import sys
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pathlib import Path
project_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_path))

from log_util import logger


def verify_access_token(request: Request) -> None:
    # todo(need to add verified method)
    pass


class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            verify_access_token(request)
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # If token validation fails due to HTTPException, return the error response
            await self.print_request(request)
            logger.warning(exc)
            return JSONResponse(
                content={"detail": exc.detail}, status_code=exc.status_code
            )
        except Exception as exc:
            # If token validation fails due to other exceptions, return a generic error response
            await self.print_request(request)
            logger.warning(exc)
            return JSONResponse(
                content={"detail": f"Error: {str(exc)}"}, status_code=500
            )