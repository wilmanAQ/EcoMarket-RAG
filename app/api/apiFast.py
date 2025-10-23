
#!/usr/bin/env python3
"""
EcoMarket RAG Solution - FastAPI API
"""

from fastapi import FastAPI, HTTPException, Depends, Query as FastAPIQuery
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from loguru import logger
from contextlib import asynccontextmanager

from app.rag.embeddings import EmbeddingService
from app.rag.retriever import DocumentRetriever
from app.rag.generator import ResponseGenerator
from app.config.settings import get_settings

logger.info("Logging initialized")

embedding_service = None
retriever = None
generator = None

class QueryRequest(BaseModel):
	query: str = Field(..., min_length=1, max_length=500)
	top_k: int = Field(default=3, ge=1, le=10)
	temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class QueryResponse(BaseModel):
	answer: str
	sources: list[dict]
	confidence: float

class OrderResponse(BaseModel):
	tracking_number: int
	order_id: str
	customer_name: str
	city: str
	product: str
	category: str
	status: str
	carrier: str
	track_url: str
	notes: str
	delayed: bool
	eta: str
	last_update: str

@asynccontextmanager
async def lifespan(app: FastAPI):
	global embedding_service, retriever, generator
	logger.info("Initializing EcoMarket RAG application...")
	settings = get_settings()
	embedding_service = EmbeddingService()
	retriever = DocumentRetriever(embedding_service)
	generator = ResponseGenerator()
	logger.info("Application initialized successfully")
	yield
	logger.info("Shutting down application...")

app = FastAPI(
	title="EcoMarket RAG API",
	description="RAG-based product information and recommendation system",
	version="1.0.0",
	docs_url="/docs",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
	lifespan=lifespan
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/")
async def root():
	return {"status": "healthy", "service": "EcoMarket RAG API"}

@app.get("/health")
async def health_check():
	return {
		"status": "healthy",
		"embedding_service": embedding_service is not None,
		"retriever": retriever is not None,
		"generator": generator is not None
	}

@app.get("/get_order", response_model=OrderResponse)
async def get_order(orden_servicio: str = FastAPIQuery(..., min_length=14, max_length=15)):
	import re
	if not orden_servicio or not re.match(r"^[A-Z]{3}-\d{4}-\d{5}$", orden_servicio):
		raise HTTPException(status_code=400, detail="El parámetro 'orden_servicio' es obligatorio y debe tener el formato correcto (ECO-2509-20001)")
	return OrderResponse(
		tracking_number=20001,
		order_id=orden_servicio,
		customer_name="Camila Torres",
		city="Pereira",
		product="Televisor Samsung 55 pulgadas",
		category="Electrónica",
		status="Enviado",
		carrier="Deprisa",
		track_url=f"https://tracking.ecomarket.example/deprisa/20001",
		notes="Entregado",
		delayed=False,
		eta="2025-09-27",
		last_update="2025-09-27"
	)

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
	import re
	try:
		logger.info(f"Processing query: {request.query}")
		# Buscar el patrón en cualquier parte del texto
		match = re.search(r"[A-Z]{3}-\d{4}-\d{5}", request.query)
		orden_servicio = match.group(0) if match else None
		logger.info(f"Orden de servicio detectada: {orden_servicio}")
		if orden_servicio:
			info_order = await get_order(orden_servicio)
			new_query = f"{request.query}\nDetalles de la orden de servicio:" \
						f"ID: {info_order.order_id} " \
						f"Cliente: {info_order.customer_name} " \
						f"Ciudad: {info_order.city} " \
						f"Producto: {info_order.category} {info_order.product} " \
						f"Tipo de producto: {info_order.category} " \
						f"Estado: {info_order.status} " \
						f"Transportista: {info_order.carrier} " \
						f"URL de seguimiento: {info_order.track_url} " \
						f"Notas: {info_order.notes} " \
						f"Retraso: {info_order.delayed} " \
						f"ETA: {info_order.eta} " \
						f"Última actualización: {info_order.last_update} "
		else:
			new_query = request.query
		logger.info(f"Información de la orden: {new_query}")
		documents = await retriever.retrieve(
			new_query,
			top_k=request.top_k
		)
		response = await generator.generate(
			query=new_query,
			documents=documents,
			temperature=request.temperature
		)
		return QueryResponse(
			answer=response["answer"],
			sources=response["sources"],
			confidence=response["confidence"]
		)
	except Exception as e:
		logger.error(f"Error processing query: {str(e)}")
		raise HTTPException(status_code=500, detail=str(e))
