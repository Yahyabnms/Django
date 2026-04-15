from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import reverse


class AdminAccessMiddleware:
    """Middleware pour protéger l'accès à la page admin aux superusers uniquement."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Vérifier si l'utilisateur accède à /admin/
        if request.path.startswith('/admin/'):
            # Si l'utilisateur n'est pas authentifié, le rediriger vers la connexion
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Si l'utilisateur n'est pas superuser, refuser l'accès
            if not request.user.is_superuser:
                return HttpResponseForbidden("""
                    <!DOCTYPE html>
                    <html lang="fr">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>Accès Refusé</title>
                        <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                        <style>
                            body {
                                background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                                min-height: 100vh;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            }
                            .error-container {
                                background: white;
                                border-radius: 15px;
                                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                                padding: 60px 40px;
                                max-width: 500px;
                                text-align: center;
                            }
                            .error-icon {
                                background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                                width: 80px;
                                height: 80px;
                                border-radius: 50%;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                margin: 0 auto 20px;
                            }
                            .error-icon i {
                                font-size: 2.5rem;
                                color: white;
                            }
                            h1 {
                                color: #1f2937;
                                font-weight: bold;
                                margin-bottom: 15px;
                            }
                            p {
                                color: #6b7280;
                                margin-bottom: 30px;
                            }
                            .btn {
                                padding: 12px 30px;
                                border-radius: 8px;
                                font-weight: 600;
                                transition: all 0.3s ease;
                            }
                            .btn-primary {
                                background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
                                border: none;
                                color: white;
                            }
                            .btn-primary:hover {
                                transform: translateY(-2px);
                                box-shadow: 0 10px 25px rgba(37, 99, 235, 0.3);
                                color: white;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="error-container">
                            <div class="error-icon">
                                <i class="fas fa-lock"></i>
                            </div>
                            <h1>Accès Refusé</h1>
                            <p>Désolé, vous n'avez pas les permissions nécessaires pour accéder à cette page.</p>
                            <p style="color: #9ca3af;">Seuls les superadministrateurs peuvent accéder à la page d'administration.</p>
                            <a href="/" class="btn btn-primary">
                                <i class="fas fa-home"></i> Retour à l'accueil
                            </a>
                        </div>
                    </body>
                    </html>
                """)
        
        response = self.get_response(request)
        return response
