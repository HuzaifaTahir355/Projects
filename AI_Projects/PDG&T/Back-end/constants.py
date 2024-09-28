NOT_ALLOWED_FORMATS: list[str] = ["BMP", "GIF", "JPEG", "PNG", "TIFF", "APNG", "AVIF", "WebP", "ICO", "EPS", "SVG",
                                  "MP4", "AVI", "MOV", "WMV", "FLV", "MPG", "MPEG", "3GP", "AMV", "ASF",
                                  "MP3", "WAV", "AAC", "WMA", "SND", "RA", "AU", "OGG", "FLAC", "M4A"]

DEFAULT_CHUNK_SIZE: int = 800

EMBEDDING_MODEL_WITH_DIMENSIONS: list[dict] = [{"model": "BAAI/bge-large-en-v1.5", "dimension": 1024},
                                               {"model": "sentence-transformers/all-mpnet-base-v2", "dimension": 768},
                                               {"model": "sentence-transformers/all-MiniLM-L6-v2", "dimension": 384}]

VECTOR_STORES: list[str] = ["Pinecone", "Milvus"]

VECTOR_DB_INDEX_NAME = "pdg-index"

LLMS = ["gpt-4o-mini", "meta-llama/Llama-3-70b-chat-hf"]