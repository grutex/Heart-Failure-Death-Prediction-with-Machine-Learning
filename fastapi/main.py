import io
import os
import json
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field

import boto3
import pandas as pd
import logging
from fastapi import FastAPI, UploadFile, File
from sqlalchemy import create_engine, text
from predict import HeartFailurePredictor, build_ensemble_model

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Ingestão e Predição")

# ---------- MinIO (S3 compatível) ----------
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

BUCKET = os.getenv("S3_BUCKET", "dados-analise")

# ---------- Postgres ----------
db_url = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(db_url)

# --- Modelo preditor ---
predictor = None

@app.on_event("startup")
def init_bucket_and_db():
    global predictor
    
    print("\n[STARTUP] Iniciando configuração...")
    
    # garante bucket
    try:
        print("[STARTUP] Conectando ao MinIO...")
        resp = s3.list_buckets()
        buckets = [b["Name"] for b in resp.get("Buckets", [])]
        print(f"[STARTUP] Buckets existentes: {buckets}")
        
        if BUCKET not in buckets:
            print(f"[STARTUP] Criando bucket '{BUCKET}'...")
            s3.create_bucket(Bucket=BUCKET)
            print(f"[STARTUP] ✅ Bucket '{BUCKET}' criado")
        else:
            print(f"[STARTUP] ✅ Bucket '{BUCKET}' já existe")
        logger.info(f"Bucket '{BUCKET}' pronto")
    except Exception as e:
        print(f"[STARTUP] ❌ Erro com MinIO: {e}")
        logger.error(f"Erro ao criar bucket: {e}", exc_info=True)

    # teste rápido de conexão db
    try:
        print("[STARTUP] Conectando ao PostgreSQL...")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[STARTUP] ✅ PostgreSQL conectado")
        logger.info("Conexão com PostgreSQL OK")
    except Exception as e:
        print(f"[STARTUP] ❌ Erro PostgreSQL: {e}")
        logger.error(f"Erro ao conectar PostgreSQL: {e}", exc_info=True)
    
    # Carregar modelo
    try:
        print("[STARTUP] Carregando modelo...")
        default_model = build_ensemble_model()
        predictor = HeartFailurePredictor(model=default_model)
        print("[STARTUP] ✅ Modelo carregado com sucesso!")
        logger.info("✅ Modelo carregado com sucesso!")
    except Exception as e:
        print(f"[STARTUP] ❌ Erro ao carregar modelo: {e}")
        logger.error(f"Erro ao carregar modelo: {e}", exc_info=True)
    
    print("[STARTUP] 🚀 API pronta!\n")


@app.get("/")
def teste_api():
    return {"status": "ok", "msg": "API rodando"}


# =========================================================
# 1) Endpoint original para upload de CSV (mantido)
# =========================================================
@app.post("/enviarDados")
async def enviar_dados(file: UploadFile = File(...)):
    """
    Recebe um CSV, salva bruto no MinIO e grava em tabela dados_analise no Postgres.
    """
    content = await file.read()

    # 1) Guarda o arquivo bruto no MinIO
    key = f"{file.filename}"
    s3.put_object(Bucket=BUCKET, Key=key, Body=content)

    # 2) Lê em DataFrame e grava no banco
    df = pd.read_csv(io.BytesIO(content))
    df.to_sql("dados_analise", engine, if_exists="replace", index=False)

    return {
        "status": "ok",
        "s3_key": key,
        "rows": len(df),
        "columns": list(df.columns),
    }


# =========================================================
# 2) Endpoint para receber telemetria do ThingsBoard COM PREDIÇÃO
# =========================================================

class HeartData(BaseModel):
    age: float
    anaemia: int
    creatinine_phosphokinase: int
    diabetes: int
    ejection_fraction: int
    high_blood_pressure: int
    platelets: float
    serum_creatinine: float
    serum_sodium: int
    sex: int
    smoking: int
    time: int
    DEATH_EVENT: Optional[int] = None

@app.post("/enviarDadosThingsBoard")
async def enviar_dados_thingsboard(data: HeartData):
    """
    Endpoint chamado pelo ThingsBoard.
    - Faz predição primeiro
    - Salva o JSON completo (com DEATH_EVENT predito) no MinIO.
    - Grava em tabela dados_analise no Postgres.
    - Retorna predição com todos os dados + DEATH_EVENT predito.
    """
    
    # 0. Fazer a Predição PRIMEIRO
    predicted_death_event = None
    try:
        if predictor is None:
            logger.error("Predictor é None!")
            return {
                "status": "error",
                "message": "Preditor não inicializado",
                "DEATH_EVENT": None
            }
        
        # Preparar dados: remover DEATH_EVENT (será predito)
        data_dict = data.dict()
        data_dict.pop('DEATH_EVENT', None)
        
        # Fazer predição
        prediction_result = predictor.predict(data_dict)
        predicted_death_event = int(prediction_result["DEATH_EVENT"])
        logger.info(f"Predição realizada: {prediction_result}")
        
    except Exception as e:
        logger.error(f"Erro ao fazer predição: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e),
            "DEATH_EVENT": None
        }
    
    # 1. Salvar Dado Bruto no MinIO (COM o DEATH_EVENT predito)
    try:
        file_name = f"record_{pd.Timestamp.now().isoformat()}.json"
        # Montar JSON com DEATH_EVENT predito
        data_to_save = data.dict()
        data_to_save['DEATH_EVENT'] = predicted_death_event
        body = json.dumps(data_to_save)
        print(f"[DEBUG] Salvando em MinIO - Bucket: {BUCKET}, Arquivo: {file_name}")
        s3.put_object(Bucket=BUCKET, Key=file_name, Body=body)
        print(f"[DEBUG] ✅ Arquivo salvo em MinIO com sucesso!")
        logger.info(f"Dado salvo em MinIO: {file_name}")
    except Exception as e:
        print(f"[DEBUG] ❌ Erro ao salvar em MinIO: {e}")
        logger.error(f"Erro ao salvar em S3: {e}", exc_info=True)

    # 2. Salvar no Postgres (COM o DEATH_EVENT predito)
    try:
        data_dict = data.dict()
        data_dict['DEATH_EVENT'] = predicted_death_event
        df = pd.DataFrame([data_dict])
        df.to_sql('dados_analise', engine, if_exists='append', index=False)
        logger.info("Dado salvo em PostgreSQL")
    except Exception as e:
        logger.error(f"Erro ao salvar em PostgreSQL: {e}")

    # 3. Retornar resposta com todos os dados + DEATH_EVENT predito
    response = {
        "age": data.age,
        "anaemia": data.anaemia,
        "creatinine_phosphokinase": data.creatinine_phosphokinase,
        "diabetes": data.diabetes,
        "ejection_fraction": data.ejection_fraction,
        "high_blood_pressure": data.high_blood_pressure,
        "platelets": data.platelets,
        "serum_creatinine": data.serum_creatinine,
        "serum_sodium": data.serum_sodium,
        "sex": data.sex,
        "smoking": data.smoking,
        "time": data.time,
        "DEATH_EVENT": predicted_death_event
    }
    
    logger.info(f"Resposta: {response}")
    return response