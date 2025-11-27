from django.urls import path
from . import views

urlpatterns = [

    # 📌 LISTE + CRUD (dans la même vue)
    path(
        "naissance/",
        views.actes_naissance,
        name="actes_naissance"
    ),

    # 📌 Validation d’un acte
    path(
        "naissance/valider/<int:id>/",
        views.valider_acte,
        name="valider_acte"
    ),

    # 📌 Export CSV
    path(
        "naissance/export/csv/",
        views.export_naissance_csv,
        name="export_naissance_csv"
    ),

    # 📌 Génération PDF
    path(
        "naissance/pdf/<int:id>/",
        views.acte_naissance_pdf,
        name="acte_naissance_pdf"
    ),
]
from django.urls import path
from . import views

urlpatterns = [

    # 📌 LISTE + CRUD (dans la même vue)
    path(
        "naissance/",
        views.actes_naissance,
        name="actes_naissance"
    ),

    # 📌 Validation d’un acte
    path(
        "naissance/valider/<int:id>/",
        views.valider_acte,
        name="valider_acte"
    ),

    # 📌 Export CSV
    path(
        "naissance/export/csv/",
        views.export_naissance_csv,
        name="export_naissance_csv"
    ),

    # 📌 Génération PDF
    path(
        "naissance/pdf/<int:id>/",
        views.acte_naissance_pdf,
        name="acte_naissance_pdf"
    ),
    path("parametres/", views.parametres_mairie, name="parametres_mairie"),

    path("mariage/", views.actes_mariage, name="actes_mariage"),
    path("mariage/valider/<int:id>/", views.valider_mariage, name="valider_mariage"),
    path("mariage/export/csv/", views.export_mariage_csv, name="export_mariage_csv"),
    path("mariage/pdf/<int:id>/", views.acte_mariage_pdf, name="acte_mariage_pdf"),
    path("mariage/export/pdf/", views.export_mariage_pdf_list, name="export_mariage_pdf_list"),
    path("mariage/verify/<int:id>/", views.verify_mariage, name="verify_mariage"),
    path("deces/", views.actes_deces, name="actes_deces"),
    path("deces/valider/<int:id>/", views.valider_deces, name="valider_deces"),
    path("deces/export/csv/", views.export_deces_csv, name="export_deces_csv"),
    path("deces/pdf/<int:id>/", views.acte_deces_pdf, name="acte_deces_pdf"),
    path("deces/export/pdf/", views.export_deces_pdf_list, name="export_deces_pdf_list"),
    path("deces/verify/<int:id>/", views.verify_deces, name="verify_deces"),
    path("certificats/", views.certificats_list, name="certificats_list"),
    path("certificats/valider/<int:id>/", views.valider_certificat, name="valider_certificat"),
    path("certificats/pdf/<int:id>/", views.certificat_pdf, name="certificat_pdf"),
    path("certificats/export/pdf/", views.export_certificats_pdf_list, name="export_certificats_pdf_list"),
    path("certificats/export/csv/", views.export_certificats_csv, name="export_certificats_csv"),
    path("certificats/verify/<int:id>/", views.verify_certificat, name="verify_certificat"),
    path("registres/", views.registres_list, name="registres_list"),
    path("registres/export/csv/", views.registres_csv, name="registres_csv"),
    path("registres/export/pdf/", views.registres_pdf, name="registres_pdf"),
    path("verification/", views.verification_publique, name="verification_publique"),

]
