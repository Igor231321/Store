# Django E-commerce Store 🛒
Online store built with Django featuring cart, payments, and delivery.
---


## ✨ Features

- 📂 **Catalog** – brands, categories (tree structure with **MPTT**), product variations (size, color, SKU, stock).  
- 📥 **Bulk import** – upload products, attributes, variations, and characteristics from Excel.  
- ⚡ **Performance** – optimized queries with `select_related`, `prefetch_related`, indexes, caching.  
- 💾 **Cache** – File-based caching for product pages and queries.  
- 💳 **Payments** – integration with **WayForPay API** (signature validation, secure callbacks).  
- 🚚 **Delivery methods** – Nova Poshta, Ukrposhta, Meest (cities & warehouses stored in DB).  
- 🛒 **Cart & Orders** – persistent carts (per user/session), order statuses, discounts, stock tracking.  
- ⭐ **Reviews** – ratings, comments, pros & cons.  
- 🔔 **Stock notifications** – users can subscribe for "back in stock" alerts.  
- 🌐 **Multilanguage** – Ukrainian / Russian support on model level.  
- 🔧 **Custom Admin Panel** – styled with **django-unfold** (modern UI/UX).  
- 📡 **REST API (DRF)** – endpoints for categories, products, variations with nested serializers.  
- 🎨 **CMS elements** – static pages, homepage sliders, banners.  

---

## 🛠️ Tech Stack
- Python 3.12, Django 5
- PostgreSQL
- TailwindCSS + Flowbite (UI)
- Docker & Docker Compose

---

## 🚀 How to Run

1. Clone the project from GitHub:
```bash
git clone https://github.com/Igor231321/Store.git
cd Store
```

2. Build and start containers:
```bash
docker compose up --build
```

3. Entrypoint script will:

- Wait for PostgreSQL
- Run migrations
- Load fixtures (fixtures/products/all.json)
- Collect static files
- Start Django server

4. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

Enter your email and password when prompted.

---

## 🎉 Done!

Open in browser: http://127.0.0.1:8000

Admin panel: http://127.0.0.1:8000/admin/

---

## Author
Ihor Chernobai  
[Telegram](https://t.me/igor_chernoaby) | [Email](mailto:chernobay.i2112@gmail.com)