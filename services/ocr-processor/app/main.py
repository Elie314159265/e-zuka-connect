import os
import re
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import documentai, storage
from google.api_core.client_options import ClientOptions
from contextlib import asynccontextmanager

# 環境変数の設定
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("DOCAI_LOCATION", "us")
PROCESSOR_ID = os.getenv("DOCAI_PROCESSOR_ID", "your-document-ai-processor-id")

# クライアントの初期化（lifespan内で）
docai_client = None
storage_client = None
RESOURCE_NAME = None

class GcsUri(BaseModel):
    gcs_uri: str

def clean_and_convert_amount(amount_str: str) -> Optional[int]:
    """金額の文字列から数字以外の文字を削除し、整数に変換する"""
    if not amount_str:
        return None
    try:
        # 数字以外のすべての文字を削除
        cleaned_str = re.sub(r'[^\d]', '', amount_str)
        if cleaned_str:
            return int(cleaned_str)
        return None
    except (ValueError, TypeError):
        return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global docai_client, storage_client, RESOURCE_NAME
    docai_client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
    )
    storage_client = storage.Client()
    RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
    print("Clients initialized.")
    yield
    print("Shutting down.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "OCR Processor"}

@app.post("/process-gcs/")
async def process_receipt_from_gcs(payload: GcsUri):
    if not all([docai_client, storage_client, RESOURCE_NAME]):
        raise HTTPException(status_code=503, detail="Service is not initialized.")

    try:
        gcs_uri = payload.gcs_uri
        gcs_bucket_name, gcs_blob_name = gcs_uri.replace("gs://", "").split("/", 1)

        # GCSからファイルをダウンロード
        bucket = storage_client.bucket(gcs_bucket_name)
        blob = bucket.blob(gcs_blob_name)
        image_content = blob.download_as_bytes()
        
        # ファイルのMIMEタイプを取得
        mime_type = blob.content_type

        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )
        request = documentai.ProcessRequest(
            name=RESOURCE_NAME, raw_document=raw_document
        )
        result = docai_client.process_document(request=request)
        document = result.document

        total_amount = None
        supplier_name = None
        supplier_phone = None
        line_items = []

        for entity in document.entities:
            entity_type = entity.type_
            if entity_type == "total_amount":
                total_amount = clean_and_convert_amount(entity.mention_text)
            elif entity_type == "supplier_name":
                supplier_name = entity.mention_text
            elif entity_type == "supplier_phone":
                supplier_phone = entity.mention_text
            elif entity_type == "line_item":
                item_data = {}
                for prop in entity.properties:
                    if prop.type_ == "line_item/description":
                        item_data["description"] = prop.mention_text
                    elif prop.type_ == "line_item/amount":
                        item_data["amount"] = clean_and_convert_amount(prop.mention_text)
                if item_data:
                    line_items.append(item_data)
        
        if not total_amount and not supplier_name and not line_items:
            raise HTTPException(status_code=400, detail="Receipt information could not be extracted.")

        return {
            "supplier_name": supplier_name,
            "supplier_phone": supplier_phone,
            "total_amount": total_amount,
            "line_items": line_items,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))