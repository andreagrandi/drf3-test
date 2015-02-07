from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from shop.tests.factories import ProductFactory
from shop.models import Product

class Command(BaseCommand):
    args = ''
    help = ('Initialize an empty DB creating a User, setting a specific token, creating two'
            'products (a Widget and a Gizmo).')

    def handle(self, *args, **options):
        # Create the default User
        if User.objects.count() == 0:
            user = User.objects.create_user(username='andrea',
                email='email@isp.com', password='andreatest')
            user.save()
        else:
            user = User.objects.get(id=1)

        if Token.objects.count() == 0:
            # Generate the token for the created user
            Token.objects.create(user=user)

        # Change the Token to a known one
        Token.objects.filter(user_id=user.id).update(key='b60868c38b813ea43b36036503e3f5de025dde31')

        if Product.objects.count() == 0:
            # Create a Widget and a Gizmo products on DB
            ProductFactory.create(name='Widget', collect_stamp=True)
            ProductFactory.create(name='Gizmo', collect_stamp=False)
