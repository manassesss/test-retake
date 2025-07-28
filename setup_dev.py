#!/usr/bin/env python
"""
Script para configurar o ambiente de desenvolvimento.
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Execute a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ERRO")
        print(f"Comando: {command}")
        print(f"Erro: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Configurando ambiente de desenvolvimento...")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Erro: Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Instalando dependências"):
        sys.exit(1)
    
    # Create migrations
    if not run_command("python manage.py makemigrations", "Criando migrações"):
        sys.exit(1)
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Aplicando migrações"):
        sys.exit(1)
    
    # Create superuser if it doesn't exist
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            if run_command("python manage.py createsuperuser --username admin --email admin@example.com --noinput", "Criando superusuário"):
                print("👤 Superusuário criado: admin/admin")
        else:
            print("👤 Superusuário já existe")
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível verificar/criar superusuário: {e}")
    
    # Create static directory
    if not os.path.exists('static'):
        os.makedirs('static')
        print("📁 Diretório static criado")
    
    # Create media directory
    if not os.path.exists('media'):
        os.makedirs('media')
        print("📁 Diretório media criado")
    
    print("\n🎉 Ambiente configurado com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://localhost:8000/admin/")
    print("3. Login: admin/admin")
    print("4. API: http://localhost:8000/api/")
    
    print("\n🧪 Para executar testes:")
    print("python manage.py test")
    
    print("\n📊 Para importar dados de HTML:")
    print("python manage.py import_processes --file example_process.html")

if __name__ == "__main__":
    main() 