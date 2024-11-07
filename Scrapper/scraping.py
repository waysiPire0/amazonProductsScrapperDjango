# scraping.py
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers



def get_fake_header():
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
    return header.generate()


def get_all_pages(name,id_):
  headers = get_fake_header()
  url = f"https://www.amazon.com/stores/{name}/page/{id_}?ref_=ast_bln"
  resp = requests.get(url, headers=headers)
  soup=BeautifulSoup(resp.text,'html.parser')
  all_as = soup.findAll('a', {'data-click-type': ''})
  links = []
  for aa in all_as:
    link = aa.get('href', "")
    if '/stores/page' in link and not '/feed' in link:
      link = 'https://www.amazon.com' + link
      links.append(link)
  return links
  
def get_sub_categories(link):
  headers = get_fake_header()
  resp = requests.get(link, headers=headers)
  soup=BeautifulSoup(resp.text,'html.parser')
  linksRaw = soup.find_all('a', href=lambda href: href and '/stores/page' in href,
                      attrs={'aria-label': lambda label: label and 'learn more' in label.lower()})
  links = []
  for link in linksRaw:
    link = link.get('href', '')
    link = 'https://www.amazon.com' + link
    links.append(link)
  return links


def get_sub_sub_categories(link):
  headers = get_fake_header()
  resp = requests.get(link, headers=headers)
  soup = BeautifulSoup(resp.text,'html.parser')
  products_ = soup.findAll('div', {'data-csa-c-type': 'item'})
  products = []
  for product in products_:
    asin = product.get('data-csa-c-item-id','').split('.')[-1].strip() # amzn1.asin.B0B23LXNC8
    sku = ""
    name = product.find('h2',{'id': 'asin-title'}).get_text().strip()
    image = product.find('img',{'data-testid': 'image'}).get('src')
    products.append({
      'name': name,
      'asin': asin,
      'sku': sku,
      'image_url': image,
    })
  return products


def scrape_amazon_products(brand):
  pages = get_all_pages(brand.name, brand.pageId)
  all_products = []
  for page in pages:
    sub_pages = get_sub_categories(page)
    for sub_cat in sub_pages:
      products = get_sub_sub_categories(sub_cat)
      all_products += products
  return all_products