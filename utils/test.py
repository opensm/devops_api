from django.contrib.auth.models import User
for x in  User._meta.get_fields():
    if hasattr(x,'m2m_column_name'):
        print(x.m2m_column_name)
    else:
        continue