import pandas as pd

# Load the Dimensioning Flavour and POD Flavour sheets
dimensioning_flavour_df = pd.read_excel('dimensioning_flavour_sheet.xlsx')
pod_flavour_df = pd.read_excel('pod_flavour_sheet.xlsx')

# Initialize an empty list to store the doclist
doclist = []

# Iterate over each unique combination of Operator, Network Function, and Dimensioning Flavour
for idx, row in dimensioning_flavour_df.iterrows():
    operator = row['Operator']
    network_function = row['Network Function']
    dimensioning_flavour = row['Dimensioning-flavour']
    package = row['package']

    # Filter POD Flavour sheet to match the current Dimensioning Flavour (e.g., 'mediumtddregular')
    pod_types = ['dpp', 'dip', 'dmp', 'cmp', 'pmp', 'rmp', 'ipp']
    pod_flavours_for_flavour = pod_flavour_df[pod_flavour_df['Pod type'].isin(pod_types)]

    # Initialize the document
    doc = f"Operator: {operator}\nNetwork Function: {network_function}\nDimensioning Flavour: {dimensioning_flavour}\nPackage: {package}\n\nPod Types and their Resource Requirements:\n"
    
    # Add pod flavour details
    for pod_type in pod_types:
        pod_flavour_row = pod_flavours_for_flavour[pod_flavours_for_flavour['Pod type'] == pod_type]
        if not pod_flavour_row.empty:
            pod_flavour = pod_flavour_row.iloc[0]['Pod flavour']
            vcpu_request = pod_flavour_row.iloc[0]['vcpurequest(vCore)']
            vcpu_limit = pod_flavour_row.iloc[0]['vcpulimit(vCore)']
            vmemory = pod_flavour_row.iloc[0]['vmemory(GB)']
            hugepage = pod_flavour_row.iloc[0]['hugepage(GB)']
            persistent_volume = pod_flavour_row.iloc[0]['persistentvolume(GB)']
            package_pod = pod_flavour_row.iloc[0]['package']
            
            # Append pod information to doc
            doc += f"- Pod Type: {pod_type}\n"
            doc += f"  Pod Flavour: {pod_flavour}\n"
            doc += f"  vCPU Request (vCore): {vcpu_request}\n"
            doc += f"  vCPU Limit (vCore): {vcpu_limit}\n"
            doc += f"  vMemory (GB): {vmemory}\n"
            doc += f"  Hugepage (GB): {hugepage}\n"
            doc += f"  Persistent Volume (GB): {persistent_volume}\n"
            doc += f"  Package: {package_pod}\n\n"

    # Append the document to the doclist
    doclist.append(doc)

# Save the doclist to a text file
with open('doclist.txt', 'w') as f:
    for doc in doclist:
        f.write(doc + "\n\n" + "="*80 + "\n\n")

print("Doclist generation completed and saved to 'doclist.txt'.")
