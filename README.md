# Balancing Efficiency and Relevance: A Solr-Based Hybrid Search Architecture 🎬

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Solr](https://img.shields.io/badge/Apache_Solr-9.0-red.svg)](https://solr.apache.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

This repository contains a complete **Advanced Information Retrieval (IR)** system for movie metadata. The project implements a hybrid architecture that combines the speed of **Apache Solr** (Lexical Search) with the deep understanding of **Sentence-BERT** (Semantic Re-ranking).

## Project Overview
Traditional lexical search (BM25) often fails due to the "vocabulary gap" (e.g., searching for "hero journey" might not return movies that don't explicitly use those words). This system solves this by:
1.  **Fast Candidate Generation**: Using Solr's inverted index to fetch the top 200 candidates.
2.  **Semantic Re-ranking**: Using SBERT (`all-MiniLM-L6-v2`) and FAISS to re-rank candidates based on conceptual similarity.
3.  **Automated Evaluation**: Generating synthetic ground truth using **KeyBERT** for large-scale performance benchmarking.

## System Architecture
The system follows a three-layer design:
- **Ingestion Layer**: Python-based pipeline cleaning and batch-uploading 27,000+ movie records to Solr.
- **Retrieval Layer**: Dual-stage retrieval (Lexical via Solr DisMax + Semantic via SBERT).
- **Presentation Layer**: An interactive **Streamlit** dashboard supporting fielded search, proximity matching, and dynamic filtering.

## Key Features
-   **Hybrid Retrieval**: Combines BM25 scores with Cosine Similarity.
-   **Advanced Querying**: Supports title boosting (`^5`), proximity search (`~5`), and faceted filtering.
-   **Semantic Understanding**: Bridges the vocabulary gap for abstract queries like "coming of age" or "survival story".
-   **Automated Evaluation**: Precision@k and Recall@k metrics calculated against a KeyBERT-generated ground truth.

## Experimental Results
Our hybrid approach demonstrated significant improvements over baseline Solr:
| Query | Baseline P@5 | Hybrid P@5 |
| :--- | :---: | :---: |
| "love story" | 0.8 | **1.00** |
| "alien invasion" | 0.60 | **1.00** |
| "psych. thriller" | 0.6 | **0.80** |

## Technology Stack
-   **Core Engine**: Apache Solr
-   **Backend**: Python (PySolr)
-   **NLP Models**: Sentence-Transformers (SBERT), KeyBERT
-   **Vector Search**: FAISS
-   **Frontend**: Streamlit
-   **Deployment**: Docker & Docker Compose

##  Installation & Setup

### Prerequisites
- Docker & Docker Compose installed.

### Execution
1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Movie-Hybrid-Search-Solr.git
   cd Movie-Hybrid-Search-Solr
   
### Run with Docker:
2.
   ```bash
   docker-compose up --build

## 👥 Authors
- **Mina Eskander**<sup>†</sup> (minaeskander291@gmail.com)
- **Hagar Selim**<sup>†</sup> (Hagargalal36@gmail.com)
- **Hadeer Elkady**<sup>†</sup> (hadeeralkady606@gmail.com)

*<sup>†</sup> These authors contributed equally to this work.*

**Institution:** Arab Academy for Science, Technology and Maritime Transport (AASTMT), Egypt.
