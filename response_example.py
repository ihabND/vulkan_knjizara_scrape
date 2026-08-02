product = {'@context': 'https://schema.org/',
 '@type': 'Product',
 'brand': {'@type': 'Brand'},
 'description': 'Proizvod Signir PASTEL ACADEMY / ČETIRI BOJE je dostupan za '
                'kupovinu, ali trenutno nema detaljan opis. Molimo vas da nas '
                'kontaktirate za više informacija.',
 'image': 'https://www.knjizare-vulkan.rs/files/images/slike_proizvoda/389917.jpg.webp',
 'isbn': '5902277350374',
 'name': 'Signir PASTEL ACADEMY / ČETIRI BOJE',
 'offers': {'@type': 'Offer',
            'availability': 'http://schema.org/InStock',
            'hasMerchantReturnPolicy': {'@type': 'MerchantReturnPolicy',
                                        'applicableCountry': 'rs',
                                        'merchantReturnDays': 14,
                                        'returnFees': 'https://schema.org/FreeReturn',
                                        'returnMethod': 'https://schema.org/ReturnInStore',
                                        'returnPolicyCategory': 'https://schema.org/MerchantReturnFiniteReturnWindow'},
            'itemCondition': 'https://schema.org/NewCondition',
            'price': '110.00',
            'priceCurrency': 'RSD',
            'priceValidUntil': '2026-08-04',
            'shippingDetails': {'@type': 'OfferShippingDetails',
                                'deliveryTime': {'@type': 'ShippingDeliveryTime',
                                                 'handlingTime': {'@type': 'QuantitativeValue',
                                                                  'maxValue': 3,
                                                                  'minValue': 0,
                                                                  'unitCode': 'DAY'},
                                                 'transitTime': {'@type': 'QuantitativeValue',
                                                                 'maxValue': 14,
                                                                 'minValue': 1,
                                                                 'unitCode': 'DAY'}},
                                'shippingDestination': {'@type': 'DefinedRegion',
                                                        'addressCountry': 'rs'},
                                'shippingRate': {'@type': 'MonetaryAmount',
                                                 'currency': 'RSD',
                                                 'value': 0}},
            'url': 'https://www.knjizare-vulkan.rs/signiri/223970-signir-pastel-academy-cetiri-boje'},
 'productID': '223970',
 'sku': '389917'}

data = {}
data["name"] = product['name']
data["sku"] = product['sku']
data["isbn"] = product['isbn']
data["image"] = product['image']
data["price"] = product['offers']['price']

for key, value in data.items():
    print(f"{key} : {value}")


