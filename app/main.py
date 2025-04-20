# app/main.py
import os, datetime, logging, nltk, chromadb, json, uuid
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from app.models.search_models import SearchRequest, SearchResponse, ErrorResponse
from app.models.chat_models import ChatRequest, ChatResponse
from app.models.data_loader_models import DataLoaderResponse
from app.models.service_stats_models import ServiceStatsResponse
from app.services.llm_interface import ChatModel
from app.services.prompt_manager import PromptManager
from app.services.helpers import transcript_to_string, get_directory_size
from dotenv import load_dotenv

# Load Environment Variables 
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
llm_provider = os.getenv("LLM_PROVIDER", "ollama")
persist_directory = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")

# Load the pre trained Sentence Transformer Model 
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initalise ChromaDB Client 
chroma_client = chromadb.PersistentClient(path=persist_directory)
collection = chroma_client.get_or_create_collection("sentence_embeddings")

# FastAPI App 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
# Initialise the LLM Client
llm_client = ChatModel(provider=llm_provider)
# Initialise Prompt Manager
prompt_manager = PromptManager()
# Setup Logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.get("/service_stats", response_model=ServiceStatsResponse)
async def get_service_stats():
    try:
        db_size_bytes = get_directory_size(persist_directory)
        db_size_mb = round(db_size_bytes / (1024 * 1024), 2)
        document_count = collection.count()
        last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return ServiceStatsResponse(
            status="Online",
            dbSize=str(db_size_mb),
            documentCount=document_count,
            lastUpdated=last_updated
        )
    except Exception as e:
        logger.error(f"Error getting service stats: {e}")
        return ServiceStatsResponse(
            status="Degraded",
            dbSize="0",
            documentCount=0,
            lastUpdated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

@app.post("/search", response_model=SearchResponse, responses={500: {"model": ErrorResponse}})
def search(request_data: SearchRequest):
    try:
        logger.info(f"Received search query: {request_data.query}")

        query_embedding = model.encode(request_data.query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            include=["documents"]
        )
        if results and results['documents']:
            return {"results": results['documents'][0]}
        else:
            return {"results": []}
    except Exception as e:
        logger.error(f"An error occurred in /search: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during search")

@app.post("/chat", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
def chat(request_data: ChatRequest):
    try:
        logger.info(f"Received chat message: {request_data.message}")

        if llm_provider == 'openai':
            tool_call_prompt = prompt_manager.get_prompt("tool_call_prompt")(message=request_data.message)
            llm_returned_queries = json.loads(llm_client.chat_completion(messages=[{"role": "user", "content": tool_call_prompt}]))
            if not isinstance(llm_returned_queries, list):
                raise HTTPException(status_code=400, detail="LLM returned queries are not in list format")
            llm_returned_queries = llm_returned_queries[:5]

            queries = []
            for i in range(0,len(llm_returned_queries)):
                search_results = search(SearchRequest(query=llm_returned_queries[i]))
                if search_results and search_results["results"]:
                    queries.extend(search_results["results"])
            queries = list(set(queries))
            search_results_text = ". ".join(result for result in queries) if len(queries) > 0 else "No information found."
            logger.info(f"Search results: {search_results_text}")

            enhancement_prompt = prompt_manager.get_prompt("enhancement_prompt")(context=search_results_text, message=request_data.message)
            response = llm_client.chat_completion(messages=[{"role": "user", "content": enhancement_prompt}])
            if not response:
                raise HTTPException(status_code=500, detail="No response from LLM")
            return ChatResponse(response=response)
                
        elif llm_provider == 'ollama':
            search_results = search(SearchRequest(query=request_data.message))
            if search_results and search_results["results"]:
                search_results_text = ". ".join(result for result in search_results["results"])
                logger.info(f"Search results: {search_results_text}")

                enhancement_prompt = prompt_manager.get_prompt("enhancement_prompt")(context=search_results_text, message=request_data.message)
                response = llm_client.chat_completion(messages=[{"role": "user", "content": enhancement_prompt}])
                return ChatResponse(response=response)
            else:
                raise HTTPException(status_code=500, detail="No results found in the database")
        else:
            raise HTTPException(status_code=400, detail="Invalid LLM provider specified")

    except Exception as e:
        logger.error(f"An unexpected error occurred in /chat: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@app.post("/data_loader", response_model=DataLoaderResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def data_loader(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text_content = content.decode('utf-8')
        
        if not text_content:
            raise HTTPException(status_code=400, detail="File is empty")
            
        logger.info(f"Received file for data_loader: {file.filename}")

        parsed_data = transcript_to_string(text_content)
        chunks = nltk.sent_tokenize(parsed_data)
    
        embeddings = model.encode(chunks)
        unique_ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        print(f"Unique IDs generated: {unique_ids}")

        collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            ids=unique_ids
        )

        return DataLoaderResponse(message=f"Successfully loaded {len(chunks)} chunks from {file.filename}")
    except UnicodeDecodeError:
        logger.error(f"Unable to decode file as UTF-8: {file.filename}")
        raise HTTPException(status_code=400, detail="File is not a valid text file")
    except Exception as e:
        logger.error(f"An error occurred in /data_loader: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during data loading")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=os.getenv('PORT'), log_level="info", reload=True)