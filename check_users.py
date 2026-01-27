#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/manibharadwaj/Developer/compnay/cloned/politics/politics_backend')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'politics_backend.politics_backend.settings')

# Setup Django
django.setup()

from users.models import User

print('Users in database:')
for u in User.objects.all():
    print(f'ID: {u.id}, Email: {u.email}, Fullname: {u.fullname}, Role: {u.role}, Approved: {u.is_approved}, User: {u.is_user}, Superuser: {u.is_superuser}')