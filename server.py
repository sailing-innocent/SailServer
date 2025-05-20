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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("sail_server")
from litestar.logging import LoggingConfig


from utils.env import read_env

read_env("prod")


class SailServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.app = None
        self.router = None
        self.api_endpoint = os.environ.get("API_ENDPOINT", "/api")
        self.api_router = None
        self.debug = os.environ.get("DEV_MODE", "false").lower() == "true"

    def init(self):
        @get("/health")
        async def health_check(request: Request) -> dict[str, str]:
            return {"status": "ok"}

        self.base_router = Router(path="/", route_handlers=[health_check])
        from internal.router.db import router as db_router

        self.api_router = Router(
            path=self.api_endpoint,
            route_handlers=[db_router],
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
        self.app = Litestar(
            route_handlers=[self.base_router, self.api_router],
            debug=self.debug,
            logging_config=logging_config,
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
