# 🧠 Project Management AI Assistant

An AI-powered assistant that lets you interact with your project data using natural language. Get instant, conversational answers about tasks, timelines, and team assignments—just like talking to a human teammate.

---

## 🌐 Live Deployment

- 🔗 **Frontend**: [Frontend URL Here]
- 🔗 **Backend (API)**: [Backend URL Here]

---

## 🌟 Key Features

### ✅ Natural Language Interface  
Ask questions like:
- "Who's working on Project Beta?"
- "What tasks are pending?"
- "Is Alpha Website behind schedule?"
- "Which projects is Bob assigned to?"

### 🤖 AI-Powered Insights  
Backed by Google Gemini AI, the assistant can:
- Summarize project status
- Identify team workloads
- Flag task delays or priorities

### ⚙️ Simple Integration  
- FastAPI-based backend  
- Built-in mock project JSON data  
- Minimal configuration required

---

## 🏗️ Project Structure

```

Project-Management-AI/
│
├── app/                  # Backend (FastAPI)
│   ├── __init__.py
│   ├── main.py           # Core application logic
│   ├── mock_data.py      # Sample project JSON data
│   └── .env              # Environment variables (API Key)
│
└── README.md             # Project documentation

````

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
````

### 2. Install Dependencies

```bash
pip install fastapi uvicorn google-generativeai python-dotenv
```

### 3. Configure API Key

Create a `.env` file in the `app/` directory with the following:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

Visit the API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 💻 Frontend Setup (Next.js + TypeScript + ShadCN)

1. **Navigate to frontend**

```bash
cd ../client
```

2. **Install dependencies**

```bash
npm install
```

3. **Start the development server**

```bash
npm run dev
```

App will be available at [http://localhost:3000](http://localhost:3000)

> 💡 The frontend is fully responsive and styled with modern UI libraries.

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

## 🛠️ Customization

### 🔧 Edit Mock Data

Modify `app/mock_data.py` to include:

* Your actual team members
* Real projects and tasks
* Custom deadlines or timelines

### 🎯 Enhance Responses

Tweak the prompt formatting in `main.py` to:

* Customize response tone (e.g., formal, friendly)
* Include KPIs or completion percentages
* Format answers as bullet points or summaries

---

## ⚙️ How It Works

1. User sends a natural language question via the API.
2. System embeds project data into context.
3. Gemini AI processes the question with the embedded data.
4. AI generates a relevant, human-like answer.
5. FastAPI returns the formatted result.

---

## 📚 Resources

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Google Gemini API Docs](https://ai.google.dev/)
* [Example Project Data](./app/mock_data.py)

---

> Built with ❤️ using LangChain, Google Gemini, and FastAPI.




