import factory
from django.contrib.auth.models import User

class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = 'DRF'
    last_name = 'Test'
    username = 'drftest'
    password = 'drftest'
    is_active = True
    is_superuser = False
    last_login = now()
    date_joined = now()
