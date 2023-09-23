from pathlib import Path
import os

from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

from data_questionnaire_agent.log_init import logger

def create_if_not_exists(folder):
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    assert folder.exists(), "Folder {folder} does not exist."


class Config:
    model = os.getenv("OPENAI_MODEL")
    request_timeout = int(os.getenv("REQUEST_TIMEOUT"))
    has_langchain_cache = os.getenv("LANGCHAIN_CACHE") == "true"
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model=model,
        temperature=0,
        request_timeout=request_timeout,
        cache=has_langchain_cache,
        streaming=True,
    )
    verbose_llm = os.getenv("VERBOSE_LLM") == "true"
    ui_timeout = int(os.getenv("UI_TIMEOUT"))
    project_root = Path(os.getenv("PROJECT_ROOT"))
    assert project_root.exists()
    question_cache_folder = os.getenv("QUESTION_CACHE_FOLDER")
    question_cache_folder_path = Path(question_cache_folder)

    create_if_not_exists(question_cache_folder_path)
    wkhtmltopdf_binary = Path(os.getenv("WKHTMLTOPDF_BINARY"))
    assert wkhtmltopdf_binary.exists()
    template_location = Path(os.getenv("TEMPLATE_LOCATION"))
    assert template_location.exists()
    pdf_folder = Path(os.getenv("PDF_FOLDER"))
    create_if_not_exists(pdf_folder)
    use_tasklist = os.getenv("TASKLIST") == "true"
    knowledge_base_path = Path(os.getenv("KNOWLEDGE_BASE_PATH"))
    show_chain_of_thought = os.getenv("SHOW_CHAIN_OF_THOUGHT") == 'true'

    # Embedding related
    raw_text_folder = Path(os.getenv("RAW_TEXT_FOLDER"))
    embeddings_persistence_dir = Path(os.getenv("EMBEDDINGS_PERSISTENCE_DIR"))
    chunk_size = int(os.getenv("EMBEDDINGS_CHUNK_SIZE"))
    embeddings = OpenAIEmbeddings(chunk_size=chunk_size)
    search_results_how_many = int(os.getenv("SEARCH_RESULTS_HOW_MANY"))

    # Questions
    questions_per_batch = int(os.getenv("QUESTIONS_PER_BATCH"))

cfg = Config()


class MailConfig:
    mail_user = os.getenv("MAIL_USER")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")
    mail_server = os.getenv("MAIL_SERVER")
    mail_from_person = os.getenv("MAIL_FROM_PERSON")


mail_config = MailConfig()

if __name__ == "__main__":
    logger.info("Model: %s", cfg.model)
    logger.info("Verbose: %s", cfg.verbose_llm)
    logger.info("mail_config user: %s", mail_config.mail_user)
    logger.info("wkhtmltopdf: %s", cfg.wkhtmltopdf_binary.as_posix())
    logger.info("template_location: %s", cfg.template_location.as_posix())
    logger.info("use_tasklist: %s", cfg.use_tasklist)