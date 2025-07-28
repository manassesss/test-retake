"""
Tests for parties app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from processes.models import Process
from .models import Party, PartyContact


class PartyModelTest(TestCase):
    """Test cases for Party model."""
    
    def setUp(self):
        """Set up test data."""
        self.process = Process.objects.create(
            process_number='1234567-89.2023.1.02.0001',
            process_class='Execução de Título Extrajudicial',
            subject='Cobrança de dívida',
            judge='Dr. João Silva'
        )
        
        self.party_data = {
            'process': self.process,
            'name': 'João da Silva',
            'document': '12345678901',
            'category': 'EXEQUENTE'
        }
    
    def test_create_party(self):
        """Test creating a party."""
        party = Party.objects.create(**self.party_data)
        self.assertEqual(party.name, self.party_data['name'])
        self.assertEqual(party.document, self.party_data['document'])
        self.assertEqual(party.category, self.party_data['category'])
        self.assertEqual(party.process, self.process)
    
    def test_party_str_representation(self):
        """Test string representation of party."""
        party = Party.objects.create(**self.party_data)
        expected = f"{party.name} ({party.get_category_display()})"
        self.assertEqual(str(party), expected)
    
    def test_party_unique_constraint(self):
        """Test unique constraint for party."""
        Party.objects.create(**self.party_data)
        
        # Try to create another party with same process, name and document
        with self.assertRaises(Exception):
            Party.objects.create(**self.party_data)


class PartyContactModelTest(TestCase):
    """Test cases for PartyContact model."""
    
    def setUp(self):
        """Set up test data."""
        self.process = Process.objects.create(
            process_number='1234567-89.2023.1.02.0001',
            process_class='Test',
            subject='Test',
            judge='Test'
        )
        
        self.party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
    
    def test_create_email_contact(self):
        """Test creating an email contact."""
        contact = PartyContact.objects.create(
            party=self.party,
            contact_type='EMAIL',
            value='joao@example.com',
            is_primary=True
        )
        
        self.assertEqual(contact.contact_type, 'EMAIL')
        self.assertEqual(contact.value, 'joao@example.com')
        self.assertTrue(contact.is_primary)
    
    def test_create_phone_contact(self):
        """Test creating a phone contact."""
        contact = PartyContact.objects.create(
            party=self.party,
            contact_type='PHONE',
            value='(11) 99999-9999',
            is_primary=False
        )
        
        self.assertEqual(contact.contact_type, 'PHONE')
        self.assertEqual(contact.value, '(11) 99999-9999')
        self.assertFalse(contact.is_primary)
    
    def test_contact_str_representation(self):
        """Test string representation of contact."""
        contact = PartyContact.objects.create(
            party=self.party,
            contact_type='EMAIL',
            value='joao@example.com'
        )
        
        expected = f"{self.party.name} - Email: joao@example.com"
        self.assertEqual(str(contact), expected)


class PartyAPITest(APITestCase):
    """Test cases for Party API."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.process = Process.objects.create(
            process_number='1234567-89.2023.1.02.0001',
            process_class='Test',
            subject='Test',
            judge='Test'
        )
        
        self.party_data = {
            'process': self.process.id,
            'name': 'João da Silva',
            'document': '12345678901',
            'category': 'EXEQUENTE'
        }
    
    def test_create_party(self):
        """Test creating a party via API."""
        response = self.client.post('/api/parties/', self.party_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Party.objects.count(), 1)
        
        party = Party.objects.first()
        self.assertEqual(party.name, self.party_data['name'])
    
    def test_list_parties(self):
        """Test listing parties via API."""
        Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        response = self.client.get('/api/parties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_party_detail(self):
        """Test getting party details via API."""
        party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        response = self.client.get(f'/api/parties/{party.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], party.name)
    
    def test_update_party(self):
        """Test updating a party via API."""
        party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        update_data = {'name': 'João Silva Santos'}
        response = self.client.patch(f'/api/parties/{party.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        party.refresh_from_db()
        self.assertEqual(party.name, 'João Silva Santos')
    
    def test_delete_party(self):
        """Test deleting a party via API."""
        party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        response = self.client.delete(f'/api/parties/{party.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Party.objects.count(), 0)
    
    def test_party_contacts_endpoint(self):
        """Test getting party contacts via API."""
        party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        contact = PartyContact.objects.create(
            party=party,
            contact_type='EMAIL',
            value='joao@example.com'
        )
        
        response = self.client.get(f'/api/parties/{party.id}/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['value'], contact.value)
    
    def test_add_contact_to_party(self):
        """Test adding contact to party via API."""
        party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        
        contact_data = {
            'contact_type': 'EMAIL',
            'value': 'joao@example.com',
            'is_primary': True
        }
        
        response = self.client.post(f'/api/parties/{party.id}/add_contact/', contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PartyContact.objects.count(), 1)


class PartyContactAPITest(APITestCase):
    """Test cases for PartyContact API."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.process = Process.objects.create(
            process_number='1234567-89.2023.1.02.0001',
            process_class='Test',
            subject='Test',
            judge='Test'
        )
        
        self.party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
    
    def test_create_contact(self):
        """Test creating a contact via API."""
        contact_data = {
            'party': self.party.id,
            'contact_type': 'EMAIL',
            'value': 'joao@example.com',
            'is_primary': True
        }
        
        response = self.client.post('/api/party-contacts/', contact_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PartyContact.objects.count(), 1)
    
    def test_list_contacts(self):
        """Test listing contacts via API."""
        PartyContact.objects.create(
            party=self.party,
            contact_type='EMAIL',
            value='joao@example.com'
        )
        
        response = self.client.get('/api/party-contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_emails_endpoint(self):
        """Test getting email contacts via API."""
        PartyContact.objects.create(
            party=self.party,
            contact_type='EMAIL',
            value='joao@example.com'
        )
        
        PartyContact.objects.create(
            party=self.party,
            contact_type='PHONE',
            value='(11) 99999-9999'
        )
        
        response = self.client.get('/api/party-contacts/emails/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['contact_type'], 'EMAIL')
    
    def test_phones_endpoint(self):
        """Test getting phone contacts via API."""
        PartyContact.objects.create(
            party=self.party,
            contact_type='EMAIL',
            value='joao@example.com'
        )
        
        PartyContact.objects.create(
            party=self.party,
            contact_type='PHONE',
            value='(11) 99999-9999'
        )
        
        response = self.client.get('/api/party-contacts/phones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['contact_type'], 'PHONE')


class PartyValidationTest(TestCase):
    """Test cases for party validation."""
    
    def setUp(self):
        """Set up test data."""
        self.process = Process.objects.create(
            process_number='1234567-89.2023.1.02.0001',
            process_class='Test',
            subject='Test',
            judge='Test'
        )
    
    def test_valid_cpf_document(self):
        """Test valid CPF document."""
        party = Party.objects.create(
            process=self.process,
            name='João da Silva',
            document='12345678901',
            category='EXEQUENTE'
        )
        self.assertIsNotNone(party.id)
    
    def test_valid_cnpj_document(self):
        """Test valid CNPJ document."""
        party = Party.objects.create(
            process=self.process,
            name='Empresa LTDA',
            document='12345678000190',
            category='EXECUTADA'
        )
        self.assertIsNotNone(party.id)
    
    def test_invalid_document_length(self):
        """Test invalid document length."""
        with self.assertRaises(Exception):
            Party.objects.create(
                process=self.process,
                name='João da Silva',
                document='123456789',  # Too short
                category='EXEQUENTE'
            )
