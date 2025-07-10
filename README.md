# 🤖 SmartDoc Extractor – An MLOps-Powered Document Intelligence System

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![SpaCy](https://img.shields.io/badge/SpaCy-NLP-brightgreen?logo=spacy)](https://spacy.io/)
[![Tesseract OCR](https://img.shields.io/badge/OCR-Tesseract-blue?logo=tesseract)](https://github.com/tesseract-ocr/tesseract)
[![Docker](https://img.shields.io/badge/Docker-Containerized-informational?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-blue?logo=kubernetes)](https://kubernetes.io/)
[![CI/CD](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-success?logo=githubactions)](https://github.com/features/actions)
[![Postman Tested](https://img.shields.io/badge/API-Postman_Validated-orange?logo=postman)](https://www.postman.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**SmartDoc Extractor** is an end-to-end **MLOps-based intelligent document processing app** designed to extract, analyze, and convert unstructured documents (PDFs, scans, etc.) into structured information using:
- 🔍 Tesseract OCR
- 🧠 Custom-trained SpaCy Named Entity Recognition
- 🧾 PDF report generation with FPDF
- ⚙️ Modular pipelines, logging, exception handling, CI/CD, Docker, and Kubernetes

---

## 🎥 Demo


![MLOps Architecture](https://github.com/Harshitraiii2005/SmartDoc-Extractor/blob/main/SmartDoc-Extractor-GoogleChrome2025-07-1000-42-55-ezgif.com-video-to-gif-converter%20(2).gif)



## 📸 Screenshots

Here’s a quick look at the SmartDoc Extractor UI in action:

### 🖼️ 1. Upload Page  
![Upload Page](https://github.com/Harshitraiii2005/SmartDoc-Extractor/blob/main/SmartDoc-Extractor%20-%20Google%20Chrome%207_10_2025%209_16_51%20PM.png)

---

### 🧠 2. Entity Extraction Output  
![Entity Extraction Output](https://github.com/Harshitraiii2005/SmartDoc-Extractor/blob/main/SmartDoc-Extractor%20-%20Google%20Chrome%207_10_2025%209_17_12%20PM.png)

---

### 📄 3. PDF Summary Download  
![PDF Summary](https://github.com/Harshitraiii2005/SmartDoc-Extractor/blob/main/SmartDoc-Extractor%20-%20Google%20Chrome%207_10_2025%209_17_21%20PM.png)

---

### 🔁 4. Postman Request Demo  
![Postman Request Demo](https://github.com/Harshitraiii2005/SmartDoc-Extractor/blob/main/http___127.0.0.1_52012%20-%20Harshit%20Rai's%20Workspace%207_10_2025%203_45_40%20PM.png)


---

## 🚀 MLOps Workflow Architecture

The following architecture diagram visually represents the MLOps flow used in **SmartDoc Extractor** – from OCR to PDF generation, containerization, orchestration, and CI/CD integration.


![MLOps Architecture](https://github.com/Harshitraiii2005/SmartDoc-Extractor/blob/main/workflow.png)

### 🔄 Flow Summary:
- 📥 **Step 1: User Uploads Document**  
  A scanned PDF or image is uploaded to the web interface.

- 🔍 **Step 2: Tesseract OCR Engine**  
  Text is extracted from the image or PDF using Tesseract.

- 🧠 **Step 3: Custom NER with SpaCy**  
  The text is processed through a trained Named Entity Recognition (NER) model to detect key fields like Invoice Number, Date, Amount, etc.

- 🗃️ **Step 4: Entity Extraction**  
  All entities are extracted and structured in a clean format.

- 🧾 **Step 5: PDF Summary Generation**  
  The extracted content is compiled into a formatted PDF summary using `FPDF`.

- 🌐 **Step 6: Flask API Response**  
  The result is returned through a REST API with proper logging and exception handling.

### ⚙️ MLOps Components:
- 🐳 **Docker:** Containerizes the complete pipeline for environment consistency.
- ☸️ **Kubernetes (Minikube):** Manages container deployment locally.
- 🔁 **GitHub Actions:** Automates testing, image building, and Kubernetes deployment.
- 📋 **Postman-tested Endpoints:** Ensures endpoints are functioning across deployments.
- 📄 **Logging & Error Handling:** All errors, status, and inference flows are logged.

---




---

## 🧠 ML Component

| Task                   | Tool                            |
| ---------------------- | ------------------------------- |
| OCR                    | Tesseract                       |
| NLP Model              | SpaCy NER (trained on invoices) |
| PDF Generation         | FPDF                            |
| Preprocessing Pipeline | Python                          |

---

## ⚙️ Tech Stack

| Category             | Tools Used                            |
| -------------------- | ------------------------------------- |
| **Language**         | Python 3.10                           |
| **Framework**        | Flask (REST API)                      |
| **OCR**              | Tesseract OCR                         |
| **NLP**              | SpaCy (Custom NER Model)              |
| **PDF Output**       | FPDF                                  |
| **Containerization** | Docker                                |
| **Orchestration**    | Kubernetes with Minikube              |
| **CI/CD**            | GitHub Actions                        |
| **Testing**          | Postman                               |
| **Logging**          | Python Logging + Exception Management |

---

## 🧪 Tested on Local Server

* ✔️ API tested using **Postman** with multiple PDF & image formats
* ✔️ NER outputs validated using trained entities
* ✔️ Docker & Kubernetes deployment tested via Minikube
* ✔️ GitHub Actions workflow runs: **test → build → deploy**

---

## 📁 Project Structure

```bash
SmartDoc-Extractor/
│
├── app.py                   # Main Flask App
├── run_pipeline.py          # Preprocessing and pipeline execution
├── trained_invoice_ner/     # Trained SpaCy NER model
│
├── src/                     # All modular components
│   ├── data_cleaner.py
│   ├── data_Extraction.py
│   ├── data_feild_extraction.py
│   └── __init__.py
│
├── static/                  # Fonts & static assets
├── templates/               # Jinja2 templates for HTML rendering
│
├── Dockerfile               # Docker container config
├── deployment.yaml          # Kubernetes Deployment and Service
├── requirements.txt         # Python dependencies
├── .github/workflows/       # GitHub Actions workflow for CI/CD
├── README.md
└── LICENSE
```

---

## 🐳 Docker Deployment

```bash
# Build Docker Image
docker build -t smartdoc-extractor .

# Run Docker Container
docker run -d -p 5000:5000 --name smartdoc smartdoc-extractor
```

---

## ☸️ Kubernetes (Minikube) Deployment

```bash
# Start Minikube
minikube start

# Apply deployment
kubectl apply -f deployment.yaml

# Access service
minikube service smartdoc-service
```

---

## 🔄 CI/CD with GitHub Actions

> `.github/workflows/deploy.yml` handles:

* 🔍 Code linting
* 🧪 Pytest and validation
* 🐳 Docker build
* ☸️ Kubernetes rollout
* ✅ Post-deploy API tests

---

## 📂 API Endpoints

| Method | Endpoint        | Description                      |
| ------ | --------------- | -------------------------------- |
| POST   | `/extract`      | Upload document & extract fields |
| GET    | `/download/pdf` | Download generated summary PDF   |
| GET    | `/health`       | Health check endpoint            |

✅ Fully tested with Postman — import collection from `/tests/`

---

## ✅ Logging & Error Handling

* 📄 Log files stored in `/logs/`
* 🛑 Captures OCR failures, invalid uploads, model crashes
* 📬 Includes friendly Flask error messages with status codes

---

## 📈 Roadmap

* [ ] Add Swagger UI for API documentation
* [ ] Deploy to cloud Kubernetes (GKE/EKS)
* [ ] Add user authentication
* [ ] Build annotation tool for model retraining
* [ ] Add Streamlit UI version for non-tech users

---

## 🤝 Contributing

Contributions are welcome!

```bash
git clone https://github.com/yourusername/SmartDoc-Extractor
cd SmartDoc-Extractor
```

Please submit PRs with clear descriptions and commit messages.

---

## 📜 License

Licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for full rights and permissions.

---

## ✉️ Contact

> Made with ❤️ by **Harshit Rai**

* 📧 [upharshi2005@gmail.com](mailto:upharshi2005@gmail.com)
* 🔗 [LinkedIn](https://www.linkedin.com/in/harshit-rai-5b91142a8/)
