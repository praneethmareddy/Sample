import pandas as pd

# Step 1: Load the Excel files
dimensioning_df = pd.read_excel('dimensioning_flavour_sheet.xlsx')
pod_df = pd.read_excel('pod_flavour_sheet.xlsx')

# Step 2: Clean column names (optional but recommended)
dimensioning_df.columns = dimensioning_df.columns.str.strip().str.lower().str.replace('-', '_')
pod_df.columns = pod_df.columns.str.strip().str.lower().str.replace('(', '').str.replace(')', '').str.replace(' ', '_')

# Step 3: Initialize doclist
doclist = []

# Step 4: Group dimensioning data
grouped = dimensioning_df.groupby(['operator', 'network_function', 'dimensioning_flavour'])

for (operator, nf, flavour), group in grouped:
    entry = group.iloc[0]
    package = entry['package']

    # Extract dimensioning resources
    resource_fields = ['dpp', 'dip', 'dmp', 'cmp', 'pmp', 'rmp', 'ipp']
    resource_config = "\n".join([f"- {field.upper()}: {entry[field]}" for field in resource_fields if field in entry])

    # Step 5: Match PODs using the package
    matching_pods = pod_df[pod_df['package'] == package]

    # Format associated PODs
    pod_entries = []
    for _, pod in matching_pods.iterrows():
        pod_text = f"""\
POD Type: {pod['pod_type']}
Pod Flavour: {pod['pod_flavour']}
vCPU Request: {pod['vcpurequest']}
vCPU Limit: {pod['vcpulimit']}
Memory: {pod['vmemory']} GB
HugePage: {pod['hugepage']} GB
PersistentVolume: {pod['persistentvolume']} GB
"""
        pod_entries.append(pod_text.strip())

    pod_section = "\n\n".join(pod_entries) if pod_entries else "No associated PODs found."

    # Step 6: Create final document text
    doc_text = f"""\
Operator: {operator}
Network Function: {nf}
Dimensioning Flavour: {flavour}
Package: {package}

Resource Config:
{resource_config}

Associated POD Flavours:
{pod_section}
"""

    doclist.append(doc_text.strip())

# Step 7: Save to a .txt file or print
with open("doclist.txt", "w") as f:
    for doc in doclist:
        f.write(doc + "\n" + "="*80 + "\n")

# Optionally: Return doclist as a list of strings for embedding
# You can now pass `doclist` to an embedding pipeline like OpenAI, BGE, etc.
