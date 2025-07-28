"""
Script to extract legal process data from HTML files.
"""
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from .models import Process
from parties.models import Party, PartyContact


class ProcessDataExtractor:
    """
    Extract legal process data from HTML files.
    """
    
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
    
    def extract_process_number(self):
        """Extract process number from HTML."""
        # First try to find in h4 elements (common pattern)
        h4_elements = self.soup.find_all('h4')
        for h4 in h4_elements:
            text = h4.get_text().strip()
            # Look for process number pattern
            match = re.search(r'([0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4})', text)
            if match:
                return match.group(1)
        
        # Fallback to text search
        text = self.soup.get_text()
        process_patterns = [
            r'([0-9]{7}-[0-9]{2}\.[0-9]{4}\.[0-9]\.[0-9]{2}\.[0-9]{4})',
            r'([0-9]{20})',
        ]
        
        for pattern in process_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def extract_process_class(self):
        """Extract process class from HTML."""
        # Look for class information in the HTML structure
        class_elements = self.soup.find_all('span')
        for element in class_elements:
            # Check if this element is next to a "Classe:" label
            prev_element = element.find_previous_sibling()
            if prev_element and 'Classe:' in prev_element.get_text():
                return element.get_text().strip()
        
        # Fallback to text search
        text = self.soup.get_text()
        class_patterns = [
            r'Classe\s*:?\s*([^\\n]+)',
            r'Tipo\s*:?\s*([^\\n]+)',
        ]
        
        for pattern in class_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return "Não informado"
    
    def extract_subject(self):
        """Extract process subject from HTML."""
        # Look for subject information in the HTML structure
        subject_elements = self.soup.find_all('span')
        for element in subject_elements:
            # Check if this element is next to an "Assunto:" label
            prev_element = element.find_previous_sibling()
            if prev_element and 'Assunto:' in prev_element.get_text():
                return element.get_text().strip()
        
        # Fallback to text search
        text = self.soup.get_text()
        subject_patterns = [
            r'Assunto\s*:?\s*([^\\n]+)',
            r'Objeto\s*:?\s*([^\\n]+)',
        ]
        
        for pattern in subject_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return "Não informado"
    
    def extract_judge(self):
        """Extract judge name from HTML."""
        # Look for judge information in the HTML structure
        judge_elements = self.soup.find_all('span')
        for element in judge_elements:
            # Check if this element is next to a "Juiz:" label
            prev_element = element.find_previous_sibling()
            if prev_element and 'Juiz:' in prev_element.get_text():
                return element.get_text().strip()
        
        # Fallback to text search
        text = self.soup.get_text()
        judge_patterns = [
            r'Juiz\s*:?\s*([^\\n]+)',
            r'Magistrado\s*:?\s*([^\\n]+)',
            r'Relator\s*:?\s*([^\\n]+)',
        ]
        
        for pattern in judge_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return "Não informado"
    
    def extract_parties(self):
        """Extract parties information from HTML."""
        parties = []
        
        # Look for party patterns in the HTML structure
        party_elements = self.soup.find_all('li', class_='list-group-item')
        
        for element in party_elements:
            # Extract party information from the list item
            party_text = element.get_text()
            
            # Look for party category in badges
            badge = element.find('span', class_='badge')
            if badge:
                category = badge.get_text().strip().upper()
            else:
                category = 'TERCEIRO'
            
            # Extract name and document from the text
            # Remove the badge text from the party text
            if badge:
                party_text = party_text.replace(badge.get_text(), '').strip()
            
            # Look for document pattern in the text
            document = self.extract_document(party_text)
            clean_name = self.clean_party_name(party_text)
            
            if clean_name:
                parties.append({
                    'name': clean_name,
                    'document': document,
                    'category': self.normalize_category(category)
                })
        
        return parties
    
    def extract_document(self, text):
        """Extract document (CPF/CNPJ) from text."""
        # Look for CPF/CNPJ patterns
        doc_patterns = [
            r'CPF\s*:?\s*([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2})',
            r'CNPJ\s*:?\s*([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?[0-9]{4}-?[0-9]{2})',
            r'([0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2})',  # CPF
            r'([0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?[0-9]{4}-?[0-9]{2})',  # CNPJ
        ]
        
        for pattern in doc_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""
    
    def clean_party_name(self, name):
        """Clean party name by removing document and extra information."""
        # Remove document patterns
        name = re.sub(r'CPF\s*:?\s*[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}', '', name)
        name = re.sub(r'CNPJ\s*:?\s*[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?[0-9]{4}-?[0-9]{2}', '', name)
        name = re.sub(r'Documento\s*:?\s*[0-9]{3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9]{2}', '', name)
        name = re.sub(r'Documento\s*:?\s*[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}/?[0-9]{4}-?[0-9]{2}', '', name)
        
        # Remove extra whitespace and clean
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Remove common prefixes/suffixes
        name = re.sub(r'^(EXEQUENTE|EXECUTADA|AUTOR|RÉU|REU|TERCEIRO|REQUERENTE|REQUERIDO)\s*:?\s*', '', name, flags=re.IGNORECASE)
        
        # Remove parentheses and their content
        name = re.sub(r'\([^)]*\)', '', name)
        
        return name if name and len(name.strip()) > 2 else None
    
    def normalize_category(self, category):
        """Normalize party category."""
        category_map = {
            'EXEQUENTE': 'EXEQUENTE',
            'EXECUTADA': 'EXECUTADA',
            'AUTOR': 'AUTOR',
            'RÉU': 'REU',
            'REU': 'REU',
            'REQUERENTE': 'AUTOR',
            'REQUERIDO': 'REU',
            'TERCEIRO': 'TERCEIRO',
        }
        
        return category_map.get(category.upper(), 'TERCEIRO')
    
    def extract_all_data(self):
        """Extract all process data from HTML."""
        return {
            'process_number': self.extract_process_number(),
            'process_class': self.extract_process_class(),
            'subject': self.extract_subject(),
            'judge': self.extract_judge(),
            'parties': self.extract_parties()
        }


def extract_and_save_process(html_content):
    """
    Extract process data from HTML and save to database.
    
    Args:
        html_content (str): HTML content of the process page
        
    Returns:
        Process: The created process object or None if failed
    """
    try:
        extractor = ProcessDataExtractor(html_content)
        data = extractor.extract_all_data()
        
        if not data['process_number']:
            print("Could not extract process number from HTML")
            return None
        
        # Check if process already exists
        process, created = Process.objects.get_or_create(
            process_number=data['process_number'],
            defaults={
                'process_class': data['process_class'],
                'subject': data['subject'],
                'judge': data['judge']
            }
        )
        
        if created:
            print(f"Created new process: {process.process_number}")
        else:
            print(f"Process already exists: {process.process_number}")
        
        # Create parties
        for party_data in data['parties']:
            if party_data['name']:
                party, party_created = Party.objects.get_or_create(
                    process=process,
                    name=party_data['name'],
                    document=party_data['document'],
                    defaults={'category': party_data['category']}
                )
                
                if party_created:
                    print(f"  Created party: {party.name} ({party.get_category_display()})")
        
        return process
        
    except Exception as e:
        print(f"Error extracting process data: {e}")
        return None 