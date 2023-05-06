import requests
import yaml
from backend.models import (Category, Parameter, Product, ProductInfo,
                            ProductParameter, Shop)

replacements = {
    'shop': 'name',
    'goods': 'product_infos',
    'parameters': 'product_parameters',
    'id': 'external_id'
    }


def yaml_shop_load(data, request):
    product_infos = data.pop('goods')
    categories = data.pop('categories')

    shop, _ = Shop.objects.get_or_create(name=data.pop('shop'),
                                         user=request.user,
                                         )

    for category in categories:
        obj, _ = Category.objects.update_or_create(defaults={'name': category.pop('name')},
                                                   **category,
                                                   )
        obj.shops.add(shop)
        obj.save()

    for product in product_infos:
        product_name, _ = Product.objects.get_or_create(name=product.pop('name'),
                                                        category_id=product.pop('category'),
                                                        )
        product_parameters = product.pop('parameters')

        defaults = {'price': product.pop('price')}
        defaults.update({'price_rrc': product.pop('price_rrc')})
        defaults.update({'quantity': product.pop('quantity')})
        external_id = product.pop('id')
        obj, _ = ProductInfo.objects.update_or_create(defaults=defaults,
                                                      shop=shop,
                                                      product_id = product_name.id,
                                                      external_id=external_id,
                                                      **product,
                                                      )

        for key, val in product_parameters.items():
            parameter, _ = Parameter.objects.get_or_create(name=key)
            ProductParameter.objects.update_or_create(defaults={'value': val},
                                                      parameter=parameter,
                                                      product_info=obj,
                                                      )

    return True


def link_shop_load(link, request):
    data = requests.get(link).content
    return yaml_shop_load(data, request)


def file_shop_load(file, request):
    with file.open() as f:
        data = yaml.safe_load(f)
    return yaml_shop_load(data, request)
