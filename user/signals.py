import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def log_error(response):
    print(f"Error: {response.status_code} - {response.text}")

def create_directory_if_not_exists(path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Authorization': f'OAuth {settings.YANDEX_DISK_TOKEN}',
    }
    params = {'path': path}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 404:
        # Директория не существует, создаем ее
        response = requests.put(url, headers=headers, params=params)
        if response.status_code != 201:  # Проверяем, что директория была создана
            log_error(response)

def copy_file(source_path, destination_path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/copy'
    headers = {
        'Authorization': f'OAuth {settings.YANDEX_DISK_TOKEN}',
    }
    params = {
        'from': source_path,
        'path': destination_path,
        'overwrite': 'true'  # Установлено в 'true' для перезаписи
    }
    response = requests.post(url, headers=headers, params=params)
    if response.status_code != 202:  # Проверяем, что файл был скопирован
        log_error(response)

@receiver(post_save, sender=User)
def create_user_directory_and_files(sender, instance, created, **kwargs):
    if created:
        user_dir = f'/{instance.username}/'
        
        # Создание директории пользователя, если она не существует
        create_directory_if_not_exists(user_dir)
        
        # Копирование файлов из корневой директории в директорию пользователя
        copy_file('/Instance.xlsx', f'{user_dir}svodnaya_tablica_ostatkov_tovarov.xlsx')
        copy_file('/Instance.txt', f'{user_dir}Доступы.txt')