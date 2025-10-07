# 📌 Property Listing Platform

> A property listing platform where users can search, create, and favorite listings, connect with owners, and filter results to find the perfect place to buy or rent. 

---

## 🚀 Live Demo  
[View Project](https://property-listing-platform.up.railway.app/)

---

## ✨ Features  
- User authentication with secure registration and login for landlords and renters
- Advanced search and filter functionality to quickly find listings by price, location, beds, and baths
- Full CRUD functionality with the ability to create, edit, delete, and favorite listings

---

## 🛠️ Tech Stack  
- **Frontend:** Django Templates, Bootstrap
- **Backend:** Django, Python
- **Database:** SQLite
- **Hosting:** Railway  

---

## 📸 Screenshots  
![Screenshot 1](https://ethanstewart.dev/mockups/propertylistingplatform_mockup_dark.svg) 

---

## ⚡ Getting Started (Django)

Clone the repo:  
```bash
git clone https://github.com/estewart35/PropertyListingPlatform.git
cd PropertyListingPlatform
```

Create a `.env` file in the project root and add the required environment variables:
```bash
# .env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEVELOPMENT=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```
*(Refer to `.env.example` in the repo for variable names.)*

Install dependencies and run locally:
```bash
pip install -r requirements.txt
python manage.py runserver
```
