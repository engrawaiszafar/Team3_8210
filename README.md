# Django Project - Team3_8210

A Django web application with routing and template rendering capabilities.

## Project Overview

This is a Django 6.0.3 project with the following features implemented:
- ✅ Django setup and configuration
- ✅ App creation (`main` app)
- ✅ URL routing
- ✅ Template rendering

## Project Structure

```
Team3_8210/
├── core/                 # Main project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing configuration
│   ├── asgi.py          # ASGI configuration
│   └── wsgi.py          # WSGI configuration
├── main/                # Main application
│   ├── templates/       # HTML templates
│   │   └── home.html
│   ├── views.py         # View functions
│   ├── models.py        # Database models
│   ├── urls.py          # App-specific URLs
│   └── admin.py         # Admin configuration
├── venv/                # Virtual environment
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
└── README.md            # This file
```

## Installation & Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd Team3_8210
```

### 2. Activate Virtual Environment
```bash
# On Windows (Git Bash)
source venv/Scripts/activate

# Or on Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install django
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Available Routes

| Route | View | Description |
|-------|------|-------------|
| `/` | `home` | Home page |
| `/admin/` | Django Admin | Admin interface |

## Views

### Home View
Located in `main/views.py`:
```python
def home(request):
    return render(request, 'home.html')
```

Renders the `home.html` template.

## Templates

Templates are stored in `main/templates/`:
- `home.html` - Home page template

## Development

### Create a Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### Make Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run Tests
```bash
python manage.py test
```

## Configuration

Key settings in `core/settings.py`:
- **DEBUG**: Currently set to `True` for development
- **INSTALLED_APPS**: Includes `main` application
- **DATABASE**: SQLite (default)
- **TEMPLATES**: Configured to use Django template engine

## 🌐 Deployment (PythonAnywhere)

### 1. Clone Repository
```bash
git clone <repository-url>
cd Team3_8210
```

### 2. Create & Activate Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

### 6. Configure Web App

In PythonAnywhere **Web** tab, set:

**Source Code:**
```
/home/arunreddyy/Team3_8210
```

**WSGI Configuration File:**
```python
import os
import sys

path = '/home/arunreddyy/Team3_8210'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 7. Static & Media File Mapping

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/arunreddyy/Team3_8210/staticfiles` |
| `/media/` | `/home/arunreddyy/Team3_8210/media` |

### 8. Update Django Settings

In `core/settings.py`, ensure these settings are configured:

```python
ALLOWED_HOSTS = ['arunreddyy.pythonanywhere.com']

CSRF_TRUSTED_ORIGINS = ['https://arunreddyy.pythonanywhere.com']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 9. Reload Web App

👉 Go to **Web** tab → Click **Reload**

### 🌍 Live URL
```
https://arunreddyy.pythonanywhere.com/admin-login/
```

## Next Steps

Consider implementing:
- [ ] Additional views and templates
- [ ] Models and database schema
- [ ] User authentication
- [ ] Form handling
- [ ] Static files (CSS, JavaScript)
- [ ] Production deployment configuration

## Troubleshooting

### Django Command Not Found
If you encounter "No module named django":
```bash
pip install django
```

### Virtual Environment Not Activated
Ensure you're in the virtual environment before running Django commands. Check if `(venv)` appears in your terminal prompt.

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)

## License

[Add your license here]

## Version

- Django: 6.0.3
- Python: 3.12.6
