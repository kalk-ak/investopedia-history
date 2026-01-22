import csv
import os

csv_file = "performance-history-2026-01-21.csv"
readme_file = "README.md"

# Generate Markdown Table
table_lines = []
table_lines.append("### Historical Stock Performance")
table_lines.append("")
table_lines.append("| Date | Stock Value |")
table_lines.append("| :--- | :---------- |")

try:
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # key 'Stock Value' might vary if there are extra spaces, strictly checking headers might be needed
            # But usually DictReader handles it if the header is clean.
            # The provided content shows "Stock Value" as the 3rd column.
            stock_val = row.get("Stock Value", "")
            date_val = row.get("Date", "")
            table_lines.append(f"| {date_val} | {stock_val} |")
except FileNotFoundError:
    print(f"Error: {csv_file} not found.")
    exit(1)

table_content = "\n".join(table_lines) + "\n\n"

# Read README
try:
    with open(readme_file, "r") as f:
        readme_content = f.read()
except FileNotFoundError:
    print(f"Error: {readme_file} not found.")
    exit(1)

# Insert Table
# We look for "Last updated on" to insert before it.
marker = "Last updated on"
if marker in readme_content:
    parts = readme_content.split(marker)
    # parts[0] is everything before, parts[1] is everything after (likely just the date)
    # We want to insert at the end of parts[0], but maybe ensure some spacing.
    new_content = parts[0].rstrip() + "\n\n" + table_content + marker + parts[1]
else:
    # If marker not found, append to end
    new_content = readme_content + "\n\n" + table_content

# Write README
with open(readme_file, "w") as f:
    f.write(new_content)

print(f"Successfully updated {readme_file} with stock history.")
