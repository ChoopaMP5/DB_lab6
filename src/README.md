## Requirements

- Python 3,9+
- MySQL database 5.7
- pip

## Installation

1. Clone repo:
   ```bash
   git clone https://your-repo-url.git
   cd your-repo
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql
   ```

3. Set connection to MySQL in database.py:
   ```
   DATABASE_URL = "mysql+pymysql://root@localhost/pakyliak"

  
4. Create MySQL database:
   ```
   CREATE DATABASE your_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
  
5. Start server:
   ```
   python -m uvicorn main:app --reload
   ```

6.  Check your server `http://127.0.0.1:8000`
