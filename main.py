

#!/usr/bin/env python3
"""
EcoMarket RAG Solution - Main Entry Point
FastAPI application for RAG-based product queries and recommendations
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager
from app.api.apiFast import app

#!/usr/bin/env python3
"""
EcoMarket RAG Solution - Main Entry Point
Lanzador de la API FastAPI
"""
if __name__ == "__main__":
    import uvicorn
    from app.config.settings import get_settings
    settings = get_settings()
    uvicorn.run(
        "app.api.apiFast:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
