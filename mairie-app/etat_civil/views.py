from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import get_template
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
from io import BytesIO
import csv
import qrcode
import base64
import io

from .forms import (
    ActeNaissanceForm,
    ActeMariageForm,
    ActeDecesForm,
    CertificatForm,
    ParametreMairieForm
)
from .models import (
    ActeNaissance,
    ActeMariage,
    ActeDeces,
    Certificat,
    HistoriqueEtatCivil,
    HistoriqueVerification,
    ParametreMairie,
    Registre
)
from .utils import envoyer_email, envoyer_sms


@login_required
def parametres_mairie(request):
    parametre = ParametreMairie.objects.first()
    
    if request.method == "POST":
        form = ParametreMairieForm(request.POST, request.FILES, instance=parametre)
        if form.is_valid():
            form.save()
            return redirect("parametres_mairie")
    else:
        form = ParametreMairieForm(instance=parametre)
    
    return render(request, "etatcivil/parametres.html", {"form": form, "parametre": parametre})


@login_required
def actes_deces(request):
    search = request.GET.get("search", "")
    qs = ActeDeces.objects.all()
    if search:
        qs = qs.filter(nom__icontains=search) | qs.filter(prenom__icontains=search) | qs.filter(numero__icontains=search)

    paginator = Paginator(qs.order_by("-created_at"), 10)
    page = request.GET.get("page")
    actes = paginator.get_page(page)

    form = ActeDecesForm()

    # Create
    if request.method == "POST" and "create" in request.POST:
        form = ActeDecesForm(request.POST)
        if form.is_valid():
            acte = form.save(commit=False)
            acte.created_by = request.user
            acte.save()
            HistoriqueEtatCivil.objects.create(
                acte_type="deces", acte_id=acte.id, action="Création", user=request.user
            )
            return redirect("actes_deces")

    # Edit
    if request.method == "POST" and "edit" in request.POST:
        acte = get_object_or_404(ActeDeces, id=request.POST.get("acte_id"))
        form_edit = ActeDecesForm(request.POST, instance=acte)
        if form_edit.is_valid():
            form_edit.save()
            HistoriqueEtatCivil.objects.create(
                acte_type="deces", acte_id=acte.id, action="Modification", user=request.user
            )
            return redirect("actes_deces")

    # AJAX Delete
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest" and request.POST.get("action") == "delete":
        try:
            acte = ActeDeces.objects.get(id=request.POST.get("id"))
            HistoriqueEtatCivil.objects.create(
                acte_type="deces", acte_id=acte.id, action="Suppression", user=request.user
            )
            acte.delete()
            return JsonResponse({"status": "success"})
        except ActeDeces.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Introuvable"}, status=404)

    return render(request, "etatcivil/deces_list.html", {
        "actes": actes,
        "form": form,
        "search": search,
    })


@login_required
def valider_deces(request, id):
    # rôle validation : chef de service ou superadmin
    if not (request.user.role in ("chef_service", "superadmin")):
        return redirect("actes_deces")
    acte = get_object_or_404(ActeDeces, id=id)
    acte.statut = "Validé"
    acte.validated_by = request.user
    acte.save()
    HistoriqueEtatCivil.objects.create(
        acte_type="deces", acte_id=acte.id, action="Validation", user=request.user
    )
    return redirect("actes_deces")


@login_required
def export_deces_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actes_deces.csv"'
    writer = csv.writer(response)
    writer.writerow(["N°", "Année", "Nom", "Prénom", "Sexe", "Date", "Lieu", "Cause", "Statut"])
    for a in ActeDeces.objects.order_by("annee", "numero"):
        writer.writerow([
            a.numero, a.annee, a.nom, a.prenom, a.sexe,
            a.date_deces, a.lieu_deces, a.cause_deces, a.statut
        ])
    return response


@login_required
def acte_deces_pdf(request, id):
    acte = get_object_or_404(ActeDeces, id=id)

    # Générer QR (url de vérification)
    verify_url = request.build_absolute_uri(reverse("verify_deces", args=[acte.id]))
    qr_img = qrcode.make(verify_url)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_bytes = qr_buffer.getvalue()

    # Sauvegarde QR dans le modèle
    acte.qr_code.save(f"qr_deces_{acte.id}.png", ContentFile(qr_bytes), save=False)

    # base64 pour le PDF
    qr_b64 = base64.b64encode(qr_bytes).decode()

    # Générer HTML
    template = get_template("etatcivil/pdf_deces.html")
    html = template.render({"acte": acte, "qr_b64": qr_b64})

    # Générer PDF en mémoire
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse("Erreur génération PDF", status=500)
    pdf_bytes = pdf_buffer.getvalue()

    # Sauvegarder PDF dans le modèle
    acte.pdf.save(f"acte_deces_{acte.id}.pdf", ContentFile(pdf_bytes), save=True)

    # Retourner PDF au client
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="acte_deces_{acte.numero}.pdf"'
    return response


@login_required
def export_deces_pdf_list(request):
    actes = ActeDeces.objects.all()
    template = get_template("etat_civil/pdf_deces_list.html")
    html = template.render({"actes": actes})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="actes_deces_list.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erreur génération PDF", status=500)
    return response


@login_required
def verify_deces(request, id):
    acte = get_object_or_404(ActeDeces, id=id)
    return render(request, "etatcivil/verify_deces.html", {"acte": acte})


@login_required
def actes_mariage(request):
    search = request.GET.get("search", "")
    qs = ActeMariage.objects.all()
    if search:
        qs = qs.filter(
            epoux_nom__icontains=search
        ) | qs.filter(epouse_nom__icontains=search) | qs.filter(numero__icontains=search)

    paginator = Paginator(qs.order_by("-created_at"), 10)
    page = request.GET.get("page")
    actes = paginator.get_page(page)

    form = ActeMariageForm()

    # Create
    if request.method == "POST" and "create" in request.POST:
        form = ActeMariageForm(request.POST)
        if form.is_valid():
            acte = form.save(commit=False)
            acte.created_by = request.user
            acte.save()
            # historique
            HistoriqueEtatCivil.objects.create(
                acte_type="mariage", acte_id=acte.id, action="Création", user=request.user
            )
            return redirect("actes_mariage")

    # Edit
    if request.method == "POST" and "edit" in request.POST:
        acte = get_object_or_404(ActeMariage, id=request.POST.get("acte_id"))
        form_edit = ActeMariageForm(request.POST, instance=acte)
        if form_edit.is_valid():
            form_edit.save()
            HistoriqueEtatCivil.objects.create(
                acte_type="mariage", acte_id=acte.id, action="Modification", user=request.user
            )
            return redirect("actes_mariage")

    # AJAX Delete
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest" and request.POST.get("action") == "delete":
        try:
            acte = ActeMariage.objects.get(id=request.POST.get("id"))
            HistoriqueEtatCivil.objects.create(
                acte_type="mariage", acte_id=acte.id, action="Suppression", user=request.user
            )
            acte.delete()
            return JsonResponse({"status": "success"})
        except ActeMariage.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Introuvable"}, status=404)

    return render(request, "etatcivil/mariage_list.html", {
        "actes": actes,
        "form": form,
        "search": search,
    })


@login_required
def valider_mariage(request, id):
    acte = get_object_or_404(ActeMariage, id=id)
    acte.statut = "Validé"
    acte.validated_by = request.user
    acte.save()
    HistoriqueEtatCivil.objects.create(
        acte_type="mariage", acte_id=acte.id, action="Validation", user=request.user
    )
    return redirect("actes_mariage")


@login_required
def export_mariage_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actes_mariage.csv"'
    writer = csv.writer(response)
    writer.writerow(["N°", "Année", "Epoux", "Epouse", "Date", "Lieu", "Statut"])
    for a in ActeMariage.objects.order_by("annee", "numero"):
        writer.writerow([
            a.numero, a.annee,
            f"{a.epoux_nom} {a.epoux_prenom}",
            f"{a.epouse_nom} {a.epouse_prenom}",
            a.date_mariage, a.lieu_mariage, a.statut
        ])
    return response


@login_required
def acte_mariage_pdf(request, id):
    acte = get_object_or_404(ActeMariage, id=id)

    # 1) Génération du QR Code
    verify_url = request.build_absolute_uri(reverse("verify_mariage", args=[acte.id]))
    qr_img = qrcode.make(verify_url)

    # Convertir QR en bytes pour le sauvegarder
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_bytes = qr_buffer.getvalue()

    # Sauvegarde QR dans le modèle si vide ou régénération forcée
    acte.qr_code.save(f"qr_mariage_{acte.id}.png", ContentFile(qr_bytes), save=False)

    # Base64 pour le PDF
    qr_b64 = base64.b64encode(qr_bytes).decode()

    # 2) Génération HTML
    template = get_template("etatcivil/pdf_mariage.html")
    html = template.render({"acte": acte, "qr_b64": qr_b64})

    # 3) Génération PDF en bytes pour sauvegarde
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse("Erreur génération PDF", status=500)

    pdf_bytes = pdf_buffer.getvalue()

    # Sauvegarde PDF dans le modèle
    acte.pdf.save(f"acte_mariage_{acte.id}.pdf", ContentFile(pdf_bytes), save=True)

    # 4) Envoi du PDF au client
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="acte_mariage_{acte.numero}.pdf"'
    return response


@login_required
def export_mariage_pdf_list(request):
    # Liste complète en PDF (ex: tableau)
    actes = ActeMariage.objects.all()
    template = get_template("etat_civil/pdf_mariage_list.html")
    html = template.render({"actes": actes})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="actes_mariage_list.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erreur génération PDF", status=500)
    return response


@login_required
def verify_mariage(request, id):
    # Page publique qui montre info sommaire et statut (utilisée par QR)
    acte = get_object_or_404(ActeMariage, id=id)
    return render(request, "etatcivil/verify_mariage.html", {"acte": acte})


def generate_qr(data):
    qr = qrcode.make(data)
    blob = BytesIO()
    qr.save(blob, format='PNG')
    return blob.getvalue()


@login_required
def actes_naissance(request):
    search = request.GET.get("search", "")
    actes = ActeNaissance.objects.filter(
        nom__icontains=search
    ) | ActeNaissance.objects.filter(
        prenom__icontains=search
    ) | ActeNaissance.objects.filter(
        numero__icontains=search
    )

    paginator = Paginator(actes, 10)
    page = request.GET.get("page")
    actes = paginator.get_page(page)

    form = ActeNaissanceForm()

    # ➤ Create
    if request.method == "POST" and "create" in request.POST:
        form = ActeNaissanceForm(request.POST)
        if form.is_valid():
            acte = form.save(commit=False)
            acte.created_by = request.user
            acte.save()
            return redirect("actes_naissance")

    # ➤ Edit
    if request.method == "POST" and "edit" in request.POST:
        acte = get_object_or_404(ActeNaissance, id=request.POST.get("acte_id"))
        form_edit = ActeNaissanceForm(request.POST, instance=acte)
        if form_edit.is_valid():
            form_edit.save()
            return redirect("actes_naissance")

    # ➤ Delete (AJAX)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        acte = ActeNaissance.objects.get(id=request.POST.get("id"))
        acte.delete()
        return JsonResponse({"status": "success"})

    return render(request, "etatcivil/naissance_list.html", {
        "actes": actes,
        "form": form,
        "search": search,
    })


@login_required
def valider_acte(request, id):
    acte = get_object_or_404(ActeNaissance, id=id)
    acte.statut = "Validé"
    acte.validated_by = request.user
    acte.save()
    return redirect("actes_naissance")


@login_required
def export_naissance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actes_naissance.csv"'

    writer = csv.writer(response)
    writer.writerow(["N°", "Année", "Nom", "Prénom", "Sexe", "Date", "Lieu"])

    for acte in ActeNaissance.objects.all():
        writer.writerow([
            acte.numero,
            acte.annee,
            acte.nom,
            acte.prenom,
            acte.sexe,
            acte.date_naissance,
            acte.lieu_naissance
        ])
    return response


@login_required
def acte_naissance_pdf(request, id):
    acte = get_object_or_404(ActeNaissance, id=id)

    template = get_template("etatcivil/acte_naissance_pdf.html")
    html = template.render({'acte': acte})

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = f'filename="acte_naissance_{acte.id}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response


@login_required
def certificats_list(request):
    search = request.GET.get("search", "")
    qs = Certificat.objects.all()

    if search:
        qs = qs.filter(nom__icontains=search) | qs.filter(prenom__icontains=search) | qs.filter(type_certificat__icontains=search)

    paginator = Paginator(qs.order_by("-created_at"), 10)
    page = request.GET.get("page")
    certs = paginator.get_page(page)

    form = CertificatForm()

    # ➤ CREATE
    if request.method == "POST" and "create" in request.POST:
        form = CertificatForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.created_by = request.user
            cert.save()

            # Historique
            HistoriqueEtatCivil.objects.create(
                acte_type="certificat", acte_id=cert.id, action="Création", user=request.user
            )

            # 📩 Notification Email
            envoyer_email(
                cert.email,
                "Votre demande de certificat a été enregistrée",
                f"Bonjour {cert.prenom},\n\nVotre demande de certificat ({cert.get_type_certificat_display()}) est bien enregistrée.\n"
            )

            # 📱 SMS (optionnel)
            envoyer_sms(
                cert.telephone,
                f"Votre demande de certificat {cert.get_type_certificat_display()} est enregistrée."
            )

            return redirect("certificats_list")

    # ➤ EDIT
    if request.method == "POST" and "edit" in request.POST:
        cert = get_object_or_404(Certificat, id=request.POST.get("cert_id"))
        form_edit = CertificatForm(request.POST, instance=cert)
        if form_edit.is_valid():
            form_edit.save()

            # Historique
            HistoriqueEtatCivil.objects.create(
                acte_type="certificat", acte_id=cert.id, action="Modification", user=request.user
            )

            # 📩 Notification Email
            envoyer_email(
                cert.email,
                "Mise à jour de votre certificat",
                f"Bonjour {cert.prenom},\n\nVotre demande de certificat a été mise à jour.\n"
            )

            return redirect("certificats_list")

    # ➤ AJAX DELETE
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
        and request.POST.get("action") == "delete"
    ):
        try:
            cert = Certificat.objects.get(id=request.POST.get("id"))

            # Historique
            HistoriqueEtatCivil.objects.create(
                acte_type="certificat", acte_id=cert.id, action="Suppression", user=request.user
            )

            # 📩 Notification Email
            envoyer_email(
                cert.email,
                "Votre certificat a été supprimé",
                f"Bonjour {cert.prenom},\nVotre demande de certificat a été supprimée par le service."
            )

            cert.delete()
            return JsonResponse({"status": "success"})
        except Certificat.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Introuvable"}, status=404)

    return render(request, "etatcivil/certificats_list.html", {
        "certs": certs,
        "form": form,
        "search": search,
    })


@login_required
def valider_certificat(request, id):
    if not (request.user.role in ("chef_service", "superadmin")):
        return redirect("certificats_list")

    cert = get_object_or_404(Certificat, id=id)
    cert.statut = "Validé"
    cert.validated_by = request.user
    cert.save()

    # Historique
    HistoriqueEtatCivil.objects.create(
        acte_type="certificat", acte_id=cert.id, action="Validation", user=request.user
    )

    # 📩 Email
    envoyer_email(
        cert.email,
        "Votre certificat a été validé",
        f"Bonjour {cert.prenom},\n\nVotre certificat ({cert.get_type_certificat_display()}) a été VALIDÉ.\n"
        "Vous pourrez télécharger le PDF dès qu'il sera généré."
    )

    # 📱 SMS
    envoyer_sms(
        cert.telephone,
        f"Votre certificat {cert.get_type_certificat_display()} a été VALIDÉ."
    )

    return redirect("certificats_list")


@login_required
def certificat_pdf(request, id):
    cert = get_object_or_404(Certificat, id=id)

    # -------------------------------------------------------
    # 1️⃣ Génération du lien public pour la vérification
    # -------------------------------------------------------
    verify_url = request.build_absolute_uri(
        reverse("verify_certificat", args=[cert.id])
    )

    # -------------------------------------------------------
    # 2️⃣ Génération du QR Code
    # -------------------------------------------------------
    qr_img = qrcode.make(verify_url)
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_bytes = buffer.getvalue()

    # Sauvegarde dans la BDD (champ qr_code du modèle)
    cert.qr_code.save(
        f"qr_cert_{cert.id}.png",
        ContentFile(qr_bytes),
        save=False
    )

    # Base64 pour affichage dans le template HTML
    qr_b64 = base64.b64encode(qr_bytes).decode()

    # -------------------------------------------------------
    # 3️⃣ Rendu HTML → PDF
    # -------------------------------------------------------
    template = get_template("etatcivil/pdf_certificat.html")

    html = template.render({
        "cert": cert,
        "qr_b64": qr_b64,
        "verify_url": verify_url
    })

    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    if pisa_status.err:
        return HttpResponse("Erreur lors de la génération du PDF", status=500)

    pdf_bytes = pdf_buffer.getvalue()

    # -------------------------------------------------------
    # 4️⃣ Sauvegarde du PDF dans le modèle
    # -------------------------------------------------------
    cert.pdf.save(
        f"certificat_{cert.id}.pdf",
        ContentFile(pdf_bytes),
        save=True
    )

    # -------------------------------------------------------
    # 5️⃣ Ajouter dans l'historique
    # -------------------------------------------------------
    HistoriqueEtatCivil.objects.create(
        acte_type="certificat",
        acte_id=cert.id,
        action="Génération du PDF",
        user=request.user
    )

    # -------------------------------------------------------
    # 6️⃣ Retourner le PDF au navigateur
    # -------------------------------------------------------
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response['Content-Disposition'] = (
        f'attachment; filename="certificat_{cert.id}.pdf"'
    )
    return response


@login_required
def export_certificats_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="certificats.csv"'
    writer = csv.writer(response)
    writer.writerow(["ID", "Type", "Nom", "Prénom", "DateNaiss", "Adresse", "Statut", "Créé le"])
    for c in Certificat.objects.order_by("created_at"):
        writer.writerow([c.id, c.get_type_certificat_display(), c.nom, c.prenom, c.date_naissance or "", c.adresse or "", c.statut, c.created_at])
    return response


@login_required
def export_certificats_pdf_list(request):
    certs = Certificat.objects.all()
    template = get_template("etatcivil/pdf_certificats_list.html")
    html = template.render({"certs": certs})
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="certificats_list.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erreur génération PDF", status=500)
    return response


@login_required
def verify_certificat(request, id):
    cert = get_object_or_404(Certificat, id=id)
    return render(request, "etatcivil/verify_certificat.html", {"cert": cert})


@login_required
def registres_list(request):
    registres = Registre.objects.order_by("-annee", "type_acte")

    stats = {
        "naissance": ActeNaissance.objects.count(),
        "mariage": ActeMariage.objects.count(),
        "deces": ActeDeces.objects.count(),
        "certificat": Certificat.objects.count(),
    }

    return render(request, "etatcivil/registres_list.html", {
        "registres": registres,
        "stats": stats,
    })


# Export CSV
@login_required
def registres_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registres.csv"'

    writer = csv.writer(response)
    writer.writerow(["Type", "Année", "Dernier Numéro"])

    for r in Registre.objects.all():
        writer.writerow([r.type_acte, r.annee, r.dernier_numero])

    return response


# Export PDF
@login_required
def registres_pdf(request):
    registres = Registre.objects.all()
    template = get_template("etat_civil/pdf_registres.html")
    html = template.render({"registres": registres})

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="registres.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erreur génération PDF", status=500)

    return response


def verification_publique(request):
    query = request.GET.get("code", "")
    resultat = None

    if query:
        # Recherche multi-documents
        resultat = (
            ActeNaissance.objects.filter(code_verification=query).first() or
            ActeDeces.objects.filter(code_verification=query).first() or
            ActeMariage.objects.filter(code_verification=query).first() or
            Certificat.objects.filter(code_verification=query).first()
        )

        # Enregistrer historique
        HistoriqueVerification.objects.create(
            code=query,
            type_document=resultat.type_document if resultat else "Non trouvé",
            resultat=bool(resultat),
            user=request.user if request.user.is_authenticated else None
        )

        # Génération QR code pour le document si trouvé
        qr_b64 = None
        if resultat:
            verify_url = request.build_absolute_uri(f"/verification/?code={query}")
            qr_img = qrcode.make(verify_url)
            buffer = io.BytesIO()
            qr_img.save(buffer, format="PNG")
            qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    else:
        qr_b64 = None

    return render(request, "etatcivil/verification_publique.html", {
        "query": query,
        "resultat": resultat,
        "qr_b64": qr_b64
    })
