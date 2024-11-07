
# Amazon Brand Product Scraper

  

This Django project is a web scraping system integrated with Celery to automate scraping of all products from a specific Amazon brand. The project updates the product list four times a day, storing key information such as product name, ASIN, SKU, and image URL. The project provides a REST API for retrieving and filtering products by brand.

  

## Features

  

-  **Django Admin**: Define and manage Amazon brands. Admins can view and manage products for each brand.

-  **Web Scraping**: Periodic scraping to retrieve product details from Amazon, with anti-scraping measures (e.g., user-agent rotation).

-  **Periodic Task Scheduling with Celery**: Scheduled scraping tasks run four times a day to keep product data up-to-date.

-  **REST API**: Retrieve and filter products by brand via a Django REST Framework API.

  

## Table of Contents

  

1. [Installation](#installation)

2. [Configuration](#configuration)

3. [Usage](#usage)

4. [API Documentation](#api-documentation)

  
---

  

## Installation

  

### 1. Clone the Repository

  

```bash

git clone  <your-repository-url>

cd your-project-directory

```

  

### 2. Install Dependencies

  

Ensure you have Python 3.8+ and pip installed. Then, install the required packages:

  

```bash

pip install  -r  requirements.txt

```

  

### 3. Set Up Redis (for Celery)

  

This project uses Redis as the Celery broker. Install Redis locally or use a hosted Redis instance.

  

### 4. Configure Environment Variables

  

Create a `.env` file in the project root and add the following configurations:

  

```plaintext

SECRET_KEY=your_django_secret_key

CELERY_BROKER_URL=redis://localhost:6379/0

CELERY_RESULT_BACKEND=redis://localhost:6379/0

```

  

### 5. Apply Migrations

  

Run migrations to set up the database schema:

  

```bash

python manage.py  migrate

```

  

### 6. Create a Superuser

  

```bash

python manage.py  createsuperuser

```

  

### 7. Start Django and Celery

  

In separate terminal windows, run:

  

```bash

# Start the Django server

python manage.py  runserver

  

# Start the Celery worker

celery -A  your_project_name  worker  -l  info

  

# Start the Celery beat scheduler

celery -A  your_project_name  beat  -l  info

```

  

---

  

## Configuration

  

This project uses **Django Celery Beat** to manage periodic scraping tasks for each brand, scheduled to run four times a day. Configure task scheduling in the Django Admin under "Periodic Tasks."

  

### Setting Up Periodic Tasks

  

To configure tasks to scrape products for all brands, create a periodic task in Django Admin:

  

1. Go to **Django Admin** > **Periodic Tasks**.

2. Create a new periodic task with the following configuration:

-  **Name**: Scrape Amazon Products for All Brands

-  **Task**: `Scrapper.tasks.scrape_products_for_all_brands`

-  **Interval**: Choose an interval (e.g., every 6 hours to run 4 times a day).

  

---

  

## Usage

  

### Adding Brands and Products

  

1.  **Add a Brand**: In Django Admin, create a brand entry with the desired brand name.

2.  **View Products**: The system will automatically scrape and list products under each brand entry, updating the list four times daily.

  

To trigger the scraper manually using the management command we created earlier in `create_periodic_tasks`, you can include the following steps in the **Running Scraper Manually** section of the `README.md`:

---

### Running Scraper With Command

To set up the periodic tasks for scraping (if not already configured) or to trigger the scraping process, you can use the custom Django management command I have created:

```bash
python manage.py create_periodic_tasks
```

This command sets up the periodic tasks to run four times a day and initiates the scraping process for all brands in the database. Running this command is useful if you need to ensure the periodic tasks are configured or if you want to trigger an immediate scrape without waiting for the next scheduled run.



### Running Scraper Manually (Optional)

  

To trigger a manual scrape, you can call the `scrape_products_for_all_brands` Celery task.

  

```python

from Scrapper.tasks import scrape_products_for_all_brands

scrape_products_for_all_brands.delay()

```

  

---

  

## API Documentation

  

The project exposes a REST API to list products by brand with support for filtering. Here’s how to use it:

  

### Get Products by Brand

  

**Endpoint**: `/products/<brand_name>/`

  

**Method**: `GET`

  

**Query Parameters**:

-  `asin`: Filter by ASIN

-  `sku`: Filter by SKU

-  `name`: Filter by product name

-  `search`: Full-text search by product name

-  `ordering`: Order by fields (e.g., `name`, `asin`, `sku`)

  

**Example Requests**:

```bash

# Get all products by brand "ExampleBrand"

GET /scrapper/products/ExampleBrand/

  

# Filter products by ASIN

GET /scrapper/products/ExampleBrand/?asin=B08T5QVX5B

  

# Search products by name

GET /scrapper/products/ExampleBrand/?search=phone

  

# Order products by name

GET /scrapper/products/ExampleBrand/?ordering=name

```  


---

  
