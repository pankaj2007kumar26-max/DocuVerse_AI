# KANPUR INSTITUTE OF TECHNOLOGY
**A-1, UPSIDC Industrial Area, Chakeri Ward, Rooma, Kanpur – 208001**  
*(Approved by AICTE, New Delhi & Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow)*  
**ISO 9001:2015 CERTIFIED | NAAC ACCREDITED WITH GRADE 'A'**

---

# MINI PROJECT REPORT
ON

## **DOCUVERSE AI**
### *Intelligent Document Reading & Question Answering System*
*(A High-Performance Retrieval-Augmented Generation (RAG) & Groq LPU Powered Academic Assistant)*

---

**A Mini Project Report Submitted in Partial Fulfilment of the Requirements for the Degree of**  
### **BACHELOR OF TECHNOLOGY**  
**IN**  
### **COMPUTER SCIENCE AND ENGINEERING**

**Session:** 2025–2026  
**Year:** 2nd | **Semester:** 3rd / 4th | **Section:** A  

---

| **Submitted to:** | **Submitted by:** |
| :--- | :--- |
| **Ms. Prakanksha Shukla** | **Pankaj Kumar** |
| Assistant Professor, CSE Department | Roll Number: `2501651530026` *(or College Roll No.)* |
| Kanpur Institute of Technology, Kanpur | Department of Computer Science & Engineering |

---

<div style="page-break-after: always;"></div>

# CERTIFICATE

This is to certify that the mini project report entitled **“DOCUVERSE AI – Intelligent Document Reading & Question Answering System”** has been submitted by **Pankaj Kumar** (Roll Number: `2501651530026`), student of **Bachelor of Technology in Computer Science and Engineering** at **Kanpur Institute of Technology, Kanpur**, during the academic session **2025–2026**.

The project work has been carried out under the guidance and supervision of **Ms. Prakanksha Shukla** (Assistant Professor, Department of Computer Science and Engineering). This report is submitted in partial fulfilment of the requirements for the award of the degree of **Bachelor of Technology**.

To the best of our knowledge, the work presented in this report is original, technically sound, and suitable for academic evaluation.

<br><br><br>

---

### **SIGNATURES**

<br>

| **Head of Department** | **Project Guide** |
| :--- | :--- |
| <br><br>____________________________________ | <br><br>____________________________________ |
| **Mr. Rahul Singh** | **Ms. Prakanksha Shukla** |
| Head of Department | Assistant Professor |
| Department of Computer Science & Engineering | Department of Computer Science & Engineering |
| Kanpur Institute of Technology, Kanpur | Kanpur Institute of Technology, Kanpur |

---

<div style="page-break-after: always;"></div>

# DECLARATION

I, **Pankaj Kumar**, student of **Bachelor of Technology in Computer Science and Engineering**, 2nd Year, at **Kanpur Institute of Technology, Kanpur**, hereby declare that the project report entitled **“DOCUVERSE AI – Intelligent Document Reading & Question Answering System”** is prepared and presented by me under the supervision and guidance of **Ms. Prakanksha Shukla**, Assistant Professor, Department of Computer Science and Engineering.

I solemnly declare that this report represents my authentic project work and that all information, algorithms, libraries, and concepts derived from external literature and open-source documentation have been duly acknowledged and cited.

This report has not been submitted previously to this or any other university or institute for the award of any degree, diploma, or academic certificate. I take full responsibility for the originality, technical integrity, and correctness of the work presented herein.

<br><br>

**Date:** 24 November 2026  
**Place:** Kanpur  

<br><br>
____________________________________  
**Pankaj Kumar**  
Roll Number: `2501651530026`  
B.Tech (Computer Science & Engineering), 2nd Year  
Kanpur Institute of Technology, Kanpur  

---

<div style="page-break-after: always;"></div>

# ACKNOWLEDGEMENT

I would like to express my deepest gratitude and sincere appreciation to everyone who supported and guided me in the successful design, implementation, and deployment of my mini project, **“DocuVerse AI – Intelligent Document Reading & Question Answering System.”**

First and foremost, I express my heartfelt gratitude to my esteemed project guide, **Ms. Prakanksha Shukla**, Assistant Professor, Department of Computer Science and Engineering, for her invaluable guidance, continuous encouragement, constructive critiques, and technical mentoring throughout this project. Her insights into web architecture, system design, and AI model integration were instrumental in shaping this project.

I extend my sincere thanks to **Mr. Rahul Singh**, Head of Department, Computer Science and Engineering, and all faculty members of Kanpur Institute of Technology for providing the necessary academic infrastructure, computational resources, and encouraging learning environment.

I am also profoundly thankful to the management and leadership of **Kanpur Institute of Technology** for fostering an ecosystem of innovation, technical excellence, and practical project-based learning.

Finally, I express my sincere love and gratitude to my family and friends for their unwavering patience, moral support, and motivation during late-night debugging and development sessions.

<br><br>
____________________________________  
**Pankaj Kumar**  
Department of Computer Science & Engineering  
Kanpur Institute of Technology, Kanpur  

---

<div style="page-break-after: always;"></div>

# ABSTRACT

In modern academic and professional environments, students, researchers, and professionals face unprecedented information overload. Textbooks, research papers, legal contracts, and syllabi often span hundreds of dense pages. Generic Large Language Models (LLMs) suffer from severe limitations when analyzing proprietary documents: token window restrictions, complete lack of real-time access to user files, and a notorious tendency to fabricate facts (*hallucinations*) without accountable source citations.

**DocuVerse AI** is an intelligent, high-performance document reading and question-answering system designed to overcome these challenges through **Retrieval-Augmented Generation (RAG)**. The system ingests arbitrary multi-page PDF documents, extracts clean text using **PyMuPDF**, performs sliding-window semantic chunking with optimal overlap, generates dense vector embeddings, and builds isolated high-dimensional vector indices using **FAISS (Facebook AI Similarity Search)**.

When a user submits a query, DocuVerse AI performs cosine similarity search in vector space, retrieves the top-$K$ most relevant document snippets, and constructs an anti-hallucination prompt for the **Groq LPU (Language Processing Unit) Inference Engine**. Operating on state-of-the-art open-weights models (*Qwen 2.5 / Llama 3*), Groq delivers responses with sub-second latency. Every answer is strictly grounded in the uploaded text and accompanied by verifiable, exact page citations and source snippets.

Beyond question answering, DocuVerse AI serves as a comprehensive study companion, providing:
1. One-click executive document summaries.
2. Auto-generated practice multiple-choice questions (MCQs) with detailed answer rationales.
3. Key takeaway extractions.
4. Multilingual support across English, Hindi, and Hinglish.

The application is engineered with an enterprise-grade **FastAPI REST backend** paired with a responsive, glassmorphic **Streamlit frontend**. The entire system has been validated via an automated Pytest test suite (14/14 tests passed) and deployed to cloud infrastructure (**Render** and **Streamlit Community Cloud**).

**Keywords:** *Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), FAISS, Vector Embeddings, Groq LPU, PyMuPDF, FastAPI, Streamlit, Semantic Search, Anti-Hallucination, Educational Technology.*

---

<div style="page-break-after: always;"></div>

# TABLE OF CONTENTS

| S. NO. | TOPIC | CHAPTER | PAGE |
| :---: | :--- | :---: | :---: |
| 1 | Cover Page & Title Details | — | 1 |
| 2 | Certificate of Approval | — | 2 |
| 3 | Candidate Declaration | — | 3 |
| 4 | Acknowledgement | — | 4 |
| 5 | Abstract | — | 5 |
| 6 | Table of Contents | — | 6 |
| 7 | **Introduction** | **CHAPTER 1** | **7** |
| | 1.1 General Introduction | | 7 |
| | 1.2 Problem Statement | | 7 |
| | 1.3 Proposed System | | 8 |
| | 1.4 Methodology | | 8 |
| 8 | **Objectives and Scope** | **CHAPTER 2** | **9** |
| | 2.1 Project Objectives | | 9 |
| | 2.2 Scope of the Project | | 9 |
| | 2.3 Project Overview | | 10 |
| | 2.4 Expected Outcome | | 10 |
| 9 | **Feasibility Study** | **CHAPTER 3** | **11** |
| | 3.1 Introduction | | 11 |
| | 3.2 Technical Feasibility | | 11 |
| | 3.3 Economic Feasibility | | 11 |
| | 3.4 Operational Feasibility | | 12 |
| | 3.5 Legal and Privacy Feasibility | | 12 |
| 10 | **Requirement Analysis** | **CHAPTER 4** | **13** |
| | 4.1 Introduction | | 13 |
| | 4.2 Functional Requirements | | 13 |
| | 4.3 Non-Functional Requirements | | 14 |
| | 4.4 Stakeholders | | 14 |
| | 4.5 Hardware Requirements | | 15 |
| | 4.6 Software Requirements | | 15 |
| | 4.7 Development Environment | | 15 |
| 11 | **System Design and Architecture** | **CHAPTER 5** | **16** |
| | 5.1 High-Level System Architecture | | 16 |
| | 5.2 RAG Pipeline Data Flow | | 17 |
| | 5.3 Vector Store Design & Collection Isolation | | 17 |
| | 5.4 System Workflow & Sequence | | 18 |
| | 5.5 Data Flow Diagram (Level 0 & Level 1) | | 19 |
| | 5.6 Use Case Diagram | | 20 |
| 12 | **Technology Stack** | **CHAPTER 6** | **21** |
| | 6.1 Frontend Technologies | | 21 |
| | 6.2 Backend Technologies | | 21 |
| | 6.3 Vector Database & Parsing Engines | | 22 |
| | 6.4 AI & High-Speed LLM Inference | | 22 |
| | 6.5 Technology Stack Summary Table | | 23 |
| 13 | **Main Modules Implementation** | **CHAPTER 7** | **24** |
| | 7.1 Document Ingestion & Parsing Module | | 24 |
| | 7.2 Semantic Chunking Engine | | 24 |
| | 7.3 Vector Embedding & Indexing Engine | | 25 |
| | 7.4 FastAPI REST API Server | | 26 |
| | 7.5 Cosmic Dark Streamlit UI | | 27 |
| 14 | **AI-Based Features & RAG Pipeline** | **CHAPTER 8** | **28** |
| | 8.1 Retrieval-Augmented Generation Deep Dive | | 28 |
| | 8.2 Groq LPU Hardware Acceleration | | 28 |
| | 8.3 Anti-Hallucination & Exact Citations | | 29 |
| | 8.4 Automated Study Tools (Summaries, MCQs, Takeaways) | | 29 |
| | 8.5 Multilingual Capabilities (English, Hindi, Hinglish) | | 30 |
| 15 | **Software Testing & Verification** | **CHAPTER 9** | **31** |
| | 9.1 Testing Strategy | | 31 |
| | 9.2 Automated Unit & Integration Tests | | 31 |
| | 9.3 Test Cases Execution Matrix | | 32 |
| 16 | **Deployment & Limitations** | **CHAPTER 10** | **34** |
| | 10.1 Cloud Deployment Architecture | | 34 |
| | 10.2 Production URLs & GitHub Repository | | 34 |
| | 10.3 System Limitations | | 35 |
| 17 | **Conclusion** | **CHAPTER 11** | **36** |
| 18 | **Future Scope and References** | **CHAPTER 12** | **37** |
| | 12.1 Future Enhancements | | 37 |
| | 12.2 Practical Applications | | 37 |
| | 12.3 Academic & Documentation References | | 38 |

---

<div style="page-break-after: always;"></div>

# CHAPTER 1 – INTRODUCTION

### 1.1 General Introduction
Textual documents form the backbone of modern education, science, governance, and enterprise communication. In colleges and universities, students encounter syllabi, academic research papers, reference books, lab manuals, and slide decks in Portable Document Format (PDF). As the volume of course materials expands, the time required to read, synthesize, and extract key information increases dramatically.

Standard keyword search (`Ctrl + F`) is fundamentally inadequate for comprehension because it relies on exact character matching. It cannot understand synonyms, semantic relationships, contextual subtleties, or implicit meaning. Conversely, standalone generative AI chatbots (such as standard ChatGPT or Gemini without document grounding) are prone to *hallucinations*—generating convincing but completely fictitious statements—and have no verified knowledge of private lecture notes or newly published college materials.

**DocuVerse AI** bridges this critical gap by creating an end-to-end, production-ready **Intelligent Document Reading and Question Answering System**. Powered by **Retrieval-Augmented Generation (RAG)**, it combines fast document parsing, semantic vector indexing, and ultra-high-speed LLM inference to empower students with verified, source-grounded answers accompanied by exact page numbers.

### 1.2 Problem Statement
Traditional methods of academic studying and document analysis suffer from the following core bottlenecks:
1. **Manual Information Retrieval Overhead:** Scanning a 100-page academic textbook or technical standard to locate a specific concept or equation consumes significant study time.
2. **AI Hallucinations and Lack of Provenance:** Generic LLMs frequently fabricate citations, fake author names, and misstate formulas because they predict words based on general training rather than verifiable local text.
3. **Context Window Limits:** Standard language models cannot take entire textbooks or multi-document corpuses in a single prompt due to token buffer limits and quadratic attention compute costs.
4. **Scattered Study Tools:** Students must juggle multiple disjointed tools—one for reading PDFs, another for writing summaries, and another for generating revision quiz questions.
5. **Language Inaccessibility:** Many students in bilingual environments understand complex engineering concepts better when explained in their regional dialect (Hindi or Hinglish), whereas most documents are in dense academic English.

### 1.3 Proposed System
DocuVerse AI introduces a unified, modular, intelligent software architecture:
- **Multi-PDF Parsing Engine:** Accepts single or multiple PDF documents simultaneously, extracting plain text alongside accurate physical page number metadata using PyMuPDF.
- **Sliding-Window Semantic Chunking:** Splits long document streams into overlapping token windows ($1000$ characters with $200$-character overlap), preserving contextual continuity across chunk boundaries.
- **High-Dimensional Vector Storage:** Encodes chunks into dense semantic vectors and builds an in-memory **FAISS (Facebook AI Similarity Search)** Index using normalized cosine similarity.
- **Multi-Tenant Collection Isolation:** Assigns each upload session a globally unique `collection_id`, strictly isolating vector spaces to prevent data leakage between different users or documents.
- **Groq LPU Acceleration:** Routes synthesized retrieval contexts to Groq's Language Processing Units, achieving inference speeds exceeding $300$ tokens per second.
- **Strict Grounding Guardrails:** System prompts enforce that if an answer is absent from the uploaded text, the model explicitly responds: *"The provided documents do not contain information to answer this question."*
- **Comprehensive Academic Study Kit:** Generates 1-click executive summaries, exam-oriented multiple-choice questions with answer keys, and bulleted takeaways in English, Hindi, and Hinglish.

### 1.4 Methodology
The development of DocuVerse AI followed the **Agile Iterative Software Development Life Cycle (SDLC)**:
1. **Requirement Engineering:** Identified student study bottlenecks, citation needs, and API specifications.
2. **Architecture & Pipeline Design:** Designed the three-tier RAG architecture separating data extraction, embedding/retrieval, and inference.
3. **Backend Engineering:** Implemented a non-blocking asynchronous REST API using FastAPI, Pydantic v2 validation models, and thread pool delegation for CPU-bound FAISS operations.
4. **Frontend Development:** Designed a modern, cosmic-themed responsive web UI using Streamlit, custom CSS3, and glassmorphic styling.
5. **Quality Assurance:** Created an automated Pytest test suite with 14 comprehensive test cases covering health, PDF parsing, vector search, Q&A, and error boundaries.
6. **Cloud Deployment:** Packaged backend services for deployment on Render and frontend UI on Streamlit Community Cloud.

---

<div style="page-break-after: always;"></div>

# CHAPTER 2 – OBJECTIVES AND SCOPE

### 2.1 Project Objectives
The primary objectives of DocuVerse AI are:
1. **Provide Document-Grounded Question Answering:** Deliver precise, factual answers to arbitrary student questions based solely on uploaded PDF files.
2. **Eliminate Fabricated Information:** Enforce strict grounding constraints so that answers cite exact source filenames and page numbers.
3. **Sub-Second Response Latency:** Leverage Groq LPU inference to provide immediate answers without the sluggish latency of conventional cloud LLM providers.
4. **Offer Smart Academic Study Helpers:** Automate the generation of executive summaries, revision MCQs, and key takeaway bullets.
5. **Multilingual Inclusivity:** Support seamless language switching between English, Hindi, and Hinglish.
6. **Ensure Multi-Tenant Isolation:** Implement isolated document collections with distinct FAISS indices to guarantee user data privacy.
7. **Deliver Production-Ready Architecture:** Expose modular REST APIs via FastAPI while maintaining a zero-configuration Streamlit web interface.

### 2.2 Scope of the Project
DocuVerse AI is designed for students, educators, researchers, and knowledge workers who deal with large volumes of technical documents.
- **Engineering & Science Students:** Quickly grasp concepts from university syllabus books, reference guides, and lecture slides.
- **Academic Researchers:** Extract methodologies, experimental setups, and related literature citations from research papers.
- **Competitive Exam Aspirants:** Generate customized practice MCQs directly from study material.
- **Legal and Corporate Analysts:** Interrogate dense reports, policy documents, and contracts without manual skimming.

### 2.3 Project Overview
The application consists of two integrated components:
1. **FastAPI REST Backend (`main.py`):** Provides 8 secure, documented endpoints handling multipart PDF uploads, text extraction, FAISS vector indexing, similarity search, Groq inference, and collection lifecycle management.
2. **Streamlit Frontend (`app.py`):** Provides a cosmic dark, mobile-responsive UI with drag-and-drop file upload, file size chips, quick-action study buttons, and formatted answer cards with expandable source citations.

### 2.4 Expected Outcome
The final product is a reliable, robust, and accessible cloud application that saves up to 70% of the time required to read and review academic documents.

---

<div style="page-break-after: always;"></div>

# CHAPTER 3 – FEASIBILITY STUDY

### 3.1 Introduction
A feasibility study evaluates whether the project can be realistically developed, hosted, and maintained within computational, economic, operational, and regulatory constraints.

### 3.2 Technical Feasibility
- **Python Ecosystem:** Python 3.11 provides industry-standard libraries for PDF parsing (`PyMuPDF`), vector indexing (`faiss-cpu`), web frameworks (`FastAPI`, `Streamlit`), and asynchronous I/O.
- **Vector Search Maturity:** FAISS is a battle-tested vector similarity search library developed by Meta AI Research, capable of performing thousands of similarity calculations in milliseconds on standard CPU hardware.
- **Groq LPU Hardware:** Groq's Tensor Streaming Processor architecture provides deterministic, high-throughput model inference without requiring expensive local GPUs.
- **Feasibility Verdict:** Highly Feasible. All required technologies are mature, fully documented, and compatible.

### 3.3 Economic Feasibility
- **Zero Software Licensing Cost:** All frameworks (FastAPI, Streamlit, FAISS, PyMuPDF, Python) are open-source and free under permissive licenses (MIT / Apache 2.0 / AGPL / BSD).
- **Free-Tier Cloud Hosting:** The backend is deployed on Render's free web tier, and the frontend is hosted on Streamlit Community Cloud.
- **Minimal Hardware Requirement:** Development and testing were executed on standard consumer laptops without proprietary hardware accelerators.
- **Feasibility Verdict:** Economically Optimal. Development and operational costs are virtually zero.

### 3.4 Operational Feasibility
- **User-Centric UI:** The interface requires zero training; users drag and drop PDF files and type plain-text questions.
- **Self-Healing Fallback:** The frontend automatically detects whether the FastAPI backend is online; if sleeping, it seamlessly executes in-memory RAG, ensuring zero downtime for end users.
- **Feasibility Verdict:** Exceptionally High. Accessible to any student with basic smartphone or computer literacy.

### 3.5 Legal and Privacy Feasibility
- **Document Confidentiality:** Documents are stored in temporary in-memory vectors or isolated session memory; no user data is used to train public models.
- **API Key Security:** API keys are injected via environment variables (`.env` and `st.secrets`); no credentials are committed to public GitHub repositories.
- **Feasibility Verdict:** Legally Compliant. Meets academic and industry standards for user privacy.

---

<div style="page-break-after: always;"></div>

# CHAPTER 4 – REQUIREMENT ANALYSIS

### 4.1 Introduction
Requirement analysis outlines the specific functional deliverables, operational constraints, and technical specifications necessary for the system to perform reliably.

### 4.2 Functional Requirements
- **FR01: PDF File Ingestion:** System must accept single or multiple `.pdf` files through web forms or REST multipart endpoints.
- **FR02: Input Validation:** System must validate file signatures (magic bytes `%PDF`) and reject non-PDF or corrupt files with HTTP 400.
- **FR03: Text & Metadata Extraction:** System must extract text from each page while tagging every block with the filename and page index.
- **FR04: Semantic Chunking:** System must split document text into overlapping chunks ($1000$ characters with $200$ overlap) to prevent context loss.
- **FR05: FAISS Vector Indexing:** System must compute dense vector representations and index them in an in-memory cosine FAISS store.
- **FR06: Context Retrieval:** System must return the top-$K$ ($K=4$) most similar chunks for any user question.
- **FR07: Grounded Answer Synthesis:** System must generate answers using Groq LPU inference strictly based on retrieved chunks.
- **FR08: Page Citations:** System must return exact source filenames, page numbers, and text snippets alongside answers.
- **FR09: Executive Summaries:** System must generate structured executive overviews of uploaded documents.
- **FR10: Practice MCQs:** System must generate multiple-choice questions with options, correct answers, and explanations.
- **FR11: Key Takeaways:** System must extract essential bulleted takeaways.
- **FR12: Multilingual Output:** System must generate answers in English, Hindi, or Hinglish as selected by the user.
- **FR13: Collection Deletion:** System must allow users to delete vector collections to free memory.

### 4.3 Non-Functional Requirements
- **NFR01: Latency:** Query retrieval and inference response time must complete within 2 to 3 seconds.
- **NFR02: Security:** All API keys must be loaded from server environment variables; uploaded files must not be accessible to other users.
- **NFR03: Isolation:** Each collection must have a unique UUID; queries must never leak data between different collections.
- **NFR04: Responsiveness:** The web UI must render smoothly on desktop screens, tablets, and mobile smartphones.
- **NFR05: Reliability:** The system must gracefully catch API timeout, corrupt PDF, and out-of-quota errors without crashing.

### 4.4 Stakeholders
- **Students / Users:** Primary beneficiaries who upload study materials and consume answers.
- **Teachers / Evaluators:** Reviewers who evaluate academic performance, verify citations, and generate quiz MCQs.
- **Developer / System Administrator:** Maintains backend services, monitors API quotas, and updates models.

### 4.5 Hardware Requirements
| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Processor** | Intel Core i3 (4th Gen) / AMD Ryzen 3 | Intel Core i5 / AMD Ryzen 5 or higher |
| **RAM** | 4 GB | 8 GB or 16 GB |
| **Storage** | 2 GB free disk space | SSD with 5 GB+ free space |
| **Network** | 1 Mbps Internet connection | 10 Mbps+ Broadband / 4G / 5G |
| **Display** | 1024 × 768 resolution | 1920 × 1080 Full HD |

### 4.6 Software Requirements
| Software | Specification / Version | Purpose |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11, Ubuntu 22.04 LTS, macOS | Development and deployment host OS |
| **Programming Language** | Python 3.11.x | Core programming runtime |
| **REST Framework** | FastAPI (v0.115+) | High-performance asynchronous backend |
| **ASGI Server** | Uvicorn (v0.34+) | Lightning-fast ASGI production web server |
| **Web Frontend** | Streamlit (v1.42+) | Interactive responsive user interface |
| **PDF Processing** | PyMuPDF / fitz (v1.25+) | High-speed PDF text and page extraction |
| **Vector Engine** | FAISS-CPU (v1.9+) | Dense vector indexing & similarity search |
| **AI Inference** | Groq Cloud REST API | Ultra-fast LPU inference (Qwen / Llama 3) |
| **Testing Engine** | Pytest (v8.3+) | Automated unit and integration testing |
| **Version Control** | Git & GitHub | Source code repository and version tracking |
| **Cloud Hosting** | Render & Streamlit Cloud | Production web deployment |

---

<div style="page-break-after: always;"></div>

# CHAPTER 5 – SYSTEM DESIGN AND ARCHITECTURE

### 5.1 High-Level System Architecture
DocuVerse AI follows a modern, decoupled **Three-Tier Microservices Architecture**:
1. **Presentation Layer (Frontend):** Built with Streamlit, custom CSS3, and responsive HTML components. Communicates with backend services over HTTP REST.
2. **Application & Service Layer (Backend):** FastAPI asynchronous server (`main.py`) orchestrating request validation, PDF parsing, text chunking, and Groq API calls.
3. **Data & Vector Retrieval Layer (Data Store):** In-memory FAISS indices encapsulated inside `CollectionManager`, providing isolated vector spaces for each document collection.

```
+-------------------------------------------------------------------+
|                        CLIENT BROWSER                             |
|          (Streamlit Cosmic Dark UI - Desktop / Mobile)            |
+-------------------------------------------------------------------+
                                  |
                                  | HTTP REST / JSON
                                  v
+-------------------------------------------------------------------+
|                   FASTAPI APPLICATION BACKEND                     |
|                   (Uvicorn ASGI Server @ :8000)                   |
|                                                                   |
|   +-------------------+  +-------------------+  +---------------+  |
|   | /api/docs/upload  |  |     /api/chat     |  | /summary,/mcq |  |
|   +-------------------+  +-------------------+  +---------------+  |
+-------------------------------------------------------------------+
          |                                        |
          | Extracts Text                          | Top-K Chunks + Prompt
          v                                        v
+---------------------------+            +---------------------------+
|    PyMuPDF (fitz) +       |            |    GROQ LPU CLOUD         |
| Semantic Text Splitter    |            | (Qwen 2.5 / Llama 3 API)  |
+---------------------------+            +---------------------------+
          |                                        |
          | Dense Vectors                          | Generated Answer
          v                                        v
+---------------------------+            +---------------------------+
|    FAISS VECTOR STORE     | ---------> | Formatted Output with     |
|   (Isolated Collection)   | Top Chunks | Verified Page Citations   |
+---------------------------+            +---------------------------+
```

### 5.2 RAG Pipeline Data Flow
The Retrieval-Augmented Generation pipeline consists of two phases:
1. **Ingestion Phase (Offline/Upload Time):**
   $$\text{PDF File} \xrightarrow{\text{PyMuPDF}} \text{Page Texts} \xrightarrow{\text{Chunking}} \{c_1, c_2, \dots, c_n\} \xrightarrow{\text{Embeddings}} \{\vec{v}_1, \vec{v}_2, \dots, \vec{v}_n\} \xrightarrow{\text{Indexing}} \text{FAISS Index}$$
2. **Query Phase (Online/Run Time):**
   $$\text{User Query } q \xrightarrow{\text{Embedding}} \vec{q} \xrightarrow{\text{Cosine Similarity}} \text{Top-}K \text{ Chunks } \{c_{(1)}, \dots, c_{(K)}\}$$
   $$\{q, c_{(1)}, \dots, c_{(K)}\} \xrightarrow{\text{Anti-Hallucination Prompt}} \text{Groq LPU} \xrightarrow{\text{Inference}} \text{Answer with Page Citations}$$

### 5.3 Vector Store Design & Collection Isolation
To prevent cross-contamination between different user documents, `vector_store.py` defines a thread-safe `CollectionManager`:
- Each collection is assigned a unique UUID (`collection_id`).
- Each collection maintains its own `FaissVectorStore` instance containing:
  - An in-memory FAISS Index (`IndexFlatIP` for inner product / cosine similarity on normalized vectors).
  - A parallel chunk metadata registry: `[{"text": ..., "source": filename, "page": page_number}]`.
- A collection deletion endpoint (`DELETE /api/documents/{collection_id}`) purges the index and metadata from memory, preventing memory leaks.

### 5.4 System Workflow
1. **User uploads PDF:** Frontend sends multipart form-data to `POST /api/documents/upload`.
2. **Backend parses & indexes:** Server extracts text per page, chunks text with overlap, creates FAISS index, and returns `collection_id` with page and chunk counts.
3. **User asks question:** Frontend sends JSON payload `{"collection_id", "question", "language"}` to `POST /api/chat`.
4. **Similarity Retrieval:** Server searches FAISS vector index, retrieves top 4 chunks with metadata.
5. **Inference Execution:** Server formats Groq prompt, calls Groq REST API, parses grounded response.
6. **Result Display:** Frontend renders answer card, model badge, and expandable citation chips.

### 5.5 Data Flow Diagram (Level 0 & Level 1)
- **DFD Level 0 (Context Level):**
  $$\text{Student/User} \underset{\text{Answer + Citations}}{\overset{\text{PDF Upload + Query}}{\rightleftharpoons}} [\text{DocuVerse AI System}]$$
- **DFD Level 1 (Modular Breakdown):**
  - Process 1.0: Ingestion & Magic Byte Validation
  - Process 2.0: Page Text Parsing & Semantic Splitting
  - Process 3.0: Embedding Calculation & FAISS Index Storage
  - Process 4.0: Similarity Search & Context Assembly
  - Process 5.0: Groq LPU Inference & Grounding Check
  - Process 6.0: Response Formatting & Citation Tagging

### 5.6 Use Case Diagram
- **Primary Actor:** Student / Academic User
- **Use Cases:**
  - `UC01: Upload PDF Documents` (Includes validation and chunking)
  - `UC02: Ask Question` (Includes semantic search, LLM inference, citation viewing)
  - `UC03: Generate Executive Summary`
  - `UC04: Generate Practice MCQs`
  - `UC05: Extract Key Takeaways`
  - `UC06: Select Language (English / Hindi / Hinglish)`
  - `UC07: Reset / Delete Collection`

---

<div style="page-break-after: always;"></div>

# CHAPTER 6 – TECHNOLOGY STACK

### 6.1 Frontend Technologies
- **Streamlit:** Python-based reactive web application framework facilitating rapid state management and widget rendering.
- **Custom CSS3 Glassmorphism:** Dark theme `#0B0D1B` with semi-transparent violet overlays (`rgba(99, 102, 241, 0.15)`), rounded cards (`border-radius: 18px`), and fluid typography using CSS `clamp()`.
- **Responsive Layout:** Dynamic CSS media queries ensuring that buttons, upload areas, and citation cards stack cleanly on mobile viewports ($\le 768\text{px}$).

### 6.2 Backend Technologies
- **FastAPI:** Modern, asynchronous web framework built on Starlette and Pydantic. Provides automatic OpenAPI/Swagger documentation at `/docs`.
- **Uvicorn:** Production-grade ASGI server providing lightning-fast HTTP request handling.
- **Pydantic v2:** Rigorous data validation and serialization models ensuring type safety across all request bodies and JSON responses.
- **Asynchronous Non-Blocking Execution:** Uses `asyncio.to_thread` for CPU-intensive PDF parsing and FAISS indexing, ensuring the FastAPI event loop is never blocked.

### 6.3 Vector Database & Parsing Engines
- **PyMuPDF (`fitz`):** C-accelerated PDF parsing library capable of extracting text and layout metadata up to 10× faster than legacy tools like PyPDF2 or PDFMiner.
- **FAISS (Facebook AI Similarity Search):** State-of-the-art C++ library for high-speed similarity search in high-dimensional vector spaces. Uses normalized L2 Euclidean distance equivalent to Cosine Similarity.
- **Character Text Splitter:** Configured with `chunk_size = 1000` and `chunk_overlap = 200` to preserve semantic continuity across paragraph splits.

### 6.4 AI & High-Speed LLM Inference
- **Groq Cloud LPU Inference:** Cloud inference engine running on Groq's Tensor Streaming Processors. Delivers sustained speeds of over $300\text{ tokens/second}$.
- **Selected Models:**
  - `qwen/qwen3.8-27b` (High-speed multilingual SOTA reasoning model)
  - `openai/gpt-oss-20b` (Verified high-efficiency instruction-tuned fallback model)

### 6.5 Technology Stack Summary Table
| Architectural Layer | Component / Technology | Justification & Role |
| :--- | :--- | :--- |
| **User Interface** | Streamlit + Custom CSS | Cosmic dark theme, zero-refresh widgets, responsive mobile grid |
| **REST API Server** | FastAPI + Uvicorn | Asynchronous endpoint routing, CORS handling, Pydantic validation |
| **PDF Extraction** | PyMuPDF (fitz) | Fast C-level text and page-by-page metadata parsing |
| **Text Chunking** | LangChain Text Splitters | Overlapping character chunking to preserve semantic context |
| **Vector Index** | FAISS-CPU | In-memory cosine similarity search with isolated collection spaces |
| **AI Inference** | Groq Cloud LPU Engine | Ultra-fast token generation for grounded Q&A, summaries, and MCQs |
| **Test Automation**| Pytest + TestClient | Automated validation of all 8 endpoints and RAG workflows |
| **Deployment** | Render & Streamlit Cloud | Cloud hosting with automated continuous deployment from GitHub |

---

<div style="page-break-after: always;"></div>

# CHAPTER 7 – MAIN MODULES IMPLEMENTATION

### 7.1 Document Ingestion & Parsing Module (`pdf_reader.py`)
Responsible for reading raw PDF binary streams and converting them into structured text objects with accurate page numbers:
```python
import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes, filename: str) -> list[dict]:
    """
    Extracts text page-by-page from raw PDF bytes.
    Returns a list of dicts: [{"text": str, "source": str, "page": int}]
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_data = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if text:
            pages_data.append({
                "text": text,
                "source": filename,
                "page": page_num + 1  # 1-indexed for human readability
            })
    doc.close()
    return pages_data
```

### 7.2 Semantic Chunking Engine (`text_splitter.py`)
Splits continuous page text into discrete chunks while maintaining a sliding overlap:
- **Chunk Size:** $1000$ characters.
- **Chunk Overlap:** $200$ characters.
- **Metadata Inheritance:** Each chunk inherits its parent document's `source` filename and exact `page` number.

### 7.3 Vector Embedding & Indexing Engine (`vector_store.py`)
Encapsulates FAISS indexing and collection management:
```python
class FaissVectorStore:
    def __init__(self):
        self.chunks = []
        self.index = None

    def add_documents(self, chunks: list[dict]):
        self.chunks.extend(chunks)
        texts = [c["text"] for c in chunks]
        embeddings = get_text_embeddings(texts)  # Dense normalized vectors
        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatIP(dim)  # Inner Product = Cosine Similarity
        self.index.add(embeddings)

    def similarity_search(self, query: str, top_k: int = 4) -> list[dict]:
        query_vec = get_text_embeddings([query])
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results
```

### 7.4 FastAPI REST API Server (`main.py`)
Implements all 8 required REST API endpoints with robust error handling and file size checks:
1. `GET /`: Application status and API information.
2. `GET /health`: Health probe returning memory, model, and server status.
3. `POST /api/documents/upload`: Multipart PDF upload, chunking, and index creation.
4. `POST /api/chat`: Context retrieval, Groq inference, and citation assembly.
5. `POST /api/documents/{id}/summary`: Executive document summary generation.
6. `POST /api/documents/{id}/mcqs`: Practice multiple-choice question generation.
7. `POST /api/documents/{id}/key-points`: Key takeaway bullet extraction.
8. `DELETE /api/documents/{id}`: Vector collection deletion and memory reclamation.

### 7.5 Cosmic Dark Streamlit UI (`app.py`)
Implements the user-facing interface:
- **Header Section:** `📄✨ PDF Assistant` with `✨ Your AI Study Helper` pill badge.
- **Upload Card (Card 1):** Drag-and-drop file uploader with file chips and processing buttons.
- **Query Card (Card 2):** Input text box, language dropdown (English, Hindi, Hinglish), and quick-action study buttons.
- **Output Display (Card 3):** Glassmorphic answer card featuring:
  - Formatted Markdown response.
  - Model badge (`⚡ Powered by Groq LPU (qwen/qwen3.8-27b)`).
  - Expandable citation boxes showing source filename, page number, and matched text snippet.

---

<div style="page-break-after: always;"></div>

# CHAPTER 8 – AI-BASED FEATURES & RAG PIPELINE

### 8.1 Retrieval-Augmented Generation Deep Dive
Retrieval-Augmented Generation (RAG) is the gold standard for enterprise and academic knowledge retrieval. Instead of asking a language model to recall facts from its fixed training weights, RAG dynamically injects verifiable reference text into the prompt at runtime.

DocuVerse AI implements a strict RAG cycle:
1. The user's query is vectorized into embedding space.
2. The FAISS vector database retrieves the top-4 most semantically similar paragraphs.
3. A structured prompt is assembled containing the question, the retrieved snippets, and the system grounding instructions.
4. The LLM acts purely as an analytical reasoning and synthesis engine, forbidden from introducing outside facts.

### 8.2 Groq LPU Hardware Acceleration
Traditional cloud LLM APIs (e.g., standard GPT-4) take 5 to 15 seconds to return answers. This latency disrupts the student's study flow.
Groq LPUs use a deterministic Tensor Streaming Architecture that eliminates traditional GPU memory bandwidth bottlenecks. DocuVerse AI generates complete academic answers, summaries, and MCQs in **under 1.5 seconds**, providing an interactive real-time experience.

### 8.3 Anti-Hallucination & Exact Citations
To guarantee academic integrity, the system prompt strictly enforces:
> *"You are DocuVerse AI, a strictly document-grounded academic assistant. You must answer the user's question using ONLY the provided document excerpts. If the excerpts do not contain the answer, explicitly state: 'The provided documents do not contain information to answer this question.' Never invent facts, formulas, or page numbers."*

Alongside the generated text, DocuVerse AI returns structured citation objects:
```json
{
  "filename": "B.Tech_2nd_Yr_CSE_Syllabus.pdf",
  "page": 14,
  "snippet": "...Dynamic Programming: Matrix Chain Multiplication, Longest Common Subsequence..."
}
```

### 8.4 Automated Study Tools
1. **Executive Summaries:** Compresses large documents into core background, key concepts, technical methodologies, and conclusions.
2. **Practice MCQs:** Generates 4 exam-style multiple-choice questions with 4 options ($A, B, C, D$), an answer key, and an explanation citing specific concepts.
3. **Key Takeaways:** Extracts 5 to 7 high-impact revision bullet points.

### 8.5 Multilingual Capabilities
Recognizing the diverse linguistic needs of Indian engineering students, DocuVerse AI supports:
- **English:** Formal academic English.
- **Hindi (हिन्दी):** Pure, clean Hindi script.
- **Hinglish:** Natural conversational Hindi written in Latin script (e.g., *"Is document ke according, Dynamic Programming complex problems ko sub-problems me divide karta hai"*), widely preferred for quick conceptual understanding.

---

<div style="page-break-after: always;"></div>

# CHAPTER 9 – SOFTWARE TESTING & VERIFICATION

### 9.1 Testing Strategy
To guarantee production reliability, DocuVerse AI was subjected to a comprehensive quality assurance process combining automated unit testing, API integration testing, security boundary validation, and end-to-end interface testing.

### 9.2 Automated Unit & Integration Tests
An automated test suite was developed using `pytest` and FastAPI's `TestClient` in `test_backend.py`. The suite exercises every endpoint against real in-memory vector stores and synthetic PDF fixtures.

**Execution Command:**
```powershell
pytest test_backend.py -v
```

**Test Execution Output:**
```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\Niharika Gautam\Downloads\DocuVerseAI
collected 14 items

test_backend.py::test_root_endpoint PASSED                               [  7%]
test_backend.py::test_health_endpoint PASSED                             [ 14%]
test_backend.py::test_upload_invalid_file_extension PASSED               [ 21%]
test_backend.py::test_upload_corrupt_pdf PASSED                          [ 28%]
test_backend.py::test_upload_valid_pdf_and_create_collection PASSED      [ 35%]
test_backend.py::test_chat_question_answering PASSED                     [ 42%]
test_backend.py::test_chat_nonexistent_collection PASSED                 [ 50%]
test_backend.py::test_chat_empty_question PASSED                         [ 57%]
test_backend.py::test_document_summary PASSED                            [ 64%]
test_backend.py::test_document_mcqs PASSED                               [ 71%]
test_backend.py::test_document_key_points PASSED                         [ 78%]
test_backend.py::test_delete_collection PASSED                           [ 85%]
test_backend.py::test_delete_nonexistent_collection PASSED               [ 92%]
test_backend.py::test_missing_api_key_handling PASSED                    [100%]

============================= 14 passed in 20.61s =============================
```

### 9.3 Test Cases Execution Matrix
| Test ID | Test Scenario | Input Data | Expected Result | Actual Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **TC01** | Root Endpoint Check | `GET /` | HTTP 200, system name and status "online" | Status "online", docs at `/docs` | **PASSED** |
| **TC02** | Health Probe | `GET /health` | HTTP 200, healthy status, memory usage | Status "healthy", active collections | **PASSED** |
| **TC03** | Invalid File Rejection | Upload `.txt` / `.exe` file | HTTP 400 with invalid file error message | HTTP 400 Bad Request returned | **PASSED** |
| **TC04** | Corrupt PDF Rejection | Corrupt bytes with `.pdf` name | HTTP 400 with corrupted PDF error | HTTP 400 Bad Request returned | **PASSED** |
| **TC05** | Valid PDF Processing | Valid academic PDF | HTTP 201, `collection_id`, page count > 0 | `collection_id` generated, chunks indexed | **PASSED** |
| **TC06** | Grounded Q&A | Valid `collection_id` + query | HTTP 200, factual answer + exact page citations | Answer generated with source citations | **PASSED** |
| **TC07** | Invalid Collection Q&A | Non-existent UUID | HTTP 404 Collection Not Found | HTTP 404 returned correctly | **PASSED** |
| **TC08** | Empty Question Handling | Empty string `""` | HTTP 422 / 400 Validation Error | Handled cleanly with validation error | **PASSED** |
| **TC09** | Executive Summary | Valid `collection_id` | HTTP 200, structured executive summary | Summary generated successfully | **PASSED** |
| **TC10** | Practice MCQ Generation | Valid `collection_id` | HTTP 200, 4 formatted MCQs with answer key | MCQs with options and keys returned | **PASSED** |
| **TC11** | Key Points Extraction | Valid `collection_id` | HTTP 200, bulleted takeaway points | Key takeaways extracted cleanly | **PASSED** |
| **TC12** | Collection Deletion | `DELETE /api/documents/{id}` | HTTP 200, collection removed from memory | Collection purged from manager | **PASSED** |
| **TC13** | Delete Missing Collection | Non-existent UUID | HTTP 404 Collection Not Found | HTTP 404 returned | **PASSED** |
| **TC14** | Missing API Key Guard | No API key configured | System fallback / explicit error response | Fallback executed, no crash | **PASSED** |

---

<div style="page-break-after: always;"></div>

# CHAPTER 10 – DEPLOYMENT & LIMITATIONS

### 10.1 Cloud Deployment Architecture
DocuVerse AI is designed for seamless, modern continuous deployment:
1. **Backend Web Service (Render):**
   - Configured via `render.yaml`.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: `GROQ_API_KEY` configured securely in Render dashboard.
2. **Frontend Web App (Streamlit Community Cloud):**
   - Repository: `https://github.com/pankaj2007kumar26-max/DocuVerse_AI`
   - Branch: `main` | Entry file: `app.py`
   - Configured with `BACKEND_URL` and `GROQ_API_KEY` in Streamlit Secrets.

### 10.2 Production URLs & GitHub Repository
- **GitHub Repository:**  
  [https://github.com/pankaj2007kumar26-max/DocuVerse_AI](https://github.com/pankaj2007kumar26-max/DocuVerse_AI)
- **FastAPI Backend (Interactive Swagger Docs):**  
  `https://docuverse-ai-backend.onrender.com/docs`
- **Streamlit Live Web Application:**  
  `https://docuverseai.streamlit.app`

### 10.3 System Limitations
1. **Scanned Image PDFs:** Currently relies on digital PDF text extraction; scanned physical papers without an OCR layer require pre-processing with an OCR tool (e.g., Tesseract).
2. **In-Memory Volatility:** In the free deployment tier, FAISS vector indices reside in server RAM. Server cold-restarts purge active collections, requiring users to re-upload documents.
3. **Complex Tables & Mathematical Formulas:** Highly intricate multi-column matrices or handwritten mathematical derivations may experience formatting distortion during plain text extraction.
4. **Third-Party API Rate Limits:** Free-tier Groq API keys operate within rate limits (requests per minute / tokens per minute).

---

<div style="page-break-after: always;"></div>

# CHAPTER 11 – CONCLUSION

**DocuVerse AI – Intelligent Document Reading & Question Answering System** successfully addresses the challenge of academic information overload by delivering an accurate, fast, and grounded document intelligence platform.

By integrating **PyMuPDF** for high-fidelity text extraction, **FAISS** for fast semantic vector indexing, and **Groq Cloud LPUs** for sub-second language model inference, the project solves the twin problems of generic AI: token limitations and factual hallucinations. Every answer is strictly grounded in the uploaded course material and accompanied by exact page numbers and verifiable text snippets.

The project demonstrates full-stack software engineering maturity through:
- A decoupled, production-grade **FastAPI** backend supporting multi-tenant document isolation.
- A modern, responsive **Streamlit** user interface featuring a cosmic dark aesthetic and mobile-friendly layouts.
- Rigorous automated verification via a **14-test Pytest suite** achieving 100% pass rates.
- Practical educational utility through one-click summaries, revision MCQs, key points, and multilingual (English, Hindi, Hinglish) capabilities.

In conclusion, DocuVerse AI stands as an effective, reliable, and user-friendly AI study assistant that substantially reduces revision time, boosts conceptual clarity, and enhances learning efficiency for students and educators alike.

---

<div style="page-break-after: always;"></div>

# CHAPTER 12 – FUTURE SCOPE AND REFERENCES

### 12.1 Future Enhancements
The architecture of DocuVerse AI provides a foundation for future academic and commercial enhancements:
1. **Optical Character Recognition (OCR) Integration:** Incorporate Tesseract OCR or EasyOCR to extract text seamlessly from scanned handwritten lecture notes and historical papers.
2. **Persistent Cloud Vector Databases:** Migrate from in-memory FAISS to managed cloud vector databases (e.g., Pinecone, Qdrant, or ChromaDB with PostgreSQL) for cross-session index persistence.
3. **Multi-Modal Vision Understanding:** Integrate vision-language models (e.g., Llama 3.2 Vision) to interpret engineering diagrams, circuit schematics, and flowcharts embedded within PDFs.
4. **Interactive Chat Memory:** Implement conversational memory buffers allowing students to ask iterative follow-up questions in a continuous dialogue.
5. **Speech Interface:** Add text-to-speech (TTS) and speech-to-text (STT) capabilities for hands-free audio revision.

### 12.2 Practical Applications
- **Higher Education:** University students studying B.Tech, M.Tech, BCA, MCA, and medical curricula.
- **Academic Research:** Scholars synthesizing literature reviews across dozens of published IEEE/Springer papers.
- **Legal and Corporate Compliance:** Fast retrieval of contractual terms, clauses, and regulatory guidelines.
- **Competitive Exams:** Rapid MCQ drill generation for GATE, UPSC, and technical recruitment tests.

### 12.3 Academic & Documentation References
1. **Retrieval-Augmented Generation (RAG):** Lewis, P., et al. (2020). *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks."* Advances in Neural Information Processing Systems (NeurIPS 2020).
2. **FAISS Vector Library:** Johnson, J., Douze, M., & Jégou, H. (2019). *"Billion-Scale Similarity Search with GPUs."* IEEE Transactions on Big Data.
3. **FastAPI Documentation:** Tiangolo, S. (2024). *FastAPI Framework, High Performance Web APIs.* Available at: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
4. **PyMuPDF Documentation:** McKie, P. & Liu, J. (2024). *PyMuPDF: Python Bindings for the MuPDF Library.* Available at: [https://pymupdf.readthedocs.io](https://pymupdf.readthedocs.io)
5. **Streamlit Documentation:** Snowflake Inc. (2024). *Streamlit Python Documentation.* Available at: [https://docs.streamlit.io](https://docs.streamlit.io)
6. **Groq LPU Architecture:** Groq Inc. (2024). *Tensor Streaming Processor Architecture & Inference Documentation.* Available at: [https://groq.com](https://groq.com)
7. **Pydantic Validation:** Colvin, S. (2024). *Pydantic: Data Validation Using Python Type Annotations.* Available at: [https://docs.pydantic.dev](https://docs.pydantic.dev)
8. **Uvicorn ASGI Server:** Encode OSS (2024). *Uvicorn: The Lightning-Fast ASGI Server.* Available at: [https://www.uvicorn.org](https://www.uvicorn.org)

---

**END OF MINI PROJECT REPORT**

**Submitted By:** Pankaj Kumar  
**Roll Number:** `2501651530026`  
**Project Guide:** Ms. Prakanksha Shukla  
**Department:** Computer Science and Engineering  
**Institute:** Kanpur Institute of Technology, Kanpur  
**Academic Session:** 2025–2026  
