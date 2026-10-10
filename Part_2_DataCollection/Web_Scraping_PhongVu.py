import requests
import pandas as pd
from fake_useragent import UserAgent
import time

url = "https://discovery.tekoapis.com/api/v2/search-skus-v2"

total_products = []
page = 1
page_size = 40
max_products = int(input('Input the maximum amount of products need scraping: '))

while True:
    payload = {
        "terminalId": 4,
        "smartActivationClientId": "be49a8bb-12dd-4f77-b6f5-6f6c845e3f2e",
        "filter": {},
        "isNeedFeaturedProducts": True,
        "isNewVisitorOnly": False,
        "page": page,
        "pageSize": page_size,
        "returnFilterable": [],
        "slug": "/c/chuot-may-tinh",
        "sorting": {
            "sort": "SORT_BY_CREATED_AT",
            "order": "ORDER_BY_DESCENDING"
        }
    }
    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout = 10)
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            break

        data = response.json()
        products = (data.get('data',{}).get('products',[]))
        if not products:
            print('All products have been scraped')
            break

        for product in products:
            sku = product.get('sku')
            name = product.get('name')
            brand = product.get('brandName')
            retail_price = product.get('supplierRetailPrice')
            latest_price = product.get('latestPrice')
            discount_percent = product.get('discountPercent')
            product_id = product.get('productId')
            discount_amount = product.get('discountAmount')

            total_products.append({
                'ProductId': product_id,
                'sku': sku,
                'Name': name,
                'Brand': brand,
                'Retail_Price': retail_price,
                'Latest_Price': latest_price,
                'Discount_Percent': discount_percent,
                'Discount_Amount': discount_amount,
            })

            if len(total_products) >= max_products:
                break

        print(f'Succeeded in scraping {len(total_products)}/{max_products} products of page {page}')
        if len(total_products) >= max_products:
            print('Reached limit of products need scraping')
            break

        page += 1
        time.sleep(1.5)
    except Exception as e:
        print(f'Error: {e}')
        break

df = pd.DataFrame(total_products)
df.to_csv('Chuot_PhongVu.csv',index=False, encoding='utf-8-sig')
print(f'Finished saving {len(total_products)} products')