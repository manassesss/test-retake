#!/usr/bin/env python
"""
Script para definir a senha do usuário admin.
"""
import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_system.settings')
django.setup()

from django.contrib.auth.models import User

def set_admin_password():
    """Set admin password."""
    try:
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Set password
        admin_user.set_password('admin123')
        admin_user.save()
        
        print("✅ Senha do usuário 'admin' definida como 'admin123'")
        print("👤 Credenciais: admin/admin123")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    set_admin_password() 