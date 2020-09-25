import json
import logging
import os
import requests
from requests.exceptions import HTTPError
from emailClient import sendEmail

# NVidia store URL
NVIDIA_URL = 'https://api-prod.nvidia.com/direct-sales-shop/DR/add-to-cart'#os.environ['nvidia_url']
# Product ID of the 3080
RTX3080 = '5438481700'
RTX2060 = '5379432500'
PRODUCT_ID = RTX3080

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    
    product_payload = {
        'products': [
            {
                'productId':PRODUCT_ID,
                'quantity': 1
                
            }
        ]
    }
    headers = {
        'Host':'api-prod.nvidia.com',
        'Connection':'keep-alive',
        'Content-Length':'52',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'nvidia_shop_id':'8210009D3B8271EFA27E6AB0E174502C',
        'Content-Type':'application/json',
        'Origin':'https://www.nvidia.com',
        'Sec-Fetch-Site':'same-site',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Dest':'empty',
        'Referer':'https://www.nvidia.com/en-us/shop/geforce/gpu/?page=1&limit=9&locale=en-us&category=GPU&gpu=RTX%202080%20SUPER,RTX%202080%20Ti,RTX%202070%20SUPER,RTX%202070,RTX%202060%20SUPER,RTX%202060&gpu_filter=TITAN%20RTX~0,RTX%202080%20Ti~2,RTX%202080%20SUPER~7,RTX%202070%20SUPER~10,RTX%202070~1,RTX%202060%20SUPER~9,RTX%202060~0,GTX%201660%20Ti~0,GTX%201660%20SUPER~0,GTX%201660~0,GTX%201650%20SUPER~0,GTX%201650~0',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9'
    }

    try:
        response = requests.post(NVIDIA_URL,headers=headers, data=json.dumps(product_payload))

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err.response.content}')  
    except Exception as err:
        logger.error(f'Other error occurred: {err}')  
    else:
        logger.info('Success!')
        respData = response.json()
        logger.info(respData)
        if respData['location']:
            logger.info('We have a card! Email email email')
            sendEmail(respData['location'])