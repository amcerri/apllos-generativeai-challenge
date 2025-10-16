# Data Architecture: Data Management and Processing

This document describes the actual data architecture and data management systems implemented in the Apllos Assistant project.

## Data Architecture Overview

The Apllos Assistant uses a data architecture with the following components:

- **PostgreSQL Database**: Primary data storage with pgvector extension
- **Analytics Data**: Olist e-commerce dataset for analytics queries
- **Knowledge Data**: Document chunks with vector embeddings for RAG
- **Commerce Data**: Sample commercial documents for processing
- **Configuration**: YAML-based configuration files

## Data Sources

### 📊 Analytics Data
**Purpose**: Business analytics and metrics data from the Olist e-commerce dataset

#### Data Types
- **Orders**: Order information and transactions
- **Customers**: Customer profiles and demographics
- **Products**: Product catalog and categories
- **Sellers**: Seller information and performance
- **Reviews**: Customer reviews and ratings
- **Geolocation**: Geographic data for orders and customers

#### Data Format
- **CSV Files**: Raw data in CSV format
- **PostgreSQL Tables**: Structured data in relational format
- **Schema**: Defined in `data/samples/schema.sql`

#### Data Ingestion
- **Script**: `scripts/ingest_analytics.py`
- **Process**: Loads CSV files into PostgreSQL tables
- **Validation**: Data validation and type checking
- **Allowlist**: Generates `app/routing/allowlist.json` for SQL safety

### 📚 Knowledge Data
**Purpose**: Document knowledge base for RAG (Retrieval Augmented Generation)

#### Document Types
- **PDF Documents**: Business documents and e-books
- **Text Files**: Plain text documents
- **Content**: E-commerce guides, tutorials, and best practices

#### Data Processing
- **Text Extraction**: OCR and text extraction from PDFs
- **Chunking**: Document splitting into manageable chunks
- **Embeddings**: Vector embeddings using OpenAI embeddings
- **Storage**: Stored in `doc_chunks` table with pgvector

#### Data Ingestion
- **Script**: `scripts/ingest_vectors.py`
- **Process**: Processes documents in `data/docs/` folder
- **Embeddings**: Generates vector embeddings for semantic search
- **Index**: Creates IVFFLAT index for fast vector similarity search

### 💼 Commerce Data
**Purpose**: Sample commercial documents for testing and demonstration

#### Document Types
- **Invoices**: Sample invoice documents
- **Purchase Orders**: Sample purchase order documents
- **Receipts**: Sample receipt documents
- **Contracts**: Sample contract documents

#### Data Processing
- **Text Extraction**: Multi-format text extraction (PDF, DOCX, TXT)
- **OCR**: Optical Character Recognition for images
- **Structured Extraction**: LLM-based structured data extraction
- **Validation**: Data validation and consistency checks

## Data Storage

### 🗄️ PostgreSQL Database
**Purpose**: Primary data storage with pgvector extension

#### Database Schema
- **Analytics Tables**: Orders, customers, products, sellers, reviews, geolocation
- **Knowledge Tables**: `doc_chunks` table with vector embeddings
- **Configuration**: Database connection and settings

#### Vector Storage
- **Technology**: pgvector extension
- **Embeddings**: 1536-dimensional vectors (OpenAI embeddings)
- **Index**: IVFFLAT index for cosine similarity search
- **Performance**: Vector similarity queries

#### Data Safety
- **Allowlist**: SQL allowlist for safe query execution
- **Read-only**: Analytics queries are read-only
- **Timeouts**: Query timeouts and row limits
- **Validation**: SQL validation and safety checks

### 📁 File Storage
**Purpose**: Document and configuration file storage

#### Document Storage
- **Location**: `data/docs/` folder
- **Formats**: PDF, DOCX, TXT files
- **Processing**: OCR and text extraction
- **Metadata**: Document metadata and information

#### Configuration Storage
- **Location**: `app/config/` folder
- **Formats**: YAML configuration files
- **Settings**: Application settings and parameters
- **Models**: LLM model configurations

## Data Processing

### ⚡ Real-time Processing
**Purpose**: Process user queries in real-time

#### Query Processing
- **Routing**: LLM-based query routing
- **Supervision**: Deterministic guardrails and fallbacks
- **Agent Processing**: Specialized agent processing
- **Response Generation**: LLM-based response generation

#### Technologies
- **LangGraph**: Multi-agent orchestration
- **OpenAI API**: LLM processing and embeddings
- **PostgreSQL**: Database queries and vector search
- **FastAPI**: REST API for external access

### 🔄 Batch Processing
**Purpose**: Process data ingestion and preparation

#### Data Ingestion
- **Analytics**: Load Olist dataset into PostgreSQL
- **Vectors**: Process documents and generate embeddings
- **Allowlist**: Generate SQL allowlist from schema
- **Validation**: Data validation and quality checks

#### Technologies
- **Python Scripts**: Custom ingestion scripts
- **PostgreSQL**: Database operations
- **OpenAI API**: Embedding generation
- **File Processing**: Document text extraction

## Data Analytics

### 📊 Analytics Queries
**Purpose**: Natural language to SQL conversion for analytics

#### Query Processing
- **Planner**: Converts natural language to SQL
- **Executor**: Safely executes SQL queries
- **Normalizer**: Formats results in Portuguese
- **Safety**: Allowlist validation and read-only execution

#### Analytics Capabilities
- **Sales Analysis**: Revenue, orders, and performance metrics
- **Customer Analysis**: Customer behavior and demographics
- **Product Analysis**: Product performance and categories
- **Geographic Analysis**: Location-based insights
- **Time Series**: Temporal analysis and trends

### 🔍 Knowledge Search
**Purpose**: Semantic search over document knowledge base

#### Search Processing
- **Retrieval**: Vector similarity search
- **Ranking**: Result ranking and filtering
- **Answering**: LLM-based answer generation
- **Citations**: Source citation and validation

#### Search Capabilities
- **Semantic Search**: Meaning-based search
- **Document Retrieval**: Relevant document chunks
- **Answer Generation**: Comprehensive answers in Portuguese
- **Source Attribution**: Document citations and references

## Data Security

### 🔒 Data Protection
**Purpose**: Ensure data security and privacy

#### Security Measures
- **SQL Safety**: Allowlist-based SQL validation
- **Read-only**: Analytics queries are read-only
- **Timeouts**: Query timeouts and resource limits
- **Validation**: Input validation and sanitization

#### Access Control
- **Database Access**: Controlled database access
- **API Security**: API key authentication
- **CORS**: Configurable CORS settings
- **Rate Limiting**: Request rate limiting

## Data Governance

### 📋 Data Quality
**Purpose**: Ensure data quality and consistency

#### Quality Measures
- **Data Validation**: Input data validation
- **Schema Validation**: Database schema validation
- **Allowlist Validation**: SQL allowlist validation
- **Error Handling**: Comprehensive error handling

#### Monitoring
- **Logging**: Structured logging with context
- **Metrics**: Performance and usage metrics
- **Health Checks**: System health monitoring
- **Tracing**: Distributed tracing for debugging

## Best Practices

### 📋 Data Architecture Best Practices
**Purpose**: Guidelines for effective data architecture

#### Design Principles
- **Simplicity**: Keep architecture simple and maintainable
- **Safety**: Prioritize data safety and security
- **Performance**: Optimize for query performance
- **Reliability**: Ensure system reliability
- **Scalability**: Design for future growth

#### Implementation Guidelines
- **Data Modeling**: Effective data modeling
- **Data Integration**: Seamless data integration
- **Data Processing**: Efficient data processing
- **Data Storage**: Optimal data storage
- **Data Analytics**: Effective data analytics

This data architecture guide provides a complete framework for understanding the data management and processing systems in the Apllos Assistant project.

---

**← [Back to Documentation Index](../README.md)**