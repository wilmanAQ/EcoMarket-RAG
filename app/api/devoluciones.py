import os
import json
import re
from pathlib import Path
from glob import glob
from loguru import logger
import httpx
from app.config.settings import get_settings
from pydantic import BaseModel, Field

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
 
class DevolutionsGenerator:
    """
    Generates methods for managing devolutions
    """
    def __init__(self):
        """Initialize the DevolutionsGenerator"""
        logger.info("Initializing DevolutionsGenerator")
        settings = get_settings()


    async def buscar_devolucion_por_orden(self, orden_servicio: str) -> bool:
        """Busca una devolución por el ID de la orden de servicio"""
        docs_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs")
        json_path = os.path.join(docs_folder, "devoluciones_registradas.json")
        if not os.path.exists(json_path):
            return False
        with open(json_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return False
            try:
                data = json.loads(content)
            except Exception:
                logger.error("Error al cargar el archivo JSON de devoluciones")
                return False
            for registro in data:
                if registro.get("order_id") == orden_servicio:
                    return True
            return False

    async def registrar_devolucion_en_json(self, codigo_devolucion: str) -> bool:
        """Registra una devolución en un archivo JSON dado el código de devolución"""
        import re
        import json
        import httpx
        import os
        from pathlib import Path
        from glob import glob
        from app.config.settings import get_settings
        
        codigo = codigo_devolucion
                
        match = re.search(r"[A-Z]{3}-\d{4}-\d{5}-\d{6}", codigo)
        orden_servicio = match.group(0) if match else None
        if not orden_servicio:
            return False

        # Obtener dataset de órdenes
        with httpx.Client() as client:
            settings = get_settings()
            response = client.get(settings.endpointdataset)
            data = response.json()
            rows = data.get("rows", [])

        match_orden_servicio = re.search(r"[A-Z]{3}-\d{4}-\d{5}", orden_servicio)
        orden_servicio = match_orden_servicio.group(0) if match_orden_servicio else None
        if not orden_servicio:
            return False
        # Buscar la orden por order_id
        order = next((row for row in rows if row['row']['order_id'] == orden_servicio), None)

        if order:
            order_response = OrderResponse(
                tracking_number=order['row'].get('tracking_number', 0),
                order_id=order['row'].get('order_id', orden_servicio),
                customer_name=order['row'].get("customer_name", ""),
                city=order['row'].get("city", ""),
                product=order['row'].get("product", ""),
                category=order['row'].get("category", ""),
                status=order['row'].get("status", ""),
                carrier=order['row'].get("carrier", ""),
                track_url=order['row'].get("track_url", ""),
                notes=order['row'].get("notes", "") + f" Devolución registrada con código: {codigo}",
                delayed=order['row'].get("delayed", False),
                eta=order['row'].get("eta", ""),
                last_update=order['row'].get("last_update", "")
            )

            docs_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs")
            json_files = glob(os.path.join(docs_folder, "*.json"))
            try:
                for json_path in json_files:
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if not content:
                                json_data = []
                            else:
                                json_data = json.loads(content)
                        json_data.append(order_response.dict())
                        with open(json_path, "w", encoding="utf-8") as f:
                            json.dump(json_data, f, ensure_ascii=False, indent=2)
                    except Exception:
                        return False
            except Exception:
                logger.error(f"Error al registrar la devolución en los archivos JSON.")
                return False
            return True
        else:
            return False
    
        
