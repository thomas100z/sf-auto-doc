import os
import xml.etree.ElementTree as ET
from typing import List, Tuple

def ensure_directory_exists(directory: str, debug: bool = False) -> None:
    if debug:
        print(f"Ensuring directory exists: {directory}")
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_field_info(field_file: str, debug: bool = False) -> Tuple[str, str, str]:
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

def extract_validation_rule_info(rule_file: str, debug: bool = False) -> Tuple[str, str, str]:
    if debug:
        print(f"Extracting validation rule info from: {rule_file}")
    tree = ET.parse(rule_file)
    root = tree.getroot()
    namespace = {'ns': 'http://soap.sforce.com/2006/04/metadata'}
    
    # Only process active rules
    is_active = root.find('ns:active', namespace).text.lower() == 'true' if root.find('ns:active', namespace) is not None else False
    if not is_active:
        return None
        
    name = root.find('ns:fullName', namespace).text if root.find('ns:fullName', namespace) is not None else 'N/A'
    description = root.find('ns:errorMessage', namespace).text if root.find('ns:errorMessage', namespace) is not None else 'N/A'
    formula = root.find('ns:errorConditionFormula', namespace).text if root.find('ns:errorConditionFormula', namespace) is not None else 'N/A'
    
    rule_info = (name, description, formula)
    if debug:
        print(f"Extracted validation rule info: {rule_info}")
    return rule_info

def generate_documentation(object_name: str, base_path: str, debug: bool = False) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
    if debug:
        print(f"Generating documentation for: {object_name}")
    fields_documentation = []
    validation_rules_documentation = []

    # process fields
    fields_path = os.path.join(base_path, 'objects', object_name, 'fields')
    if debug:
        print(f"Fields path: {fields_path}")
        
    if os.path.exists(fields_path):
        for field_file in os.listdir(fields_path):
            if field_file.endswith('.field-meta.xml'):
                field_info = extract_field_info(os.path.join(fields_path, field_file))
                fields_documentation.append(field_info)

    # process validation rules
    validation_rules_path = os.path.join(base_path, 'objects', object_name, 'validationRules')
    if debug:
        print(f"Validation rules path: {validation_rules_path}")
        
    if os.path.exists(validation_rules_path):
        for rule_file in os.listdir(validation_rules_path):
            if rule_file.endswith('.validationRule-meta.xml'):
                rule_info = extract_validation_rule_info(os.path.join(validation_rules_path, rule_file))
                if rule_info:
                    validation_rules_documentation.append(rule_info)

    return fields_documentation, validation_rules_documentation

def save_documentation(fields_documentation: List[Tuple[str, str, str]], validation_rules_documentation: List[Tuple[str, str, str]], object_name: str, output_dir: str, debug: bool = False) -> None:
    if debug:
        print(f"Saving documentation for: {object_name} in {output_dir}")
    ensure_directory_exists(output_dir)
    output_file = os.path.join(output_dir, f'{object_name}.md')
    with open(output_file, 'w') as f:
        f.write(f'# {object_name} Documentation\n\n')
        
        # Write fields table
        f.write('## Fields\n\n')
        f.write('| Label | API Name | Type |\n')
        f.write('|-------|----------|------|\n')
        for label, api_name, field_type in fields_documentation:
            f.write(f'| {label} | {api_name} | {field_type} |\n')
            
        # Write validation rules table if there are any
        if validation_rules_documentation:
            f.write('\n## Validation Rules\n\n')
            f.write('| Name | Description | Formula |\n')
            f.write('|------|-------------|---------|\n')
            for name, description, formula in validation_rules_documentation:
                f.write(f'| {name} | {description} | {formula} |\n')
