# FastAPI Project

This is a FastAPI project.

## Installation
### 1. Clone the Repository

```bash
git clone https://github.com/abinet1/lucid-pro.git
cd lucid-pro
```

### 2. verify if python is installed and setup vertual env

```bash
python --version

python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies and Set Environment Variables
```bash
pip install -r requirements.txt

```

#### Create a .env file in the root directory of the project and add the following environment variables

```bash
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
DB_NAME=your_db_name
```

### 4. Run the Application

```bash
fastapi run dev
```