import pandas as pd
from collections import defaultdict

# Load your Excel files
dimension_df = pd.read_excel("dimensioning_flavour.xlsx")
pod_df = pd.read_excel("pod_flavour.xlsx")

# Normalize column names just in case
dimension_df.columns = dimension_df.columns.str.strip().str.lower()
pod_df.columns = pod_df.columns.str.strip().str.lower()

# Initialize doclist
doclist = []

# Iterate over each row in the dimensioning sheet
for idx, row in dimension_df.iterrows():
    operator = row['operator']
    network_function = row['network function']
    package = row['package']
    
    # Extract component requirements
    components = ['dpp', 'dip', 'dmp', 'cmp', 'pmp', 'rmp', 'ipp']
    component_details = "\n".join([f"- {comp.upper()}: {row[comp]}" for comp in components if comp in row])
    
    # Find matching PODs using the package field
    matching_pods = pod_df[pod_df['package'] == package]

    # Format matching PODs
    pod_details = ""
    for i, pod_row in matching_pods.iterrows():
        pod_details += f"""
{len(pod_details.splitlines()) // 8 + 1}. POD Name: {pod_row['postoperative']}
   POD Flavour: {pod_row['podflavour']}
   vCPU Request: {pod_row['vcpurequest']}
   vCPU Limit: {pod_row['vcpulimit']}
   Memory: {pod_row['vmemory']}
   Hugepages: {pod_row.get('hugepage', 'N/A')}
   Persistent Volume: {pod_row.get('persistentvolume', 'N/A')}
"""

    # Compose final chunk
    chunk_text = f"""Operator: {operator}
Network Function: {network_function}
Dimensioning Flavour Package: {package}

Package Requirements:
{component_details}

PODs Using This Flavour:
{pod_details.strip()}

Note: This flavour is used in the {network_function} function by {operator} and shared across the above PODs.
"""

    # Append to doclist
    doclist.append({
        "id": f"{operator}_{network_function}_{package}".lower().replace(" ", "_"),
        "text": chunk_text
    })

# Save to CSV or JSON
pd.DataFrame(doclist).to_csv("rag_doclist.csv", index=False)
