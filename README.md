# 🧠 Project Management AI Assistant

An AI-powered assistant that lets you interact with your project data using natural language. Get instant, conversational answers about tasks, timelines, and team assignments—just like talking to a human teammate.

---

## 🌐 Live Deployment

* 🔗 **Frontend**: \[[https://langtrack-project-assistant.vercel.app/](https://langtrack-project-assistant.vercel.app/)]
* 🔗 **Backend (API Docs)**: \[[https://langtrack-server.onrender.com/docs](https://langtrack-server.onrender.com/docs)]

---

## 🌟 Key Features

### ✅ Natural Language Interface

Ask questions like:

* "Who's working on Project Beta?"
* "What tasks are pending?"
* "Is Alpha Website behind schedule?"
* "Which projects is Bob assigned to?"

### 🤖 AI-Powered Insights

Backed by Google Gemini AI, the assistant can:

* Summarize project status
* Identify team workloads
* Flag task delays or priorities

### ⚙️ Simple Integration

* FastAPI-based backend
* Built-in mock project JSON data
* Minimal configuration required

---

## 🛠️ Technologies & Concepts Used

This project integrates **modern AI, vector search, and backend technologies**:

* **FastAPI** → High-performance Python backend for API endpoints.
* **Google Gemini (Generative AI API)** → Powers natural language understanding and response generation.
* **Embeddings (`text-embedding-001`)** → Converts text into dense vectors for semantic search.
* **Pinecone Vector Database** → Stores and retrieves embeddings efficiently.
* **Cosine Similarity** → Used as the metric to find the most relevant project data.
* **Dynamic Prompting** → Prompts are built on the fly using retrieved context.
* **Zero-Shot Prompting** → The AI answers without any pre-defined examples, only context + query.
* **System & User Prompts** → System role defines assistant behavior; user role provides the actual question.
* **Evaluation Dataset** → Ingests project data from a CSV dataset hosted on Hugging Face.

---

## 🏗️ Project Structure

```
Project-Management-AI/
│
├── app/                  # Backend (FastAPI)
│   ├── __init__.py
│   ├── main.py           # Core application logic
│   ├── embeddings.py     # Google Gemini embeddings
│   ├── pinecone_client.py# Vector DB setup (Pinecone)
│   ├── rag_utils.py      # Prompt building & text chunking
│   ├── ingest.py         # Ingest dataset into Pinecone
│   ├── mock_data.py      # Sample project JSON data
│   └── .env              # Environment variables (API Key)
│
└── README.md             # Project documentation
```

---

## 🚀 Quick Start

### 1. Clone and Setup Environment

```bash
git clone [your-repo-url]
cd server
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn google-generativeai python-dotenv pinecone-client pandas
```

### 3. Configure API Keys

Create a `.env` file in the `app/` directory with the following:

```env
GOOGLE_API_KEY=your_api_key_here
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name
EMBED_DIM=3072
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

Visit the API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 💻 Frontend Setup (Next.js + TypeScript + ShadCN)

1. Navigate to frontend

```bash
cd ../client
```

2. Install dependencies

```bash
npm install
```

3. Start the development server

```bash
npm run dev
```

App will be available at [http://localhost:3000](http://localhost:3000)

---

## 📡 API Endpoints

| Endpoint  | Method | Description                      |
| --------- | ------ | -------------------------------- |
| `/ask`    | POST   | Ask questions about project data |
| `/health` | GET    | Service status check             |

### 🧪 Sample Request

```bash
curl -X POST "http://localhost:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question":"Who is working on Alpha Website?"}'
```

---

## ⚙️ How It Works

1. User sends a natural language question via the API.
2. Query is embedded into vectors using Google Gemini.
3. Pinecone retrieves the most relevant project data using cosine similarity.
4. A **dynamic prompt** is built with the context.
5. Gemini AI generates a zero-shot answer.
6. FastAPI returns the structured result as JSON.

---

## 📚 Resources

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Google Gemini API Docs](https://ai.google.dev/)
* [Pinecone Documentation](https://docs.pinecone.io/)
* [Example Project Data](./app/mock_data.py)

---

> Built with ❤️ using Google Gemini, Pinecone, and FastAPI.
