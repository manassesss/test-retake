#!/usr/bin/env python
"""
Script para testar a API do sistema de processos jurídicos com autenticação.
"""
import requests
import json
from getpass import getpass

def test_api_with_auth():
    """Test the API endpoints with authentication."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testando API do Sistema de Processos Jurídicos (com autenticação)")
    print("=" * 60)
    
    # Get credentials
    username = "admin"
    password = "admin123"  # Updated password
    
    # Create session with authentication
    session = requests.Session()
    session.auth = (username, password)
    
    # Test 1: List processes
    print("\n1. 📋 Listando processos...")
    try:
        response = session.get(f"{base_url}/api/processes/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! Encontrados {data['count']} processos")
            for process in data['results']:
                print(f"   - {process['process_number']}: {process['process_class']}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    # Test 2: Get specific process
    print("\n2. 🔍 Detalhes do primeiro processo...")
    try:
        response = session.get(f"{base_url}/api/processes/1/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Processo: {data['process_number']}")
            print(f"   Classe: {data['process_class']}")
            print(f"   Assunto: {data['subject']}")
            print(f"   Juiz: {data['judge']}")
            print(f"   Partes: {data['parties_count']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    # Test 3: List parties
    print("\n3. 👥 Listando partes...")
    try:
        response = session.get(f"{base_url}/api/parties/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! Encontradas {data['count']} partes")
            for party in data['results']:
                print(f"   - {party['name']} ({party['category_display']})")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    # Test 4: Export Excel
    print("\n4. 📊 Testando exportação Excel...")
    try:
        response = session.get(f"{base_url}/api/processes/export_excel/")
        if response.status_code == 200:
            print("✅ Arquivo Excel gerado com sucesso!")
            print(f"   Tamanho: {len(response.content)} bytes")
            print(f"   Tipo: {response.headers.get('Content-Type')}")
            
            # Save the file
            with open("processos_export.xlsx", "wb") as f:
                f.write(response.content)
            print("   💾 Arquivo salvo como 'processos_export.xlsx'")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    # Test 5: Get process parties
    print("\n5. 👥 Partes do primeiro processo...")
    try:
        response = session.get(f"{base_url}/api/processes/1/parties/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Encontradas {len(data)} partes no processo")
            for party in data:
                print(f"   - {party['name']} ({party['category_display']}) - {party['document']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Teste da API concluído!")
    print("\n📋 URLs disponíveis:")
    print(f"   Admin: {base_url}/admin/")
    print(f"   API Processes: {base_url}/api/processes/")
    print(f"   API Parties: {base_url}/api/parties/")
    print(f"   Export Excel: {base_url}/api/processes/export_excel/")

if __name__ == "__main__":
    test_api_with_auth() 