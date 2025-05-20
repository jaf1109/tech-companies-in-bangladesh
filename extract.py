# import re
import pandas as pd
import json

INPUT_FILE  = 'README.adoc'
OUTPUT_CSV  = 'companies.csv'
OUTPUT_JSON = 'companies.json'

# 1) Read the file
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 2) Parse cells, handling wrapped lines
cells = []
for raw in lines:
    line = raw.rstrip('\n')
    # Skip empty lines
    if not line.strip():
        continue
    # If line starts with '|', it's a new cell
    if line.startswith('|'):
        cells.append(line.lstrip('|').strip())
    else:
        # Otherwise it's a continuation of the previous cell
        if cells:
            cells[-1] += ' ' + line.strip()

# 3) (Optional) Remove header row if present
expected_header = [
    "Company Name",
    "Office location",
    "Technologies",
    "Web presence",
    "No. of Software Engineers"
]
if cells[:5] == expected_header:
    cells = cells[5:]

# 4) Sanity-check that we have a multiple of 5 cells
if len(cells) % 5 != 0:
    raise RuntimeError(f"Expected a multiple of 5 data cells, got {len(cells)}")

# 5) Group into records of 5 cells each
records = []
for i in range(0, len(cells), 5):
    records.append({
        "Company Name":      cells[i],
        "Office location":   cells[i+1],
        "Technologies":      cells[i+2],
        "Web presence":      cells[i+3],
        "No. of Engineers":  cells[i+4],
    })

# 6) Create a DataFrame and write out CSV & JSON
df = pd.DataFrame(records)
df.to_csv(OUTPUT_CSV, index=False)

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(records)} records:")
print(df.head())
