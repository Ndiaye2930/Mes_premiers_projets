from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users import views  # <-- Correct import des fonctions depuis users/views.py

urlpatterns = [
    path('', views.home_view, name='home'),  # <-- page d'accueil
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', include('users.urls')),
    path('etatcivil/', include('etat_civil.urls')),
    path("annonces/", include("annonces.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
