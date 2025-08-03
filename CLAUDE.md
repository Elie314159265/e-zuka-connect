# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend (Next.js)
```bash
cd frontend
npm run dev        # Start development server on localhost:3000
npm run build      # Build production bundle
npm run start      # Start production server
npm run lint       # Run ESLint
```

### Backend Services
```bash
# Core API (FastAPI)
cd services/core-api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# OCR Processor (FastAPI)
cd services/ocr-processor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Deployment
```bash
./scripts/deploy.sh  # Deploy to Kubernetes using kubectl
```

## Architecture Overview

### Project Structure
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and Framer Motion
- **Backend**: Microservices architecture with FastAPI
  - `core-api`: Main API service with user auth, receipts, weather data
  - `ocr-processor`: Google Document AI integration for receipt processing
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Deployment**: Kubernetes with Docker containers

### Core Services

#### Core API (`services/core-api/`)
- **Framework**: FastAPI with SQLAlchemy
- **Authentication**: JWT tokens with passlib/bcrypt
- **Database Models**: Users, Receipts, ReceiptItems, WeatherData
- **API Routes**: `/api/auth`, `/api/users`, `/api/receipts`, `/api/weather`, `/api/analysis`, `/api/debug`
- **CORS**: Configured for production domain and localhost development

#### OCR Processor (`services/ocr-processor/`)
- **Purpose**: Receipt text extraction using Google Document AI
- **Input**: GCS URIs pointing to receipt images
- **Output**: Structured data (supplier_name, total_amount, line_items)
- **Dependencies**: Google Cloud Document AI and Storage clients

#### Frontend (`frontend/`)
- **Framework**: Next.js 14 with App Router
- **UI Components**: Custom components with Framer Motion animations
- **State Management**: Zustand store for authentication
- **Styling**: Tailwind CSS with custom animations
- **Key Pages**: Home, Login/Register (User/Owner), Dashboard, Receipt Upload

### Database Schema
- **Users**: email, hashed_password, full_name, age_group, gender, is_owner
- **Receipts**: user_id, supplier_name, total_amount, receipt_date
- **ReceiptItems**: receipt_id, description, amount
- **WeatherData**: date, temperature, humidity, weather_code

### API Integration
- Frontend communicates with core-api on `/api/*` routes
- Core-api calls ocr-processor for receipt processing
- Google Cloud services integration for document processing and storage

### Development Notes
- TypeScript strict mode is disabled in frontend tsconfig
- No existing test framework detected - check with user before implementing tests
- Environment variables needed for GCP integration (PROJECT_ID, PROCESSOR_ID)
- Kubernetes deployment configured with base and production overlays