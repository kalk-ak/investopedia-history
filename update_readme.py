import csv
import os

csv_file = "performance-history-2026-01-21.csv"
readme_file = "README.md"

# Generate Markdown Table
table_lines = []
table_lines.append("### Historical Stock Performance")
table_lines.append("")
table_lines.append("| Date | Stock Value | Cash | Account Value |")
table_lines.append("| :--- | :---------- | :--- | :------------ |")

try:
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # key 'Stock Value' might vary if there are extra spaces, strictly checking headers might be needed
            # But usually DictReader handles it if the header is clean.
            stock_val = row.get("Stock Value", "")
            date_val = row.get("Date", "")
            cash_val = row.get("Cash", "")
            account_val = row.get("Account Value", "")
            table_lines.append(f"| {date_val} | {stock_val} | {cash_val} | {account_val} |")
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
header_marker = "### Historical Stock Performance"
end_marker = "Last updated on"

# Check if the old history table exists
start_index = readme_content.find(header_marker)

if start_index != -1:
    # Found the old table header, remove the old history
    end_index = readme_content.find(end_marker, start_index)
    
    if end_index != -1:
        # Replace content between start_index and end_index (start of footer)
        pre_content = readme_content[:start_index].rstrip()
        post_content = readme_content[end_index:]
        new_content = pre_content + "\n\n" + table_content + post_content
    else:
        # No end marker found after start marker. Replace until end of file.
        pre_content = readme_content[:start_index].rstrip()
        new_content = pre_content + "\n\n" + table_content
else:
    # Table not present, insert it normally
    if end_marker in readme_content:
        parts = readme_content.split(end_marker)
        # Insert before the end marker
        new_content = parts[0].rstrip() + "\n\n" + table_content + end_marker + parts[1]
    else:
        # If marker not found, append to end
        new_content = readme_content + "\n\n" + table_content

# Write README
with open(readme_file, "w") as f:
    f.write(new_content)

print(f"Successfully updated {readme_file} with stock history.")