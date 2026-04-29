import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from Client.models import Client

def create_test_users():
    """Créer des comptes clients de test"""
    
    # Données des utilisateurs de test
    test_users = [
        {
            'username': 'client1',
            'email': 'client1@example.com',
            'password': 'password123',
            'first_name': 'Ahmed',
            'last_name': 'Mohammed',
            'telephone': '0612345678'
        },
        {
            'username': 'client2',
            'email': 'client2@example.com',
            'password': 'password123',
            'first_name': 'Fatima',
            'last_name': 'Alami',
            'telephone': '0623456789'
        },
        {
            'username': 'client3',
            'email': 'client3@example.com',
            'password': 'password123',
            'first_name': 'Youssef',
            'last_name': 'Bennani',
            'telephone': '0634567890'
        },
        {
            'username': 'client4',
            'email': 'client4@example.com',
            'password': 'password123',
            'first_name': 'Amina',
            'last_name': 'Khalil',
            'telephone': '0645678901'
        },
        {
            'username': 'client5',
            'email': 'client5@example.com',
            'password': 'password123',
            'first_name': 'Omar',
            'last_name': 'Zaki',
            'telephone': '0656789012'
        }
    ]
    
    print("🚀 Création des comptes clients de test...")
    
    for user_data in test_users:
        try:
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=user_data['username']).exists():
                print(f"⚠️  L'utilisateur {user_data['username']} existe déjà")
                continue
            
            # Créer l'utilisateur Django
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Créer le client associé
            client = Client.objects.create(
                nom=user_data['last_name'],
                prenom=user_data['first_name'],
                email=user_data['email'],
                telephone=user_data['telephone'],
                adresse=f"Adresse de {user_data['first_name']} {user_data['last_name']}"
            )
            
            print(f"✅ Compte créé: {user_data['username']} ({user_data['first_name']} {user_data['last_name']})")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de {user_data['username']}: {e}")
    
    print("\n📊 Résumé des comptes créés:")
    print("Utilisateur | Email | Mot de passe")
    print("-" * 40)
    for user_data in test_users:
        print(f"{user_data['username']} | {user_data['email']} | password123")
    
    print(f"\n🎉 Total utilisateurs: {len(test_users)}")
    print("🔗 URL de connexion: http://127.0.0.1:8000/login/")

if __name__ == '__main__':
    create_test_users()
