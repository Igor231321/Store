import uuid

import requests

from integrations.models import ApiKey

#

URL = 'https://api.novaposhta.ua/v2.0/json/'
API_KEY = ApiKey.objects.filter(service=ApiKey.ServiceChoices.NOVA_POST)


def load_countries():
    from order.models import Country
    page = 1
    limit = 100

    while True:
        json = {
            "apiKey": API_KEY,
            "modelName": "AddressGeneral",
            "calledMethod": "getSettlements",
            "methodProperties": {
                "Warehouse": "1",
                "Page": str(page),
                "Limit": str(limit),
            }
        }

        response = requests.post(url=URL, json=json)
        data = response.json()

        if not data["success"]:
            print("Помилка у відповіді запиту")
            break

        countries = data.get("data")
        if not countries:
            print("Данних не має")
            break

        result_countries = []

        for county in countries:
            result_countries.append(Country(ref=county["Ref"],
                                            description=county["Description"],
                                            area_description=county["AreaDescription"],
                                            country_type=county["SettlementTypeDescription"])
                                    )

        page += 1

        Country.objects.bulk_create(result_countries)
        print(f"Запрос успешно сработал, добавлено в БД: {len(result_countries)}")


def load_warehouses():
    from order.models import Country, Warehouse

    Warehouse.objects.all().delete()
    print("База успішно оновлена...")
    print("Отримання данних від API...")

    json = {
        "apiKey": API_KEY,
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
        }
    }

    response = requests.post(url=URL, json=json)
    data = response.json()

    result = []
    no_countries = []
    for warehouse in data["data"]:
        try:
            country = Country.objects.get(ref=warehouse['SettlementRef'])

            if warehouse["TypeOfWarehouse"] in ["95dc212d-479c-4ffb-a8ab-8c1b9073d0bc",
                                                "f9316480-5f2d-425d-bc2c-ac7cd29decf0"]:
                warehouse_type = Warehouse.WarehouseType.TERMINAL
            else:
                warehouse_type = Warehouse.WarehouseType.POST_OFFICE

            warehouse_obj = Warehouse(country=country,
                                      description=warehouse["Description"],
                                      warehouse_type=warehouse_type,
                                      number=warehouse["Number"])

            result.append(warehouse_obj)
        except Country.DoesNotExist:
            no_countries.append(warehouse["SettlementRef"])

    Warehouse.objects.bulk_create(result)
    print("Успішно")
    print(f"Загружено відділень: {len(result)}")


def generate_reference():
    text = uuid.uuid4().hex
    digits = "".join(filter(str.isdigit, text))
    return digits[:6]
