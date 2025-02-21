import os
import xml.etree.ElementTree as ET

def ensure_directory_exists(directory, debug=False):
    if debug:
        print(f"Ensuring directory exists: {directory}")
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_field_info(field_file, debug=False):
    if debug:
        print(f"Extracting field info from: {field_file}")
    tree = ET.parse(field_file)
    root = tree.getroot()
    namespace = {'ns': 'http://soap.sforce.com/2006/04/metadata'}
    label = root.find('ns:label', namespace).text if root.find('ns:label', namespace) is not None else 'N/A'
    api_name = root.find('ns:fullName', namespace).text if root.find('ns:fullName', namespace) is not None else 'N/A'
    field_type = root.find('ns:type', namespace).text if root.find('ns:type', namespace) is not None else 'N/A'
    field_info = (label, api_name, field_type)
    if debug:
        print(f"Extracted field info: {field_info}")
    return field_info

def generate_documentation(object_name, base_path, debug=False):
    if debug:
        print(f"Generating documentation for: {object_name}")
    documentation = []


    # process objects 
    fields_path = os.path.join(base_path, 'objects', object_name,'fields')
    if debug:
        print(f"Fields path: {fields_path}")
        
    if os.path.exists(fields_path):
        for field_file in os.listdir(fields_path):
            if field_file.endswith('.field-meta.xml'):
                field_info = extract_field_info(os.path.join(fields_path, field_file))
                documentation.append(field_info)

    return documentation

def save_documentation(documentation, object_name, output_dir, debug=False):
    if debug:
        print(f"Saving documentation for: {object_name} in {output_dir}")
    ensure_directory_exists(output_dir)
    output_file = os.path.join(output_dir, f'{object_name}.md')
    with open(output_file, 'w') as f:
        f.write(f'# {object_name} Documentation\n\n')
        f.write('| Label | API Name | Type |\n')
        f.write('|-------|----------|------|\n')
        for label, api_name, field_type in documentation:
            f.write(f'| {label} | {api_name} | {field_type} |\n')
