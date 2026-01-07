import os
try:
	import requests
except ImportError:
	requests = None
import json

try:
	# Provide a thin wrapper to the data_processor enrich function if available
	from utils.data_processor import enrich_transactions as _enrich_transactions
except Exception:
	_enrich_transactions = None


def fetch_all_products():
	"""Fetch all products from DummyJSON API and return a dict keyed by product id (str)."""
	url = "https://dummyjson.com/products?limit=100"
	if requests is None:
		print("✗ 'requests' not installed — cannot fetch products.")
		return {}
	try:
		print(" Fetching product data from API...")
		resp = requests.get(url, timeout=10)
		resp.raise_for_status()
		data = resp.json()
		products = data.get("products", [])
		products_dict = {str(p["id"]): p for p in products}
		print(f"✓ Fetched {len(products_dict)} products from API")
		return products_dict
	except requests.RequestException as e:
		print(f"✗ API Error: {e}")
		return {}


if __name__ == "__main__":
	products = fetch_all_products()
	if products:
		print("\nSample product:")
		print(products.get('1'))  # iPhone 9


def enrich_transactions(transactions, products_dict):
	"""Wrapper that calls the real `enrich_transactions` in `utils.data_processor` if available.
	If the internal function is not importable, returns the transactions unchanged.
	"""
	if _enrich_transactions is None:
		print("✗ enrich_transactions not available (utils.data_processor missing)")
		return transactions
	return _enrich_transactions(transactions, products_dict)


def save_enriched_data(enriched_transactions, path="output/enriched_transactions.json"):
	"""Persist enriched transactions to a JSON file under `output/`.
	Creates the `output/` directory if missing.
	"""
	os.makedirs(os.path.dirname(path) or "output", exist_ok=True)
	try:
		with open(path, "w", encoding="utf-8") as f:
			json.dump(enriched_transactions, f, indent=2, ensure_ascii=False)
		print(f"✓ Saved enriched data: {path}")
	except Exception as e:
		print(f"✗ Error saving enriched data: {e}")
