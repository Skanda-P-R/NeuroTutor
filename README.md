# 🧠 NeuroTutor

**NeuroTutor** is a Flask-based web application designed to help users enhance their debugging skills and understand Python code better through interactive challenges. The platform includes user authentication, code analysis, and automatic correction capabilities.

---

## 🚀 Features

- 🧾 **User Authentication** (Register/Login/Logout)
- 🛠️ **Code Debugging Challenges**
- 🧪 **Code Error Detection**
- 🔧 **Automatic Code Correction**
- 📊 **Progress Tracking** (questions debugged & codes corrected)

---

## 🖥️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, Jinja2 Templates  
- **Database:** MySQL (via `flask_mysqldb`)  
- **Security:** Password hashing with Werkzeug  
- **Debugging Engine:** Custom modules (`groq_api_debug`, `symbolic_debugger`)

---

## 📂 Project Structure

```
.
├── app.py                   # Main Flask app
├── templates/               # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── code.html
│   └── debug.html
├── static/                  # All the CSS and JS codes
│   ├── bg.svg
│   ├── style.css
│   └── script.js
├── groq_api_debug.py        # Challenge code generator & comparison logic
├── symbolic_debugger.py     # Code analysis and correction
├── groq_api.py              # Correct code generator based on Errors
```

---

## 🛠️ Setup Instructions
### 1. Clone the Repository
```
git clone https://github.com/yourusername/neurotutor.git
cd neurotutor
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Set Environment Variables
```
export sql_username=your_mysql_username
export sql_password=your_mysql_password
export groq_api=your_groq_api
```
### 4. Configure MySQL
```
CREATE DATABASE neuro_tutor_db;

USE neuro_tutor_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    questions_debugged INT DEFAULT 0,
    codes_corrected INT DEFAULT 0
);
```
### 5. Run the App
```
python app.py
```
Visit http://localhost:5000/ in your browser.

---

## ✅ API Endpoints

| Route                  | Method    | Description                          |
|------------------------|-----------|--------------------------------------|
| `/`                    | GET       | Home page (protected)                |
| `/login`               | GET/POST  | User login                           |
| `/register`            | GET/POST  | User registration                    |
| `/logout`              | GET       | Logout and clear session             |
| `/code-checker`        | GET       | Code checker interface               |
| `/debugger-challenge`  | GET       | Debugging challenge interface        |
| `/get_code`            | POST      | Get code based on difficulty         |
| `/check_solution`      | POST      | Submit and verify debugging solution |
| `/check_errors`        | POST      | Analyze code for errors              |
| `/correct_code`        | POST      | Get AI-corrected version of the code |

--- 

## 🙌 Contribution
Feel free to fork this repo and submit pull requests. For major changes, open an issue first to discuss your idea.

---

## 📃 License
This project is licensed under the MIT License. See the [LICENSE]() file for details.
