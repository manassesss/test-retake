"""
Tests for processes app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Process
from parties.models import Party, PartyContact


class ProcessModelTest(TestCase):
    """Test cases for Process model."""
    
    def setUp(self):
        """Set up test data."""
        self.process_data = {
            'process_number': '1234567-89.2023.1.02.0001',
            'process_class': 'Execução de Título Extrajudicial',
            'subject': 'Cobrança de dívida',
            'judge': 'Dr. João Silva'
        }
    
    def test_create_process(self):
        """Test creating a process."""
        process = Process.objects.create(**self.process_data)
        self.assertEqual(process.process_number, self.process_data['process_number'])
        self.assertEqual(process.process_class, self.process_data['process_class'])
        self.assertEqual(process.subject, self.process_data['subject'])
        self.assertEqual(process.judge, self.process_data['judge'])
    
    def test_process_str_representation(self):
        """Test string representation of process."""
        process = Process.objects.create(**self.process_data)
        expected = f"{process.process_number} - {process.process_class}"
        self.assertEqual(str(process), expected)
    
    def test_process_parties_count(self):
        """Test parties count property."""
        process = Process.objects.create(**self.process_data)
        self.assertEqual(process.parties_count, 0)
        
        # Add a party
        Party.objects.create(
            process=process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        self.assertEqual(process.parties_count, 1)


class ProcessAPITest(APITestCase):
    """Test cases for Process API."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.process_data = {
            'process_number': '1234567-89.2023.1.02.0001',
            'process_class': 'Execução de Título Extrajudicial',
            'subject': 'Cobrança de dívida',
            'judge': 'Dr. João Silva'
        }
    
    def test_create_process(self):
        """Test creating a process via API."""
        response = self.client.post('/api/processes/', self.process_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Process.objects.count(), 1)
        
        process = Process.objects.first()
        self.assertEqual(process.process_number, self.process_data['process_number'])
    
    def test_list_processes(self):
        """Test listing processes via API."""
        Process.objects.create(**self.process_data)
        
        response = self.client.get('/api/processes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_process_detail(self):
        """Test getting process details via API."""
        process = Process.objects.create(**self.process_data)
        
        response = self.client.get(f'/api/processes/{process.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['process_number'], process.process_number)
    
    def test_update_process(self):
        """Test updating a process via API."""
        process = Process.objects.create(**self.process_data)
        update_data = {'subject': 'Updated subject'}
        
        response = self.client.patch(f'/api/processes/{process.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        process.refresh_from_db()
        self.assertEqual(process.subject, 'Updated subject')
    
    def test_delete_process(self):
        """Test deleting a process via API."""
        process = Process.objects.create(**self.process_data)
        
        response = self.client.delete(f'/api/processes/{process.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Process.objects.count(), 0)
    
    def test_process_parties_endpoint(self):
        """Test getting process parties via API."""
        process = Process.objects.create(**self.process_data)
        party = Party.objects.create(
            process=process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        response = self.client.get(f'/api/processes/{process.id}/parties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], party.name)
    
    def test_export_excel_endpoint(self):
        """Test exporting processes to Excel."""
        Process.objects.create(**self.process_data)
        
        response = self.client.get('/api/processes/export_excel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


class ProcessValidationTest(TestCase):
    """Test cases for process validation."""
    
    def test_process_number_validation(self):
        """Test process number validation."""
        # Valid process number
        process = Process.objects.create(
            process_number='1234567-89.2023.1.02.0001',
            process_class='Test',
            subject='Test',
            judge='Test'
        )
        self.assertIsNotNone(process.id)
        
        # Invalid process number (too short)
        with self.assertRaises(Exception):
            Process.objects.create(
                process_number='123',
                process_class='Test',
                subject='Test',
                judge='Test'
            )


class ProcessScraperTest(TestCase):
    """Test cases for process data extraction."""
    
    def test_extract_process_data(self):
        """Test extracting process data from HTML."""
        from .scrapers import ProcessDataExtractor
        
        html_content = """
        <html>
        <body>
        <h1>Processo Nº 1234567-89.2023.1.02.0001</h1>
        <p>Classe: Execução de Título Extrajudicial</p>
        <p>Assunto: Cobrança de dívida</p>
        <p>Juiz: Dr. João Silva</p>
        <p>EXEQUENTE: João da Silva - CPF: 123.456.789-01</p>
        <p>EXECUTADA: Maria Santos - CNPJ: 12.345.678/0001-90</p>
        </body>
        </html>
        """
        
        extractor = ProcessDataExtractor(html_content)
        data = extractor.extract_all_data()
        
        self.assertEqual(data['process_number'], '1234567-89.2023.1.02.0001')
        self.assertEqual(data['process_class'], 'Execução de Título Extrajudicial')
        self.assertEqual(data['subject'], 'Cobrança de dívida')
        self.assertEqual(data['judge'], 'Dr. João Silva')
        self.assertEqual(len(data['parties']), 2)
        
        # Check parties
        exequente = next(p for p in data['parties'] if p['category'] == 'EXEQUENTE')
        executada = next(p for p in data['parties'] if p['category'] == 'EXECUTADA')
        
        self.assertEqual(exequente['name'], 'João da Silva')
        self.assertEqual(exequente['document'], '123.456.789-01')
        self.assertEqual(executada['name'], 'Maria Santos')
        self.assertEqual(executada['document'], '12.345.678/0001-90')
