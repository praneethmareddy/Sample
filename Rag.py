import pandas as pd
import os
import json

# Load Excel files
dimensioning_df = pd.read_excel("dimensioning_flavour_sheet.xlsx")
pod_df = pd.read_excel("pod_flavour_sheet.xlsx")

# Normalize column names (optional, just in case)
dimensioning_df.columns = dimensioning_df.columns.str.strip().str.lower()
pod_df.columns = pod_df.columns.str.strip().str.lower()

# Create output folder
output_dir = "rag_doclist"
os.makedirs(output_dir, exist_ok=True)

doclist = []

# Loop over each row in dimensioning sheet
for _, dim_row in dimensioning_df.iterrows():
    operator = dim_row["operator"]
    network_function = dim_row["network function"]
    package = dim_row["dimensioning-flavour package"]

    # Filter relevant PODs for this package
    related_pods = pod_df[pod_df["package"] == package]

    # Build dimensioning section
    dim_section = "\n".join([
        f"- DPP: {dim_row['dpp']}",
        f"- DIP: {dim_row['dip']}",
        f"- DMP: {dim_row['dmp']}",
        f"- CMP: {dim_row['cmp']}",
        f"- PMP: {dim_row['pmp']}",
        f"- RMP: {dim_row['rmp']}",
        f"- IPP: {dim_row['ipp']}",
    ])

    # Build POD section
    pod_section = ""
    for idx, pod in related_pods.iterrows():
        pod_section += f"""
{idx+1}. Type: {pod['pod type']}
   vCPU Request: {pod['vcpurequest(vcore)']}
   vCPU Limit: {pod['vcpulimit(vcore)']}
   Memory: {pod['vmemory(gb)']} GB
   HugePage: {pod['hugepage(gb)']} GB
   Persistent Volume: {pod['persistentvolume(gb)']} GB
"""

    # Final doc string
    doc = f"""Operator: {operator}
Network Function: {network_function}
Package/Flavour: {package}

Dimensioning Components:
{dim_section}

Associated PODs:{pod_section if pod_section else " None"}
"""

    # Save as text file (optional)
    filename = f"{operator}_{network_function}_{package}.txt".replace(" ", "_").lower()
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(doc)

    # Add to doclist for embedding
    doclist.append({
        "content": doc,
        "metadata": {
            "operator": operator,
            "network_function": network_function,
            "package": package
        }
    })

# Optional: Save doclist as JSON
with open(os.path.join(output_dir, "doclist.json"), "w") as f:
    json.dump(doclist, f, indent=2)

print(f"Generated {len(doclist)} doc chunks in '{output_dir}' folder.")
