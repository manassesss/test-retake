#!/usr/bin/env python
"""
Script para testar a API do sistema de processos jurídicos.
"""
import requests
import json
from getpass import getpass

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testando API do Sistema de Processos Jurídicos")
    print("=" * 50)
    
    # Test 1: List processes
    print("\n1. 📋 Listando processos...")
    try:
        response = requests.get(f"{base_url}/api/processes/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! Encontrados {data['count']} processos")
            for process in data['results']:
                print(f"   - {process['process_number']}: {process['process_class']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    # Test 2: Get specific process
    print("\n2. 🔍 Detalhes do primeiro processo...")
    try:
        response = requests.get(f"{base_url}/api/processes/1/")
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
        response = requests.get(f"{base_url}/api/parties/")
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
        response = requests.get(f"{base_url}/api/processes/export_excel/")
        if response.status_code == 200:
            print("✅ Arquivo Excel gerado com sucesso!")
            print(f"   Tamanho: {len(response.content)} bytes")
            print(f"   Tipo: {response.headers.get('Content-Type')}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Teste da API concluído!")
    print("\n📋 URLs disponíveis:")
    print(f"   Admin: {base_url}/admin/")
    print(f"   API Processes: {base_url}/api/processes/")
    print(f"   API Parties: {base_url}/api/parties/")
    print(f"   Export Excel: {base_url}/api/processes/export_excel/")

if __name__ == "__main__":
    test_api() 