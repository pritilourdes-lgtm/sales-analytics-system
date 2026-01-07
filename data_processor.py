def parse_and_clean_transactions(raw_lines):
    """Parses raw lines into cleaned transaction dictionaries."""
    transactions = []
    for line in raw_lines:
        fields = line.split('|')
        if len(fields) != 8:
            print(f"⚠ Skipping malformed row: {line[:50]}...")
            continue
        try:
            transaction = {
                'transaction_id': fields[0].strip(),
                'date': fields[1].strip(),
                'product_id': fields[2].strip(),
                'product_name': fields[3].strip(),
                'quantity': int(fields[4].strip()),
                'unit_price': float(fields[5].strip().replace(',', '')),
                'customer_id': fields[6].strip(),
                'region': fields[7].strip()
            }
            transactions.append(transaction)
        except ValueError as e:
            print(f"⚠ Skipping row with invalid data: {line[:50]}... Error: {e}")
            continue
    print(f"✓ Parsed {len(transactions)} transactions")
    return transactions


def validate_transactions(transactions):
    """Validates transactions and returns valid ones."""
    valid = []
    invalid_count = 0
    for t in transactions:
        is_valid = (
            t['quantity'] > 0 and
            t['unit_price'] > 0 and
            len(t['date']) == 10 and
            '-' in t['date']
        )
        if is_valid:
            valid.append(t)
        else:
            invalid_count += 1
            print(f"⚠ Invalid transaction: {t.get('transaction_id')}")
    print(f"✓ Validation complete: {len(valid)} valid, {invalid_count} invalid")
    return valid


def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions."""
    return sum(t['quantity'] * t['unit_price'] for t in transactions)


def region_wise_sales(transactions):
    """Calculates total sales for each region."""
    region_sales = {}
    for t in transactions:
        region = t['region']
        revenue = t['quantity'] * t['unit_price']
        region_sales[region] = region_sales.get(region, 0) + revenue
    return region_sales


def date_based_analysis(transactions):
    """Analyzes sales trends by date."""
    daily_sales = {}
    dates = []
    for t in transactions:
        date = t['date']
        revenue = t['quantity'] * t['unit_price']
        dates.append(date)
        daily_sales[date] = daily_sales.get(date, 0) + revenue
    peak_day = max(daily_sales, key=daily_sales.get) if daily_sales else None
    min_date = min(dates) if dates else None
    max_date = max(dates) if dates else None
    return {'daily_trend': daily_sales, 'peak_day': peak_day, 'date_range': (min_date, max_date)}


def product_performance(transactions, bottom_n=3):
    """Return bottom N products by revenue."""
    product_sales = {}
    for t in transactions:
        pid = t['product_id']
        revenue = t['quantity'] * t['unit_price']
        product_sales[pid] = product_sales.get(pid, 0) + revenue
    sorted_products = sorted(product_sales.items(), key=lambda x: x[1])
    low_performers = sorted_products[:bottom_n] if len(sorted_products) >= bottom_n else sorted_products
    return {'low_performers': dict(low_performers)}


def enrich_transactions(transactions, products_dict):
    """Add category, brand, stock from API to each transaction."""
    enriched = []
    matched = 0
    for t in transactions:
        enriched_t = t.copy()
        api_product = products_dict.get(t['product_id']) if products_dict else None
        if api_product:
            enriched_t['category'] = api_product.get('category', 'Unknown')
            enriched_t['brand'] = api_product.get('brand', 'Unknown')
            enriched_t['stock_available'] = api_product.get('stock', 0)
            matched += 1
        else:
            enriched_t['category'] = 'Not Found'
            enriched_t['brand'] = 'Not Found'
            enriched_t['stock_available'] = 0
        enriched.append(enriched_t)
    print(f"✓ Enriched {len(enriched)} transactions ({matched} matched with API)")
    return enriched


if __name__ == "__main__":
    # small demo using in-memory test data
    test_data = [
        {'product_id': '1', 'quantity': 2, 'unit_price': 100, 'region': 'North', 'date': '2024-01-15'},
        {'product_id': '2', 'quantity': 1, 'unit_price': 200, 'region': 'South', 'date': '2024-01-16'},
        {'product_id': '3', 'quantity': 1, 'unit_price': 50, 'region': 'East', 'date': '2024-01-17'},
    ]
    # sample products dict mimicking API output
    sample_products = {
        '1': {'id': 1, 'category': 'Phones', 'brand': 'Acme', 'stock': 10},
        '2': {'id': 2, 'category': 'Laptops', 'brand': 'BrandX', 'stock': 5}
    }

    enriched = enrich_transactions(test_data, sample_products)
    print('Enriched sample:', enriched)
def parse_and_clean_transactions(raw_lines):
    """Parses raw lines into cleaned transaction dictionaries."""
    transactions = []
    for line in raw_lines:
        # Split by pipe delimiter
        fields = line.split('|')
        # Check if row has correct number of fields
        if len(fields) != 8:
            print(f"⚠ Skipping malformed row: {line[:50]}...")
            continue
        try:
            # Create transaction dictionary
            transaction = {
                'transaction_id': fields[0].strip(),
                'date': fields[1].strip(),
                'product_id': fields[2].strip(),
                'product_name': fields[3].strip(),
                'quantity': int(fields[4].strip()),
                'unit_price': float(fields[5].strip().replace(',', '')),
                'customer_id': fields[6].strip(),
                'region': fields[7].strip()
            }
            transactions.append(transaction)
        except ValueError as e:
            print(f"⚠ Skipping row with invalid data: {line[:50]}... Error: {e}")
            continue
    print(f"✓ Parsed {len(transactions)} transactions")
    return transactions


def validate_transactions(transactions):
    """Validates transactions and returns valid ones + summary."""
    valid = []
    invalid_count = 0
    for t in transactions:
        # Business rules validation
        is_valid = (
            t['quantity'] > 0 and              # Can't sell 0 or negative items
            t['unit_price'] > 0 and            # Can't have negative prices
            len(t['date']) == 10 and           # Date must be YYYY-MM-DD (10 chars)
            '-' in t['date']                   # Date must contain dashes
        )
        if is_valid:
            valid.append(t)
        else:
            invalid_count += 1
            print(f"⚠ Invalid transaction: {t.get('transaction_id')}")
    print(f"✓ Validation complete: {len(valid)} valid, {invalid_count} invalid")
    return valid


def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions."""
    total = 0
    for t in transactions:
        revenue = t['quantity'] * t['unit_price']
        total += revenue
    return total


def region_wise_sales(transactions):
    """Calculates total sales for each region."""
    region_sales = {}
    for t in transactions:
        region = t['region']
        revenue = t['quantity'] * t['unit_price']
        region_sales[region] = region_sales.get(region, 0) + revenue
    return region_sales


def date_based_analysis(transactions):
    """Analyzes sales trends by date."""
    daily_sales = {}
    dates = []
    for t in transactions:
        date = t['date']
        revenue = t['quantity'] * t['unit_price']
        dates.append(date)
        daily_sales[date] = daily_sales.get(date, 0) + revenue
    peak_day = max(daily_sales, key=daily_sales.get) if daily_sales else None
    min_date = min(dates) if dates else None
    max_date = max(dates) if dates else None
    return {
        'daily_trend': daily_sales,
        'peak_day': peak_day,
        'date_range': (min_date, max_date)
    }


if __name__ == "__main__":
    # Sample test data
    test_data = [
        {'product_id': '1', 'quantity': 2, 'unit_price': 100, 'region': 'North', 'date': '2024-01-15'},
        {'product_id': '2', 'quantity': 1, 'unit_price': 200, 'region': 'South', 'date': '2024-01-16'},
        {'product_id': '1', 'quantity': 1, 'unit_price': 100, 'region': 'North', 'date': '2024-01-17'},
    ]

    print("Total Revenue:", calculate_total_revenue(test_data))
    print("Region Sales:", region_wise_sales(test_data))
    print("Date Analysis:", date_based_analysis(test_data))
    # product_performance defined inline earlier in module main usage; recreate here for test
    def product_performance(transactions):
        product_sales = {}
        for t in transactions:
            pid = t['product_id']
            revenue = t['quantity'] * t['unit_price']
            product_sales[pid] = product_sales.get(pid, 0) + revenue
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1])
        low_performers = sorted_products[:3] if len(sorted_products) >= 3 else sorted_products
        return {'low_performers': dict(low_performers)}

    print("Product Performance:", product_performance(test_data))
def parse_and_clean_transactions(raw_lines):
    """Parses raw lines into cleaned transaction dictionaries."""
    transactions = []
    for line in raw_lines:
        # Split by pipe delimiter
        fields = line.split('|')
        # Check if row has correct number of fields
        if len(fields) != 8:
            print(f"⚠ Skipping malformed row: {line[:50]}...")
            continue
        try:
            # Create transaction dictionary
            transaction = {
                'transaction_id': fields[0].strip(),
                'date': fields[1].strip(),
                'product_id': fields[2].strip(),
                'product_name': fields[3].strip(),
                'quantity': int(fields[4].strip()),
                'unit_price': float(fields[5].strip().replace(',', '')),
                'customer_id': fields[6].strip(),
                'region': fields[7].strip()
            }
            transactions.append(transaction)
        except ValueError as e:
            print(f"⚠ Skipping row with invalid data: {line[:50]}... Error: {e}")
            continue
    print(f"✓ Parsed {len(transactions)} transactions")
    return transactions


def validate_transactions(transactions):
    """Validates transactions and returns valid ones + summary."""
    valid = []
    invalid_count = 0
    for t in transactions:
        # Business rules validation
        is_valid = (
            t['quantity'] > 0 and              # Can't sell 0 or negative items
            t['unit_price'] > 0 and            # Can't have negative prices
            len(t['date']) == 10 and           # Date must be YYYY-MM-DD (10 chars)
            '-' in t['date']                   # Date must contain dashes
        )
        if is_valid:
            valid.append(t)
        else:
            invalid_count += 1
            print(f"⚠ Invalid transaction: {t.get('transaction_id')}")
    print(f"✓ Validation complete: {len(valid)} valid, {invalid_count} invalid")
    return valid


def calculate_total_revenue(transactions):
    """Calculates total revenue from all transactions."""
    total = 0
    for t in transactions:
        revenue = t['quantity'] * t['unit_price']
        total += revenue
    return total


def region_wise_sales(transactions):
    """Calculates total sales for each region."""
    region_sales = {}
    for t in transactions:
        region = t['region']
        revenue = t['quantity'] * t['unit_price']
        region_sales[region] = region_sales.get(region, 0) + revenue
    return region_sales


if __name__ == "__main__":
    import os, sys
    # ensure project root is on sys.path so `utils` package is importable
    sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
    from utils.file_handler import read_sales_data
    data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.txt'))
    raw = read_sales_data(data_path)
    # remove header if present
    if raw and raw[0].startswith('TransactionID'):
        raw = raw[1:]
    txs = parse_and_clean_transactions(raw)
    valid_txs = validate_transactions(txs)
    # simple summary
    total_revenue = calculate_total_revenue(valid_txs)
    print(f"Total transactions (valid): {len(valid_txs)}")
    print(f"Total revenue (valid): {total_revenue:.2f}")
    # region-wise summary
    regions = region_wise_sales(valid_txs)
    print("Region-wise sales:")
    for r, amt in regions.items():
        print(f"  {r}: {amt:.2f}")
def parse_and_clean_transactions(raw_lines):
    """Parses raw lines into cleaned transaction dictionaries."""
    transactions = []
    for line in raw_lines:
        # Split by pipe delimiter
        fields = line.split('|')
        # Check if row has correct number of fields
        if len(fields) != 8:
            print(f"⚠ Skipping malformed row: {line[:50]}...")
            continue
        try:
            # Create transaction dictionary
            transaction = {
                'transaction_id': fields[0].strip(),
                'date': fields[1].strip(),
                'product_id': fields[2].strip(),
                'product_name': fields[3].strip(),
                'quantity': int(fields[4].strip()),
                'unit_price': float(fields[5].strip().replace(',', '')),
                'customer_id': fields[6].strip(),
                'region': fields[7].strip()
            }
            transactions.append(transaction)
        except ValueError as e:
            print(f"⚠ Skipping row with invalid data: {line[:50]}... Error: {e}")
            continue
    print(f"✓ Parsed {len(transactions)} transactions")
    return transactions


def validate_transactions(transactions):
    """Validates transactions and returns valid ones + summary."""
    valid = []
    invalid_count = 0
    for t in transactions:
        # Business rules validation
        is_valid = (
            t['quantity'] > 0 and              # Can't sell 0 or negative items
            t['unit_price'] > 0 and            # Can't have negative prices
            len(t['date']) == 10 and           # Date must be YYYY-MM-DD (10 chars)
            '-' in t['date']                   # Date must contain dashes
        )
        if is_valid:
            valid.append(t)
        else:
            invalid_count += 1
            print(f"⚠ Invalid transaction: {t.get('transaction_id')}")
    print(f"✓ Validation complete: {len(valid)} valid, {invalid_count} invalid")
    return valid


if __name__ == "__main__":
    import os, sys
    # ensure project root is on sys.path so `utils` package is importable
    sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
    from utils.file_handler import read_sales_data
    data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.txt'))
    raw = read_sales_data(data_path)
    # remove header if present
    if raw and raw[0].startswith('TransactionID'):
        raw = raw[1:]
    txs = parse_and_clean_transactions(raw)
    valid_txs = validate_transactions(txs)
    # simple summary
    total_revenue = sum(t['quantity'] * t['unit_price'] for t in valid_txs)
    print(f"Total transactions (valid): {len(valid_txs)}")
    print(f"Total revenue (valid): {total_revenue:.2f}")
def parse_and_clean_transactions(raw_lines):
    """Parses raw lines into cleaned transaction dictionaries."""
    transactions = []
    for line in raw_lines:
        # Split by pipe delimiter
        fields = line.split('|')
        # Check if row has correct number of fields
        if len(fields) != 8:
            print(f"⚠ Skipping malformed row: {line[:50]}...")
            continue
        try:
            # Create transaction dictionary
            transaction = {
                'transaction_id': fields[0].strip(),
                'date': fields[1].strip(),
                'product_id': fields[2].strip(),
                'product_name': fields[3].strip(),
                'quantity': int(fields[4].strip()),
                'unit_price': float(fields[5].strip().replace(',', '')),
                'customer_id': fields[6].strip(),
                'region': fields[7].strip()
            }
            transactions.append(transaction)
        except ValueError as e:
            print(f"⚠ Skipping row with invalid data: {line[:50]}... Error: {e}")
            continue
    print(f"✓ Parsed {len(transactions)} transactions")
    return transactions


if __name__ == "__main__":
    import os, sys
    # ensure project root is on sys.path so `utils` package is importable
    sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
    from utils.file_handler import read_sales_data
    data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.txt'))
    raw = read_sales_data(data_path)
    # remove header if present
    if raw and raw[0].startswith('TransactionID'):
        raw = raw[1:]
    txs = parse_and_clean_transactions(raw)
    def parse_and_clean_transactions(raw_lines):
        """Parses raw lines into cleaned transaction dictionaries."""
        transactions = []
        for line in raw_lines:
            # Split by pipe delimiter
            fields = line.split('|')
            # Check if row has correct number of fields
            if len(fields) != 8:
                print(f"⚠ Skipping malformed row: {line[:50]}...")
                continue
            try:
                # Create transaction dictionary
                transaction = {
                    'transaction_id': fields[0].strip(),
                    'date': fields[1].strip(),
                    'product_id': fields[2].strip(),
                    'product_name': fields[3].strip(),
                    'quantity': int(fields[4].strip()),
                    'unit_price': float(fields[5].strip().replace(',', '')),
                    'customer_id': fields[6].strip(),
                    'region': fields[7].strip()
                }
                transactions.append(transaction)
            except ValueError as e:
                print(f"⚠ Skipping row with invalid data: {line[:50]}... Error: {e}")
                continue
        print(f"✓ Parsed {len(transactions)} transactions")
        return transactions


    if __name__ == "__main__":
        import os
        from utils.file_handler import read_sales_data
        data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.txt'))
        raw = read_sales_data(data_path)
        # remove header if present
        if raw and raw[0].startswith('TransactionID'):
            raw = raw[1:]
        txs = parse_and_clean_transactions(raw)
        # simple summary
        total_revenue = sum(t['quantity'] * t['unit_price'] for t in txs)
        print(f"Total transactions: {len(txs)}")
        print(f"Total revenue: {total_revenue:.2f}")
