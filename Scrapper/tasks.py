# tasks.py
from celery import shared_task
from .models import Brand, Product
from .scraping import scrape_amazon_products

@shared_task
def scrape_products_for_brand(brand_id):
    brand = Brand.objects.get(id=brand_id)
    products_data = scrape_amazon_products(brand)

    for product_data in products_data:
        product, created = Product.objects.update_or_create(
            asin=product_data['asin'],
            defaults={
                'name': product_data['name'],
                'sku': product_data['sku'],
                'image_url': product_data['image_url'],
                'brand': brand
            }
        )


@shared_task
def scrape_products_for_all_brands():
    for brand in Brand.objects.all():
        scrape_products_for_brand.delay(brand.id)
