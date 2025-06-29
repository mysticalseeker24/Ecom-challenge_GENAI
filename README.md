# 🧠 Microservices Chatbot System

This project is a **microservices-based chatbot application** that intelligently processes user queries through a centralized `chat-service`, identifies the intent, and routes the request to the appropriate backend services — either `order-service` or `product-service`.

## 🧩 Architecture Overview

```
Frontend
   |
   ↓
Chat-Service
   ├──→ Order-Service  ──→ Mock API + LLM (order-related queries, uses Order_Data_Dataset.csv for data)
   └──→ Product-Service ──→ Pinecone + RAG + LLM (product-related queries)
```

### 1. **Frontend**

* Interface that accepts user queries and sends them to the `chat-service`.

### 2. **Chat-Service**

* Central logic to process and classify intents (e.g., order vs. product).
* Delegates to appropriate services:

  * Order-related → `order-service`
  * Product-related → `product-service`

### 3. **Order-Service**

* Fetches order information from a mock API using the `OrderDataset`.
* Formats the output using an LLM (OpenAI).

### 4. **Product-Service**

* Retrieves contextually relevant product information using Pinecone + RAG.
* Uses OpenAI for summarization and formatting.

---

## 🛠️ Setup Instructions

### 1. **Environment Variables**

Each service has its own `.env` file. Ensure the following keys are present in the environment:

```env
# chat-service .env
OPENAI_API_KEY=<open-ai api key>
PINECONE_API_KEY=<pinecone api key>
PINECONE_INDEX_NAME=<pinecone_index_name>

# order-service .env
OPENAI_API_KEY=<open-ai api key>

# product-service .env
OPENAI_API_KEY=<open-ai api key>
PINECONE_API_KEY=<pinecone api key>
PINECONE_INDEX_NAME=<pinecone_index_name>
EMBEDDING_MODEL=text-embedding-ada-002
RAG_TOP_K=5

# frontend .env.production
NEXT_PUBLIC_CHAT_SERVICE_API = "http://localhost:8000/api" // make sure to keep this url it is configured for docker services

```

*Refer to the `.env.example` files provided per service for exact values.*

---

### 2. **Preparing Pinecone (Product Dataset Index)**

Run the following script before starting the services to preprocess and upload product data to Pinecone:

```bash
python scripts/load_data.py
```

* This script:

  * Reads `Product_Information_Dataset.csv`
  * Preprocesses and chunks the data
  * Generates embeddings
  * Uploads them to Pinecone index (`rag-getting-started`)

---

## 🚀 Running the Application

After setting up the environment and initializing Pinecone:

```bash
docker-compose up --build
```

This will:

* Build all services
* Start containers for:

  * frontend
  * chat-service
  * order-service
  * product-service

---

## 🧪 How It Works

1. **User sends query** from frontend.
2. **Chat-service** uses intent classification to determine whether it's product- or order-related.
3. Depending on intent:

   * Queries are routed to either:

     * `order-service` → Mock API → Response → LLM formatting
     * `product-service` → Pinecone RAG → Response → LLM formatting
4. **Response is returned** to frontend and displayed to the user.

---

## 📦 Services Summary

| Service         | Description                              | Stack                       |
| --------------- | ---------------------------------------- | --------------------------- |
| frontend        | User-facing client                       | React / Next.js             |
| chat-service    | Intent analysis & routing logic          | FastAPI / Python            |
| order-service   | Handles order queries via mock APIs      | FastAPI / Python + OpenAI   |
| product-service | Handles product queries via Pinecone RAG | FastAPI / Python + Pinecone |

---

## 📁 Data Sources

* `Product_Information_Dataset.csv` — Source for product-service RAG system.
* `Order_Data_Dataset.csv`
* Mock API for orders — Used by order-service to simulate order information.

---

## ✅ Final Notes

* Ensure all environment variables are correctly set.
* You **must** run `load_data.py` before `docker-compose up --build`.
* The Pinecone index (`rag-getting-started`) must be initialized only once unless data changes.
* Visit [this](http://localhost:3000) to check the functionality.


## Example Screenshots

![](./public/Screenshot%202025-05-08%20194022.png)
![](./public/Screenshot%202025-05-08%20194058.png)
![](./public/Screenshot%202025-05-08%20194124.png)
![](./public/Screenshot%202025-05-08%20194202.png)
![](./public/Screenshot%202025-05-08%20194347.png)
![](./public/Screenshot%202025-05-08%20194435.png)