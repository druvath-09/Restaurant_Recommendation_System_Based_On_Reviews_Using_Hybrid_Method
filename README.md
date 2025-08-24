# 🍽️ Restaurant Recommendation System (Hybrid Method)

A hybrid recommendation system that suggests restaurants based on user reviews and other factors, combining **content-based filtering** and **collaborative filtering**.  
Built with **Django**, **SQLite**, and **Machine Learning models**.

---

## 📌 Overview
This project is designed to provide personalized restaurant recommendations using a hybrid approach:
- **Content-Based Filtering** → based on restaurant attributes like cuisine, price, and location.  
- **Collaborative Filtering** → based on user reviews and preferences.  

The system features a Django web application with a user-facing interface and an admin dashboard.

---

## ✨ Features
✅ Personalized restaurant recommendations  
✅ User review analysis and visualization  
✅ Admin dashboard for managing data  
✅ SQL database for persistence (`db.sqlite3`)  
✅ Interactive frontend using HTML, CSS, and JavaScript  

---

## 🏗️ Architecture & Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite  
- **Machine Learning:** Custom recommendation models (inside `Model/`)  

---

## ⚙️ Installation & Setup

Clone the repository:
```bash
git clone https://github.com/druvath-09/Restaurant_Recommendation_System_Based_On_Reviews_Using_Hybrid_Method.git
cd Restaurant_Recommendation_System_Based_On_Reviews_Using_Hybrid_Method/SOURCE CODE/RestaurantRecommendation
```

# Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

##Install dependencies:
```bash
pip install -r requirements.txt
```

##Run migrations and start server:
```bash
python manage.py migrate
python manage.py runserver
```

Visit 👉 http://127.0.0.1:8000/ in your browser.

📂 Project Structure:
```pgsql
Restaurant_Recommendation_System_Based_On_Reviews_Using_Hybrid_Method/
│
├── DATABASE/
│   └── DB.sql
│
├── SOURCE CODE/RestaurantRecommendation/
│   ├── AdminApp/         
│   ├── Datasets/         
│   ├── Model/            
│   ├── RestaurantRecommendation/  
│   ├── Static/           
│   ├── Templates/        
│   ├── db.sqlite3        
│   ├── manage.py         
│   └── reviews_table.html
│
└── Restaurant Recommendation.docx
```

🤝 Contributing

Contributions are welcome! 🎉
Feel free to fork this repo, raise issues, or create pull requests.

📜 License
```yaml
This project is licensed under the MIT License.

```
