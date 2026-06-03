from dotenv import load_dotenv
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    rabbitmq_url: str = "amqp://admin:admin123@localhost:5672/"
    api_gateway_base_url: str = "http://localhost:3000"

    # --- LLM Provider & Keys ---
    llm_provider: str = "openai"
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    
    google_genai_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("GOOGLE_GENAI_API_KEY", "GEMINI_API_KEY"),
    )
    google_genai_model: str = Field(
        default="gemini-2.0-flash",
        validation_alias=AliasChoices("GOOGLE_GENAI_MODEL", "GEMINI_MODEL"),
    )
    google_genai_timeout_ms: int = Field(
        default=120_000,
        validation_alias=AliasChoices("GOOGLE_GENAI_TIMEOUT", "GEMINI_TIMEOUT_MS"),
    )
    rag_llm_temperature: float = 0.2

    # --- Qdrant Vector Store ---
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection_name: str = "doctor_profiles"
    embedding_version: str = "v1"
    max_embedding_tokens: int = 1500  # Token limit instead of chars limit

    # (Duplicated block removed)

    # --- RabbitMQ / Microservices ---
    ai_rpc_queue: str = "ai_service_queue"
    ai_events_queue: str = "ai_service_events_queue"
    topic_exchange: str = "medicalink.topic"

    # --- Hybrid Qdrant ---
    rag_hybrid_enabled: bool = True
    dense_vector_name: str = "dense"
    sparse_vector_name: str = "lexical"
    fastembed_sparse_model: str = "Qdrant/bm25"
    retrieval_prefetch_limit: int = 40
    retrieval_llm_context_max: int = 24

    # --- Reranking ---
    rag_rerank_mode: str = "flashrank"
    rag_rerank_lexical_weight: float = 0.2
    flashrank_model: str = "ms-marco-MiniLM-L-12-v2"
    flashrank_cache_dir: str = ".cache/flashrank"
    rag_rerank_pool: int = 36
    
    # --- Multi-factor Ranking Weights ---
    ranking_weight_semantic: float = 0.50
    ranking_weight_lexical: float = 0.10
    ranking_weight_experience: float = 0.15
    ranking_weight_rating: float = 0.15
    ranking_weight_demographic: float = 0.10

    # --- Eval Log ---
    rag_eval_log_path: str = ""

    # --- Semantic Caching ---
    semantic_cache_enabled: bool = True
    semantic_cache_collection: str = "query_cache"
    semantic_cache_threshold: float = 0.95
    semantic_cache_model: str = "BAAI/bge-small-en-v1.5"

def get_settings() -> Settings:
    return Settings()
