#!/usr/bin/env python
import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_system.settings')
django.setup()

from processes.models import Process
from parties.models import Party

def check_data():
    print("=== VERIFICAÇÃO DOS DADOS IMPORTADOS ===")
    
    # Verificar processos
    processes = Process.objects.all()
    print(f"Total de processos: {processes.count()}")
    
    for process in processes:
        print(f"\nProcesso: {process.process_number}")
        print(f"  Classe: {process.process_class}")
        print(f"  Assunto: {process.subject}")
        print(f"  Juiz: {process.judge}")
        print(f"  Partes: {process.parties.count()}")
        
        # Verificar partes
        for party in process.parties.all():
            print(f"    - {party.name} ({party.get_category_display()}) - {party.document}")
    
    # Verificar todas as partes
    parties = Party.objects.all()
    print(f"\nTotal de partes: {parties.count()}")
    
    for party in parties:
        print(f"  {party.name} - {party.get_category_display()} - {party.document}")

if __name__ == "__main__":
    check_data() 