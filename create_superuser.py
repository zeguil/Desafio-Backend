import os
from time import sleep
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    sleep(3)
    if not User.objects.filter(username='user').exists():
        User.objects.create_superuser('user', 'user@exemplo.com', '1234')
        print("\n##################")
        print('Superuser Criado!')
        print('Usuário: user')
        print('Senha: 1234')
        print("##################\n")


if __name__ == '__main__':
    create_superuser()
