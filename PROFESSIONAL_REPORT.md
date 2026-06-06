# PROFESSIONAL PROJECT REPORT

## Financial Data Warehouse for Acme Ltd

---

### Document Information

| **Field** | **Details** |
|-----------|--------------|
| Project Title | Financial Data Warehouse for Acme Ltd |
| Student Name | Haris Mustafa |
| Student Email | haris.mustafa10@e-uvt.ro |
| Submission Date | June 6, 2026 |
| Course | Data Warehouses |
| Institution | Universitatea de Vest din Timișoara |
| GitHub Repository | https://github.com/raoharis507/financial-data-warehouse |

---

### Table of Contents

1. Executive Summary
2. Introduction
3. Technology Stack
4. System Architecture
5. Database Design
6. Temporal Data Warehouse Pattern
7. Functional Requirements (UC1-UC4)
8. REST API Endpoints (Q1-Q5)
9. Analytics & Forecasting (UC3)
10. LLM Assistant with MCP (UC4)
11. User Interfaces
12. Testing & Validation
13. Installation Guide
14. Conclusion
15. References

---

## 1. EXECUTIVE SUMMARY

This report documents the complete implementation of a Financial Data Warehouse for Acme Ltd. The system successfully meets all project requirements.

### 1.1 Key Achievements

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| NoSQL Database | ✅ | MongoDB 8.0 |
| Temporal DWH | ✅ | Append-only pattern |
| Multi-Provider Support | ✅ | Nasdaq & Bloomberg |
| Data Ingestion (UC1) | ✅ | POST /api/ingest |
| REST API (UC2) | ✅ | Q1-Q5 endpoints |
| Analytics (UC3) | ✅ | MA, Forecast, Volatility |
| LLM Assistant (UC4) | ✅ | MCP with 4 tools |
| Unit Tests | ✅ | 8 tests passing |
| Demo Video | ✅ | 3 minutes |

### 1.2 Architecture Overview

The system follows a three-tier architecture:

- **Client Layer**: Browser, cURL, API clients, LLM Assistant
- **Application Layer**: FastAPI server with REST endpoints and services
- **Data Layer**: MongoDB with assets, timeseries, datasources collections



## 2. INTRODUCTION

### 2.1 Problem Statement

Acme Ltd needs a data warehouse platform that can:

| # | Requirement | Description |
|---|-------------|-------------|
| 1 | Data Collection | Collect financial market data from multiple vendors |
| 2 | Temporal Storage | Never overwrite data, track complete history |
| 3 | Heterogeneous Data | Support stocks and crypto with different attributes |
| 4 | REST API | Provide 5 specific queries for data access |
| 5 | Analytics | Generate insights, forecasts, and risk assessments |
| 6 | LLM Assistant | Natural language interface with MCP tools |

### 2.2 Project Objectives Status

| Objective | Status | Completion Date |
|-----------|--------|-----------------|
| Design NoSQL database schema | ✅ | June 1, 2026 |
| Implement temporal pattern | ✅ | June 2, 2026 |
| Build ingestion pipeline | ✅ | June 3, 2026 |
| Create REST API (Q1-Q5) | ✅ | June 3, 2026 |
| Develop analytics modules | ✅ | June 4, 2026 |
| Integrate LLM assistant | ✅ | June 5, 2026 |
| Create professional UI | ✅ | June 5, 2026 |
| Write unit tests | ✅ | June 6, 2026 |


## 3. TECHNOLOGY STACK

### 3.1 Technologies Used

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Database** | MongoDB | 8.0 | NoSQL temporal storage |
| **Backend** | FastAPI | 0.136.1 | RESTful API framework |
| **Server** | Uvicorn | 0.47.0 | ASGI server |
| **Data Analysis** | Pandas | 3.0.3 | Data manipulation |
| **Numerical Computing** | NumPy | 2.4.5 | Mathematical operations |
| **Machine Learning** | Scikit-learn | 1.8.0 | Linear regression |
| **Validation** | Pydantic | 2.13.4 | Data validation |
| **Language** | Python | 3.14 | Core implementation |

### 3.2 Architecture Diagram

┌─────────────────────────────────────────────────────────────────┐
│ CLIENTS │
│ Browser │ cURL │ Python Client │ API Tests │ LLM Assistant │
└─────────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ FASTAPI SERVER (:8000) │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│ │ REST API │ │ Services │ │ Models │ │
│ │ (Q1-Q5) │ │ - Ingestion │ │ - Asset │ │
│ │ (UC1-UC4) │ │ - Analytics │ │ - TimeSeries │ │
│ │ │ │ - LLM │ │ - DataSource │ │
│ └──────────────┘ └──────────────┘ └──────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────┐
│ MONGODB DATABASE │
│ (financial_dwh) │
│ ┌────────────┐ ┌──────────────┐ ┌────────────────────────────┐ │
│ │ assets │ │ timeseries │ │ datasources │ │
│ │ (stocks, │ │ (prices, │ │ (Nasdaq, Bloomberg) │ │
│ │ crypto) │ │ volumes) │ │ │ │
│ └────────────┘ └──────────────┘ └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

## 3. TECHNOLOGY STACK

### 3.1 Technologies Used

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Database | MongoDB | 8.0 | NoSQL temporal storage |
| Backend | FastAPI | 0.136.1 | RESTful API framework |
| Server | Uvicorn | 0.47.0 | ASGI server |
| Data Analysis | Pandas | 3.0.3 | Data manipulation |
| Numerical Computing | NumPy | 2.4.5 | Mathematical operations |
| Machine Learning | Scikit-learn | 1.8.0 | Linear regression |
| Validation | Pydantic | 2.13.4 | Data validation |
| Language | Python | 3.14 | Core implementation |

### 3.2 System Architecture

The system follows a three-tier architecture:

**Client Layer:** Browser, cURL, Python Client, API Tests, LLM Assistant

**Application Layer:** FastAPI Server on port 8000 with REST API endpoints, Services (Ingestion, Analytics, LLM), and Data Models

**Database Layer:** MongoDB with three collections: assets, timeseries, datasources

### 3.3 Request Flow

1. Client sends HTTP request to FastAPI endpoint
2. FastAPI validates request using Pydantic models
3. Service layer processes business logic
4. MongoDB performs database operations
5. Response returned to client as JSON


## 4. DATABASE DESIGN

### 4.1 Collection: assets

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| assetId | String | Unique identifier | "AAPL" |
| symbol | String | Trading symbol | "AAPL" |
| name | String | Full name | "Apple Inc." |
| assetClass | String | Type of asset | "stock" |
| region | String | Geographic origin | "US" |
| provider | String | Data source | "Nasdaq" |
| validFrom | DateTime | Start date | "2026-06-01" |
| validTo | DateTime | End date (null if current) | null |
| isDeleted | Boolean | Soft delete flag | false |
| metadata | Object | Flexible attributes | {"sector":"Tech"} |

### 4.2 Collection: timeseries (Temporal)

| Field | Type | Description |
|-------|------|-------------|
| dataPointId | String | UUID unique identifier |
| assetId | String | Reference to asset |
| provider | String | Data source |
| timestamp | DateTime | Price recording time |
| openPrice | Float | Opening price |
| highPrice | Float | Highest price |
| lowPrice | Float | Lowest price |
| closePrice | Float | Closing price |
| volume | Float | Trading volume |
| source | String | API source |
| ingestedAt | DateTime | Ingestion time |

### 4.3 Collection: datasources

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| sourceId | String | Unique ID | "nasdaq_v1" |
| name | String | Provider name | "Nasdaq Data Link" |
| baseUrl | String | API endpoint | "https://data.nasdaq.com" |
| apiType | String | Protocol | "REST" |
| authRequired | Boolean | Authentication needed | true |
| supportedAssets | Array | Available assets | ["AAPL","MSFT"] |


## 5. TEMPORAL DATA WAREHOUSE PATTERN

### 5.1 Definition

A temporal data warehouse preserves complete history by never overwriting or deleting data. Every change adds a new record with a timestamp.

### 5.2 Implementation Comparison

| Operation | Traditional Database | This Project (Temporal) |
|-----------|---------------------|-------------------------|
| INSERT | Add single record | Add record with validFrom = now |
| UPDATE | Overwrite existing record | Add NEW record, old validTo = now |
| DELETE | Remove record | Set isDeleted = true, validTo = now |
| Query Current | Read single record | Read WHERE validTo IS NULL |
| Query Historical | Not possible | Read all records with timestamps |

### 5.3 Proof of Temporal Pattern

**API Call:**
```bash
curl "http://127.0.0.1:8000/api/timeseries/AAPL/Nasdaq"

## 6. FUNCTIONAL REQUIREMENTS (UC1-UC4)

### 6.1 UC1: Data Ingestion

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/ingest/{assetId}/{provider} | Ingest new data from provider |
| GET | /api/provenance/{assetId}/{provider} | Get data provenance |

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/api/ingest/AAPL/Nasdaq"

## 7. ANALYTICS & FORECASTING (UC3)

### 7.1 Moving Average (5-day)

**Formula:** MA5 = (P1 + P2 + P3 + P4 + P5) / 5

**Example for AAPL:**

| Day | Close Price |
|-----|-------------|
| Day 1 | $150.00 |
| Day 2 | $152.00 |
| Day 3 | $154.00 |
| Day 4 | $153.00 |
| Day 5 | $156.00 |

**Result:** MA5 = (150 + 152 + 154 + 153 + 156) / 5 = $153.00

### 7.2 Price Forecast (Linear Regression)

**Method:** Ordinary Least Squares Linear Regression

**Model:** Price = a + (b x Time)

| Parameter | Description |
|-----------|-------------|
| a (Intercept) | Base price |
| b (Slope) | Daily change (b>0 = Up trend, b<0 = Down trend) |

**Example Forecast for AAPL:**

| Day | Predicted Price |
|-----|-----------------|
| Day 1 (tomorrow) | $155.69 |
| Day 2 | $155.90 |
| Day 3 | $156.12 |

**Trend:** Upward

### 7.3 Volatility and Risk Assessment

**Formula:**
- Daily Return = (Price_t - Price_t-1) / Price_t-1
- Volatility = Standard Deviation(Daily Returns) x sqrt(252)

**Risk Classification:**

| Volatility Range | Risk Level |
|-----------------|------------|
| Less than 15% | Low |
| 15% to 30% | Medium |
| Greater than 30% | High |

**Example for AAPL:**
- Volatility: 30.99% → High Risk
- Price Range: $150 - $159

### 7.4 Analytics Results Summary

| Asset | Moving Average | Forecast Day 1 | Volatility | Risk Level |
|-------|---------------|----------------|------------|-------------|
| AAPL | $153.00 | $155.69 | 30.99% | High |
| MSFT | $284.00 | $286.50 | 0.09% | Low |
| BTC | $50,000 | $50,500 | 45.00% | High |


## 8. LLM ASSISTANT WITH MCP INTEGRATION (UC4)

### 8.1 What is MCP?

MCP (Model Context Protocol) is a pattern where an LLM calls external tools to access data. The LLM decides which tool to use based on natural language input.

### 8.2 MCP Tools Implemented

| Tool Name | Trigger Keywords | Function |
|-----------|-----------------|----------|
| list_assets | "list", "show assets" | Returns all assets |
| fetch_timeseries | "time series", "prices" | Returns price history |
| summarize_trends | "trend", "summarize" | Returns moving averages |
| compare_assets | "compare", "versus" | Compares two assets |

### 8.3 Example Interactions

**List Assets:**
```bash
curl "http://127.0.0.1:8000/api/assistant/ask?query=list%20assets"

## 9. TESTING AND VALIDATION

### 9.1 Unit Tests

| Test | Endpoint | Status |
|------|----------|--------|
| test_health | GET /health | PASSED |
| test_q1_list_assets | GET /api/assets | PASSED |
| test_q2_asset_details | GET /api/assets/AAPL | PASSED |
| test_q3_list_sources | GET /api/sources | PASSED |
| test_q5_timeseries | GET /api/timeseries/AAPL/Nasdaq | PASSED |
| test_analytics_moving_average | GET /api/analytics/ma/AAPL/Nasdaq | PASSED |
| test_analytics_forecast | GET /api/analytics/forecast/AAPL/Nasdaq | PASSED |
| test_llm_assistant | GET /api/assistant/ask | PASSED |

### 9.2 Run Tests

```bash
python3 test_app.py

## 10. INSTALLATION GUIDE

### Prerequisites

```bash
brew install mongodb-community@8.0
brew services start mongodb-community@8.0
