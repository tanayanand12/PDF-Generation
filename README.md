<p align="center">
  <img src="https://img.icons8.com/ios-filled/100/000000/pdf.png" width="80" alt="PDF Icon"/>
  <img src="https://img.icons8.com/color/96/000000/artificial-intelligence.png" width="80" alt="AI Icon"/>
</p>

<h1 align="center">AI-Powered PDF Generation Service</h1>

<p align="center">
  <b>Generate beautiful, professional PDFs from structured input using FastAPI and GPT-powered layout intelligence.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-API-green?logo=fastapi">
  <img src="https://img.shields.io/badge/ReportLab-PDF-red?logo=adobe-acrobat-reader">
  <img src="https://img.shields.io/badge/OpenAI-GPT5-lightgrey?logo=openai">
</p>

---

## ✨ Features

- 🎨 **AI Layout Planning:** Uses GPT to analyze input and suggest optimal PDF layout, page breaks, and formatting.
- 🖨️ **Professional PDF Generation:** High-quality PDFs with custom styles using ReportLab.
- 🛡️ **Input & Output Validation:** Ensures input structure and generated PDFs are correct and robust.
- 🚀 **REST API:** Simple endpoints for PDF generation, download, and health checks.
- 🔒 **Configurable & Secure:** Uses environment variables for API keys and settings.

---

## 🗂️ Project Structure

```
.
├── .env
├── config.py
├── main.py
├── requirements_check.py
├── models/
│   └── schemas.py
├── services/
│   ├── gpt_planner.py
│   ├── pdf_generator.py
│   └── validation_agent.py
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd pdf_gen_agent_v2
```

### 2. Install Requirements

Check and install dependencies:

```sh
python requirements_check.py
# If any packages are missing, install them:
pip install -r requirements.txt
```

> **Note:** If `requirements.txt` is missing, install these manually:
> ```
> pip install fastapi uvicorn pydantic openai reportlab python-dotenv requests typing-extensions
> ```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your OpenAI API key and other settings:

```
OPENAI_API_KEY=sk-...
MODEL_ID_GPT5=gpt-5-2025-08-07
DEBUG=False
TEMP_DIR=/tmp
```

### 4. Run the Service

```sh
python main.py
```

The API will be available at [http://localhost:8734](http://localhost:8734).

---

## 🛠️ API Endpoints

### `POST /generate-pdf`

Generate a PDF from structured sections.

**Request Body:**

```json
{
  "sections": [
    {"Executive Summary": "This is the summary..."},
    {"Findings": "Key findings are..."}
  ],
  "filename": "report.pdf"
}
```

**Response:**

```json
{
  "success": true,
  "filename": "report.pdf",
  "download_url": "/download/report.pdf",
  "metadata": {
    "sections_count": 2,
    "layout_strategy": "standard_professional",
    "generated_at": "2024-06-07T12:34:56"
  }
}
```

### `GET /download/{filename}`

Download a generated PDF by filename.

### `GET /health`

Health check endpoint.

---

## 🧠 How It Works

<p align="center">
  <img src="https://img.icons8.com/fluency/96/000000/flow-chart.png" width="80" alt="Flowchart"/>
</p>

1. **Input Validation:** Checks that each section is a single key-value pair.
2. **Layout Planning:** <code>services.gpt_planner.GPTPlanner</code> uses GPT to suggest layout, page breaks, and formatting.
3. **PDF Generation:** <code>services.pdf_generator.PDFGenerator</code> builds the PDF using ReportLab, applying AI-suggested styles.
4. **Output Validation:** <code>services.validation_agent.ValidationAgent</code> checks the generated PDF for integrity.
5. **Download:** PDF is saved to a temp directory and can be downloaded via the API.

---

## ⚙️ Configuration

See [`config.py`](config.py) for all configurable options, including API host/port, model selection, and PDF defaults.

---

## 📦 Models

- [`models.schemas.PDFRequest`](models/schemas.py): Input model for PDF generation.
- [`models.schemas.PDFResponse`](models/schemas.py): Output model for PDF generation.
- [`models.schemas.LayoutPlan`](models/schemas.py): Layout plan from GPT.
- [`models.schemas.ValidationResult`](models/schemas.py): Validation result model.

---

## 👩‍💻 Development

- Logging is enabled for debugging.
- All code is type-annotated and uses Pydantic for data validation.
- To add new formatting rules or validation, extend the relevant service in [`services/`](services/).

---

## 📄 License

MIT License

---

<p align="center">
  <img src="https://img.icons8.com/color/48/000000/checked-checkbox.png" width="32"/>
  <b>Author: Tanay Anand</b>