from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Annonce
from .forms import AnnonceForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse

def export_archives_pdf(request):
    archives = Annonce.objects.filter(statut="archive")

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="archives_annonces.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Archives des Annonces")
    y -= 40

    p.setFont("Helvetica", 11)

    for a in archives:
        if y < 80:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 11)

        p.drawString(50, y, f"Titre : {a.titre}")
        y -= 15

        p.drawString(50, y, f"Date : {a.created_at.strftime('%d/%m/%Y')}")
        y -= 15

        contenu = (a.contenu[:150] + "...") if len(a.contenu) > 150 else a.contenu
        p.drawString(50, y, f"Contenu : {contenu}")
        y -= 30

    p.save()
    return response

class AnnonceView(View):

    def get(self, request):
        search = request.GET.get("q", "")
        annonces = Annonce.objects.exclude(statut="archive")

        if search:
            annonces = annonces.filter(
                Q(titre__icontains=search) | Q(contenu__icontains=search)
            )

        paginator = Paginator(annonces.order_by("-created_at"), 5)
        page = request.GET.get("page")
        annonces_page = paginator.get_page(page)

        archives = Annonce.objects.filter(statut="archive")

        form = AnnonceForm()

        return render(request, "annonces/annonces.html", {
            "annonces": annonces_page,
            "archives": archives,
            "form": form,
            "search": search,
        })

    def post(self, request):
        action = request.POST.get("action")

        # CREATE
        if action == "create":
            form = AnnonceForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect("annonces")

        # EDIT
        if action == "edit":
            annonce = get_object_or_404(Annonce, pk=request.POST["id"])
            form = AnnonceForm(request.POST, request.FILES, instance=annonce)
            if form.is_valid():
                form.save()
            return redirect("annonces")

        # DELETE
        if action == "delete":
            annonce = get_object_or_404(Annonce, pk=request.POST["id"])
            annonce.delete()
            return redirect("annonces")

        # PUBLISH
        if action == "publier":
            annonce = get_object_or_404(Annonce, pk=request.POST["id"])
            annonce.publier()
            return redirect("annonces")

        # ARCHIVE
        if action == "archiver":
            annonce = get_object_or_404(Annonce, pk=request.POST["id"])
            annonce.archiver()
            return redirect("annonces")

        # RESTORE
        if action == "restaurer":
            annonce = get_object_or_404(Annonce, pk=request.POST["id"])
            annonce.restaurer()
            return redirect("annonces")


def annonce_publique(request, id):
    annonce = get_object_or_404(Annonce, id=id, statut="publie")
    return render(request, "annonces/public.html", {"annonce": annonce})
