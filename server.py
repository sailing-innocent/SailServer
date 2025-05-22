# -*- coding: utf-8 -*-
# @file server.py
# @brief The Long Last Server Entry
# @author sailing-innocent
# @date 2025-04-27
# @version 1.0
# ---------------------------------

import asyncio
import os
import json
from litestar import Litestar, Router, get, Request

import logging
from litestar.config.cors import CORSConfig
import argparse

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("sail_server")
from litestar.logging import LoggingConfig


from utils.env import read_env

read_env("prod")

from internal.exception_handlers import exception_handlers
from litestar.static_files import create_static_files_router

class SailServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = None
        self.router = None
        self.api_endpoint = os.environ.get("API_ENDPOINT", "/api")
        self.site_dist = os.environ.get("SITE_DIST", "site_dist")
        self.page_alias = ["/health", "/asset", "/playground", "/content", "/project"]
        self.api_router = None
        self.debug = os.environ.get("DEV_MODE", "false").lower() == "true"

    def init(self):
        @get("/health")
        async def health_check(request: Request) -> dict[str, str]:
            return {"status": "ok"}

        # redirect all self.page_alias to root
        for alias in self.page_alias:

            @get(alias)
            async def redirect_to_root(request: Request) -> dict[str, str]:
                return {"status": "redirect", "location": "/"}


        self.base_router = Router(
            path="/",
            route_handlers=[
                redirect_to_root,
                create_static_files_router(
                    directories=[self.site_dist],
                    path="/",
                    html_mode=True,
                    include_in_schema=False,
                ),
            ],
        )
        from internal.router.health import router as health_router
        from internal.router.finance import router as finance_router

        self.api_router = Router(
            path=self.api_endpoint,
            route_handlers=[
                health_check,
                self.base_router,
                health_router,
                finance_router,
            ],
        )

        logging_config = LoggingConfig(
            root={"level": "INFO", "handlers": ["queue_listener"]},
            formatters={
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            log_exceptions="always",
        )
        cors_config = CORSConfig(allow_origins=["*"], allow_methods=["*"])

        self.app = Litestar(
            route_handlers=[self.base_router, self.api_router],
            debug=self.debug,
            logging_config=logging_config,
            cors_config=cors_config,
            exception_handlers=exception_handlers,
            on_startup=[self.on_startup],
            on_shutdown=[self.on_shutdown],
        )

    async def on_startup(self):
        logger.info("Server starting up...")
        # Initialize any resources or connections here
        await asyncio.sleep(0.1)

    async def on_shutdown(self):
        logger.info("Server shutting down...")
        # Clean up any resources or connections here
        await asyncio.sleep(0.1)

    def run(self):
        logger.info(f"Server running on {self.host}:{self.port}")
        import uvicorn

        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=False,
        )


def main():
    try:
        host = os.environ.get("SERVER_HOST", "0.0.0.0")
        port = int(os.environ.get("SERVER_PORT", 1974))
        logger.info(f"Starting server at {host}:{port}")
        server = SailServer(host, port)
        server.init()
        server.run()
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        raise
    finally:
        logger.info("Server stopped")


if __name__ == "__main__":
    main()
