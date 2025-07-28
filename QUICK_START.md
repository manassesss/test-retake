# 🚀 Guia Rápido - Sistema de Processos Jurídicos

## ⚡ Início Rápido (5 minutos)

### 1. Clone e Configure
```bash
git clone <repository-url>
cd test-retake
python setup_dev.py
```

### 2. Execute o Servidor
```bash
python manage.py runserver
```

### 3. Acesse o Sistema
- **Admin**: http://localhost:8000/admin/
- **Credenciais**: admin/admin123

### 4. Importe Dados de Exemplo
```bash
python manage.py import_processes --file processo-01.html
python manage.py import_processes --file processo-02.html
```

### 5. Teste a API
```bash
python test_api_auth.py
```

## 🎯 URLs Principais

| Funcionalidade | URL | Credenciais |
|---|---|---|
| Admin Interface | http://localhost:8000/admin/ | admin/admin123 |
| API Processos | http://localhost:8000/api/processes/ | admin/admin123 |
| API Partes | http://localhost:8000/api/parties/ | admin/admin123 |
| Export Excel | http://localhost:8000/api/processes/export_excel/ | admin/admin123 |

## 📋 Comandos Essenciais

```bash
# Configuração inicial
python setup_dev.py

# Executar servidor
python manage.py runserver

# Importar dados
python manage.py import_processes --file processo-01.html

# Verificar dados
python check_data.py

# Testar API
python test_api_auth.py

# Executar testes
python manage.py test
```

## 🔧 Solução de Problemas

### Erro de Dependências
```bash
pip install -r requirements.txt
```

### Erro de Banco de Dados
```bash
python manage.py migrate
```

### Erro de Autenticação
```bash
python set_admin_password.py
```

### Erro de Arquivos Estáticos
```bash
mkdir static media
```

## 📊 Dados de Exemplo

Após importar os arquivos de teste, você terá:

- **2 Processos** com dados completos
- **4 Partes** com documentos e categorias
- **Dados reais** extraídos dos HTMLs

## 🎉 Pronto!

O sistema está funcionando e pronto para uso! 🚀 