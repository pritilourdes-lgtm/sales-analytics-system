def read_sales_data(path):
    """Read sales data file and return list of non-empty lines."""
    lines = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return lines


if __name__ == "__main__":
    import os
    data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_data.txt'))
    lines = read_sales_data(data_path)
    # remove header if present
    if lines and lines[0].startswith('TransactionID'):
        lines = lines[1:]
    print("\u2713 Successfully read file with utf-8 encoding")
    print(f"Read {len(lines)} lines")
    print("First line:", lines[0] if lines else "None")
