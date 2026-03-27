# app/routes/mine.py
from flask import Blueprint, jsonify, request
from app.database import supabase
from app.blockchain import proof_of_work, validar_proof
import requests
import logging
import os

logger = logging.getLogger(__name__)
mine_bp = Blueprint("mine", __name__)

@mine_bp.route("/mine", methods=["POST"])
def minar():
    """
    Toma la primera transacción pendiente, ejecuta el Proof of Work,
    crea el bloque y lo propaga a los demás nodos.
    """
    try:
        # 1. Obtener la primera transacción pendiente
        pendientes = supabase.table("transacciones_pendientes") \
            .select("*") \
            .limit(1) \
            .execute().data
        
        if not pendientes:
            return jsonify({"mensaje": "⚠ No hay transacciones pendientes para minar"}), 200
        
        transaccion = pendientes[0]
        
        # 2. Obtener el último bloque para encadenar correctamente
        cadena = supabase.table("grados") \
            .select("hash_actual") \
            .order("creado_en", desc=True) \
            .limit(1) \
            .execute().data
        
        # Si no hay bloques, este es el bloque génesis (hash_anterior = "0")
        hash_anterior = cadena[0]["hash_actual"] if cadena else "0" * 64
        
        logger.info(f"⛏  Minando bloque para: {transaccion.get('titulo_obtenido')}")
        
        # 3. Ejecutar Proof of Work
        nonce, hash_actual = proof_of_work(
            persona_id=transaccion.get("persona_id", ""),
            institucion_id=transaccion.get("institucion_id", ""),
            titulo_obtenido=transaccion.get("titulo_obtenido", ""),
            fecha_fin=str(transaccion.get("fecha_fin", "")),
            hash_anterior=hash_anterior
        )
        
        # 4. Construir el bloque completo
        nuevo_bloque = {
            "persona_id":      transaccion.get("persona_id"),
            "institucion_id":  transaccion.get("institucion_id"),
            "programa_id":     transaccion.get("programa_id"),
            "fecha_inicio":    transaccion.get("fecha_inicio"),
            "fecha_fin":       transaccion.get("fecha_fin"),
            "titulo_obtenido": transaccion.get("titulo_obtenido"),
            "numero_cedula":   transaccion.get("numero_cedula"),
            "titulo_tesis":    transaccion.get("titulo_tesis"),
            "menciones":       transaccion.get("menciones"),
            "hash_actual":     hash_actual,
            "hash_anterior":   hash_anterior,
            "nonce":           nonce,
            "firmado_por":     os.getenv("NODE_ID", "nodo-desconocido")
        }
        
        # 5. Guardar el bloque en la cadena (tabla grados)
        supabase.table("grados").insert(nuevo_bloque).execute()
        logger.info(f"✅ Bloque añadido a la cadena local")
        
        # 6. Eliminar la transacción de pendientes
        supabase.table("transacciones_pendientes") \
            .delete() \
            .eq("id", transaccion["id"]) \
            .execute()
        
        # 7. Propagar el bloque a los demás nodos
        _propagar_bloque(nuevo_bloque)
        
        return jsonify({
            "mensaje": "✅ Bloque minado y propagado",
            "bloque": nuevo_bloque
        }), 201
    
    except Exception as e:
        logger.error(f"❌ Error al minar: {str(e)}")
        return jsonify({"error": str(e)}), 500

@mine_bp.route("/blocks/receive", methods=["POST"])
def recibir_bloque():
    """
    Endpoint para recibir un bloque propagado por otro nodo.
    Valida el hash y el PoW antes de aceptarlo.
    """
    bloque = request.get_json()
    
    logger.info(f"📥 Bloque recibido de otro nodo: {bloque.get('titulo_obtenido')}")
    
    # Validar el bloque antes de aceptarlo
    es_valido = validar_proof(
        persona_id=bloque.get("persona_id", ""),
        institucion_id=bloque.get("institucion_id", ""),
        titulo_obtenido=bloque.get("titulo_obtenido", ""),
        fecha_fin=str(bloque.get("fecha_fin", "")),
        hash_anterior=bloque.get("hash_anterior", ""),
        nonce=bloque.get("nonce", 0),
        hash_actual=bloque.get("hash_actual", "")
    )
    
    if not es_valido:
        logger.warning("⚠ Bloque rechazado: hash inválido o PoW no cumple dificultad")
        return jsonify({"error": "Bloque inválido"}), 400
    
    try:
        supabase.table("grados").insert(bloque).execute()
        logger.info("✅ Bloque externo aceptado y guardado")
        return jsonify({"mensaje": "Bloque aceptado"}), 201
    except Exception as e:
        logger.error(f"❌ Error al guardar bloque externo: {str(e)}")
        return jsonify({"error": str(e)}), 500

def _propagar_bloque(bloque: dict):
    """Envía el bloque minado a todos los nodos registrados."""
    try:
        nodos = supabase.table("nodos").select("url").execute().data or []
        
        for nodo in nodos:
            url_nodo = nodo["url"]
            try:
                resp = requests.post(
                    f"{url_nodo}/blocks/receive",
                    json=bloque,
                    timeout=3
                )
                logger.info(f"📡 Bloque propagado a {url_nodo}: {resp.status_code}")
            except requests.exceptions.RequestException as e:
                logger.warning(f"⚠ Nodo {url_nodo} no disponible: {str(e)}")
    
    except Exception as e:
        logger.error(f"❌ Error propagando bloque: {str(e)}")