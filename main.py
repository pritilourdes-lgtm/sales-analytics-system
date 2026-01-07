import os
from datetime import datetime

from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_and_clean_transactions,
    validate_transactions,
    calculate_total_revenue,
    region_wise_sales,
    date_based_analysis,
    product_performance,
    enrich_transactions,
)
from utils.api_handler import fetch_all_products, save_enriched_data


def generate_sales_report(transactions, enriched_transactions):
    """Generates a comprehensive sales report."""
    # Calculate metrics
    total_revenue = calculate_total_revenue(transactions)
    total_trans = len(transactions)
    avg_order = total_revenue / total_trans if total_trans else 0

    date_analysis = date_based_analysis(transactions)
    region_analysis = region_wise_sales(transactions)
    product_analysis = product_performance(transactions)

    # Build report lines
    report_lines = [
        "=" * 60,
        "SALES ANALYTICS REPORT".center(60),
        "=" * 60,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Records Processed: {total_trans}",
        "",
        "-" * 60,
        "OVERALL SUMMARY",
        "-" * 60,
        f"Total Revenue: ${total_revenue:,.2f}",
        f"Total Transactions: {total_trans}",
        f"Average Order Value: ${avg_order:,.2f}",
        f"Date Range: {date_analysis['date_range'][0]} to {date_analysis['date_range'][1]}",
        f"Peak Sales Day: {date_analysis['peak_day']}",
        "",
        "-" * 60,
        "REGION-WISE PERFORMANCE",
        "-" * 60,
        f"{'Region':<20} {'Total Sales':>15}",
    ]

    # Add region data (sorted by sales descending)
    for region, sales in sorted(region_analysis.items(), key=lambda x: x[1], reverse=True):
        report_lines.append(f"{region:<20} ${sales:>14,.2f}")

    report_lines.extend([
        "",
        "-" * 60,
        "LOW PERFORMING PRODUCTS (Bottom 3)",
        "-" * 60,
        f"{'Product ID':<15} {'Revenue':>15}",
    ])

    # Add low performers
    for pid, rev in product_analysis['low_performers'].items():
        report_lines.append(f"{pid:<15} ${rev:>14,.2f}")

    report_lines.extend([
        "",
        "=" * 60,
        "END OF REPORT",
        "=" * 60,
    ])

    # Ensure output dir exists
    os.makedirs("output", exist_ok=True)

    # Write to file
    try:
        with open('output/sales_report.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print("✓ Report generated: output/sales_report.txt")
    except Exception as e:
        print(f"✗ Error generating report: {e}")


def main():
    """Main workflow of the sales analytics system."""

    print("\n" + "=" * 60)
    print("SALES ANALYTICS SYSTEM".center(60))
    print("=" * 60 + "\n")

    # === STEP 1-3: Read, Parse, Validate ===
    print("📂 Step 1: Reading sales data...")
    raw_lines = read_sales_data('data/sales_data.txt')

    if not raw_lines:
        print("❌ No data to process. Exiting.")
        return

    print("\n📊 Step 2: Parsing transactions...")
    transactions = parse_and_clean_transactions(raw_lines)

    print("\n✅ Step 3: Validating data...")
    transactions = validate_transactions(transactions)

    if not transactions:
        print("❌ No valid transactions. Exiting.")
        return

    # === STEP 4-6: User Filtering ===
    print("\n" + "-" * 60)
    print("FILTERING OPTIONS")
    print("-" * 60)

    # Show available options
    regions = list(set(t['region'] for t in transactions))
    amounts = [t['quantity'] * t['unit_price'] for t in transactions]

    print(f"Available regions: {', '.join(sorted(regions))}")
    print(f"Transaction amount range: ${min(amounts):,.2f} - ${max(amounts):,.2f}")

    # Ask user if they want to filter
    filter_choice = input("\n🔍 Apply filters? (y/n): ").strip().lower()

    if filter_choice == 'y':
        print("\nEnter filter criteria (press Enter to skip):")

        # Region filter
        region_filter = input(f"  Region [{', '.join(sorted(regions))}]: ").strip()

        # Amount filters
        min_amt = input("  Minimum amount: ").strip()
        max_amt = input("  Maximum amount: ").strip()

        # Apply filters
        filtered = transactions

        if region_filter:
            filtered = [t for t in filtered if t['region'] == region_filter]
            print(f"  ✓ Filtered by region: {region_filter}")

        if min_amt:
            try:
                min_val = float(min_amt)
                filtered = [t for t in filtered if t['quantity']*t['unit_price'] >= min_val]
                print(f"  ✓ Filtered by min amount: ${min_val:,.2f}")
            except ValueError:
                print("  ⚠ Invalid min amount, skipping")

        if max_amt:
            try:
                max_val = float(max_amt)
                filtered = [t for t in filtered if t['quantity']*t['unit_price'] <= max_val]
                print(f"  ✓ Filtered by max amount: ${max_val:,.2f}")
            except ValueError:
                print("  ⚠ Invalid max amount, skipping")

        transactions = filtered
        print(f"\n✓ Filtered to {len(transactions)} records")

    # === STEP 7-8: Display Analysis ===
    print("\n" + "-" * 60)
    print("QUICK ANALYSIS")
    print("-" * 60)

    total_rev = calculate_total_revenue(transactions)
    print(f"💰 Total Revenue: ${total_rev:,.2f}")

    regions_sales = region_wise_sales(transactions)
    print(f"🌎 Top Region: {max(regions_sales, key=regions_sales.get)} (${max(regions_sales.values()):,.2f})")

    date_info = date_based_analysis(transactions)
    print(f"📅 Peak Sales Day: {date_info['peak_day']}")

    # === STEP 9-11: API Enrichment ===
    print("\n" + "-" * 60)
    print("API ENRICHMENT")
    print("-" * 60)

    products_dict = fetch_all_products()
    enriched = enrich_transactions(transactions, products_dict)
    save_enriched_data(enriched)

    # === STEP 12: Generate Report ===
    print("\n" + "-" * 60)
    print("REPORT GENERATION")
    print("-" * 60)

    generate_sales_report(transactions, enriched)

    # === Completion ===
    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!".center(60))
    print("=" * 60)
    print("\nGenerated files:")
    print("  📄 output/enriched_sales_data.txt")
    print("  📊 output/sales_report.txt")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        import traceback
        traceback.print_exc()


