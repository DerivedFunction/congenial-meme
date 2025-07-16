import pypdf
import json
from io import BytesIO
from typing import Dict, Union, Tuple
from dotenv import load_dotenv
import os

load_dotenv("../../.env")  # Loads the .env file

URL = os.getenv("URL")


def fill_pdf_forms(input_pdf_path: str, json_data: str) -> Tuple[bytes, Dict[str, Union[str, list]]]:
    """
    Fills form fields in a PDF based on a JSON input and returns the modified PDF as bytes.
    
    Args:
        input_pdf_path (str): Path to the input PDF file.
        json_data (str): JSON string mapping field names to new values.
            json_data:
            {
                "DOR": 
                "RANK":
                "EDIPI":
                "MI":
                "First Name":
                "Last Name":
                "PMOS":
                "BILMOS":
                "Occasion":
                "PC From":
                "PC To":
                "Last Name RS":
                "First Name RS":
                "MI RS":
                "EDIPI RS":
                "RANK RS":
                "Billet Title":
                "Signature RS": None
                "Date RS": None
                "Signature": None
                "Date": None
                " TOPICS DISSCUSSED":
                " MOSBILLET DESCRIPTION": None
                " MAJOR ACCOMPLISHMENTS  SIGNIFICANT EVENTS THIS PERIOD":
                " PREFORMANCE EVALUATION THIS PERIOD":
                " TASKS ASSIGNED NEXT PERIOD  GOALS":
                " ADDITIONAL COMMENTS":
            }
    
    Returns:
        Tuple[bytes, Dict]: (PDF byte stream, response metadata with status and messages).
    """
    response = {"status": "success", "messages": []}
    
    # Send a request to /mosdesc/<BILMOS> to get the MOS Description
    try:
        import requests
        response_mosdesc = requests.get(f"{URL}/mosdesc/{field_values['BILMOS']}")
        if response_mosdesc.status_code == 200:
            mosdesc_data = response_mosdesc.json()
            if 'desc' in mosdesc_data:
                field_values[' MOSBILLET DESCRIPTION'] = mosdesc_data['desc']
        else:
            response["status"] = "error"
            response["messages"].append("Failed to fetch MOS Description.")
    except Exception as e:
        response["status"] = "error"
        response["messages"].append(f"Failed to fetch MOS Description: {str(e)}")
        return b"", response
    
    try:
        # Parse JSON input
        try:
            field_values = json.loads(json_data)
            if not isinstance(field_values, dict):
                raise ValueError("JSON input must be a dictionary.")
        except json.JSONDecodeError:
            response["status"] = "error"
            response["messages"].append("Invalid JSON format.")
            return b"", response
        
        # Read the PDF
        try:
            reader = pypdf.PdfReader(input_pdf_path)
        except Exception as e:
            response["status"] = "error"
            response["messages"].append(f"Failed to read PDF: {str(e)}")
            return b"", response
        
        # Create a PdfWriter object
        writer = pypdf.PdfWriter()
        
        # Copy pages from reader to writer
        for page in reader.pages:
            writer.add_page(page)
        
        # Check if the PDF has an AcroForm
        if '/AcroForm' not in reader.trailer['/Root']:
            response["status"] = "error"
            response["messages"].append("No form fields found in the PDF.")
            return b"", response
        
        # Get the form fields, including nested ones
        def extract_fields(fields, collected_fields=None):
            if collected_fields is None:
                collected_fields = []
            for field in fields:
                collected_fields.append(field)
                kids = field.get('/Kids', [])
                if kids:
                    extract_fields(kids, collected_fields)
            return collected_fields
        
        fields = extract_fields(reader.trailer['/Root']['/AcroForm'].get('/Fields', []))
        
        # Lists to track field categories
        edit_value_fields = []
        updated_fields = []
        
        # Update fields based on JSON input
        for field in fields:
            field_name = field.get('/T')
            field_type = field.get('/FT')
            field_value = field.get('/V')
            field_flags = field.get('/Ff', 0)
            
            if not field_name:
                continue
                
            # Track fields with "EDIT" in their value
            if field_value and isinstance(field_value, str) and 'edit' in field_value.lower():
                field_type_name = {
                    '/Tx': 'Textbox',
                    '/Btn': 'Checkbox or Radio Button',
                    '/Ch': 'Dropdown or List',
                    '/Sig': 'Signature'
                }.get(field_type, 'Unknown')
                edit_value_fields.append(f"{field_name} ({field_type_name})")
            
            # Update field if it’s in the JSON input and not read-only
            if field_name in field_values and not (field_flags & 1):
                try:
                    new_value = str(field_values[field_name])
                    if new_value is None:
                        continue
                    if field_type == '/Tx':  # Textbox (single-line or multiline)
                        field.update({pypdf.generic.NameObject('/V'): pypdf.generic.TextStringObject(new_value)})
                    elif field_type == '/Btn':  # Checkbox or radio button
                        field.update({pypdf.generic.NameObject('/V'): pypdf.generic.NameObject(new_value)})
                    elif field_type == '/Ch':  # Dropdown or list
                        field.update({pypdf.generic.NameObject('/V'): pypdf.generic.TextStringObject(new_value)})
                    updated_fields.append(field_name)
                    response["messages"].append(f"Updated field '{field_name}' with new value.")
                except Exception as e:
                    response["messages"].append(f"Failed to update field '{field_name}': {str(e)}")
            elif field_name in field_values:
                response["messages"].append(f"Field '{field_name}' is read-only and cannot be updated.")
        
        # Write the modified PDF to a byte stream
        output_stream = BytesIO()
        writer.write(output_stream)
        pdf_bytes = output_stream.getvalue()
        output_stream.close()
        
        # Add field information to response
        response["messages"].append(f"Fields updated: {', '.join(updated_fields) if updated_fields else 'None'}")
        if edit_value_fields:
            response["messages"].append(f"Fields with 'EDIT' in their value: {', '.join(edit_value_fields)}")
        else:
            response["messages"].append("No fields with 'EDIT' in their value found.")
        
        return pdf_bytes, response
    
    except Exception as e:
        response["status"] = "error"
        response["messages"].append(f"Unexpected error: {str(e)}")
        return b"", response