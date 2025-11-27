from django.urls import path
from .views import AnnonceView
from .views import annonce_publique
from .views import export_archives_pdf


urlpatterns = [
    path("annonces", AnnonceView.as_view(), name="annonces"),
    path("public/<int:id>/", annonce_publique, name="annonce_publique"),
    path("archives/export/pdf/", export_archives_pdf, name="export_archives_pdf"),

]
