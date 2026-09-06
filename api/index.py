import os
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parents[1] / "MyBlogs"
sys.path.insert(0, str(project_dir))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyBlogs.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
