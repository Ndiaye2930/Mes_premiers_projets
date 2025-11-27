from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('gerer/', views.gerer_utilisateurs, name='gerer_utilisateurs'),
    path("export/csv/", views.export_users_csv, name="export_users_csv"),
    path("export/pdf/", views.export_users_pdf, name="export_users_pdf"),
    path('superadmin/', views.dashboard_superadmin, name='dashboard_superadmin'),
    path('agent-ec/', views.dashboard_agent_ec, name='dashboard_agent_ec'),
    path('responsable-admin/', views.dashboard_responsable_admin, name='dashboard_responsable_admin'),
    path('agent-finances/', views.dashboard_agent_finances, name='dashboard_agent_finances'),
    path('chef-service/', views.dashboard_chef_service, name='dashboard_chef_service'),
    path('citoyen/', views.dashboard_citoyen, name='dashboard_citoyen'),
]