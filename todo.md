# 🎯 AI-QA Engine Development Checklist / Entwicklungs-Checkliste

## Phase 1: Project Setup & Infrastructure / Projekt-Setup & Infrastruktur
- [x] 1.1. Create project folder structure (PowerShell)
- [x] 1.2. Initialize C# xUnit integration test project (`dotnet new xunit`)
- [x] 1.3. Create Python virtual environment (`venv`)
- [x] 1.4. Install dependencies (`pip install -r requirements.txt`)

## Phase 2: Python Backend & AI-QA REST API (FastAPI)
- [x] 2.1. Implement FastAPI REST API server (`src/ai_qa_engine/api/main.py`)
- [x] 2.2. Implement Model Drift and Catastrophic Forgetting evaluators
- [ ] 2.3. Run API locally (`uvicorn`) and verify with Swagger UI

## Phase 3: C# xUnit SDET Automation Suite
- [ ] 3.1. Add `RestSharp` & `Newtonsoft.Json` to C# project
- [ ] 3.2. Implement `AiQaApiClient.cs` for REST API testing
- [ ] 3.3. Implement Quality Gate integration tests (`QualityGateTests.cs`)
- [ ] 3.4. Execute `dotnet test` and verify green status

## Phase 4: Streamlit Management Dashboard
- [ ] 4.1. Implement interactive dashboard (`dashboard/app.py`)

## Phase 5: CI/CD Pipeline (GitHub Actions)
- [ ] 5.1. Configure `.github/workflows/python-tests.yml`
- [ ] 5.2. Configure `.github/workflows/csharp-tests.yml`

## Phase 6: Documentation & Final Polish
- [ ] 6.1. Add German/English technical glossary (`docs/glossary.md`)
- [ ] 6.2. Finalize `README.md` with architecture diagrams
