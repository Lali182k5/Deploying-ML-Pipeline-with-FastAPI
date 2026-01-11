import requests

BASE_URL = "http://127.0.0.1:8000"


def main():
    health = requests.get(f"{BASE_URL}/")
    print("Health:", health.status_code, health.json())

    schema = requests.get(f"{BASE_URL}/schema")
    print("Schema tables:", list(schema.json().get("tables", {}).keys()))

    payload = {"question": "Show revenue by customer", "filters": {}, "limit": 5}
    query = requests.post(f"{BASE_URL}/query", json=payload)
    print("Query status:", query.status_code)
    print("SQL:", query.json().get("sql"))
    print("Result preview:", query.json().get("result", {}))


if __name__ == "__main__":
    main()

