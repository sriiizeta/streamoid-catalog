Streamoid Catalog is a backend service built with FastAPI for managing product data, providing a robust API for CRUD operations and database interactions.

Features are:

1.RESTful API endpoints for product management
2.PostgreSQL database integration via SQLModel
3.Environment-based configuration
4.Async support for high performance
5.Easy local development and deployment

Requirements are:

1.Python 3.11+
2.PostgreSQL
3.pip packages: see requirements.txt
4.Installation

Clone the repository:

git clone <repo-url>
cd streamoid-catalog


Create a virtual environment:
python -m venv venv


Activate the environment:
Windows (PowerShell):
.\venv\Scripts\activate


Linux/Mac:
source venv/bin/activate


Install dependencies:
pip install -r requirements.txt


Setup .env with your database credentials.
Run Locally
uvicorn app.main:app --reload


Access the API at: http://127.0.0.1:8000