from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.http import JsonResponse
import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
# --- VUE D'INSCRIPTION ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_dashboard(user)  # Redirection correcte
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "superadmin":
            return view_func(request, *args, **kwargs)
        messages.error(request, "Accès refusé !")
        return redirect("login")
    return wrapper
@login_required
def dashboard_superadmin(request):
    return render(request, 'dashboard/superadmin.html')
@login_required
def dashboard_agent_ec(request):
    return render(request, 'dashboard/agent_ec.html')
@login_required
def dashboard_responsable_admin(request):
    return render(request, 'dashboard/responsable_admin.html')
@login_required
def dashboard_agent_finances(request):
    return render(request, 'dashboard/agent_finances.html')
@login_required
def dashboard_chef_service(request):
    return render(request, 'dashboard/chef_service.html')
@login_required
def dashboard_citoyen(request):
    return render(request, 'dashboard/citoyen.html')

# --- VUE DE CONNEXION ---
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_dashboard(user)  # Redirection selon rôle
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


# --- VUE DE DÉCONNEXION ---
def logout_view(request):
    logout(request)
    return redirect('login')


# --- REDIRECTION SELON RÔLE ---
def redirect_user_dashboard(user):
    """
    Redirige l'utilisateur vers son tableau de bord selon son rôle.
    ATTENTION : Retourne toujours un objet HttpResponse (redirect).
    """
    if user.is_superadmin():
        return redirect('dashboard_superadmin')
    elif user.is_agent_ec():
        return redirect('dashboard_agent_ec')
    elif user.is_responsable_admin():
        return redirect('dashboard_responsable_admin')
    elif user.is_agent_finances():
        return redirect('dashboard_agent_finances')
    elif user.is_chef_service():
        return redirect('dashboard_chef_service')
    elif user.is_citoyen():
        return redirect('dashboard_citoyen')
    else:
        return redirect('login')




# users/views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # Crée ensuite le template home.html




@login_required
def gerer_utilisateurs(request):

    # AJAX suppression
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        user_id = request.POST.get("id")
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return JsonResponse({"status": "success"})

    search = request.GET.get("search", "")

    users_qs = CustomUser.objects.filter(
        nom__icontains=search
    ) | CustomUser.objects.filter(
        prenom__icontains=search
    ) | CustomUser.objects.filter(
        username__icontains=search
    )

    paginator = Paginator(users_qs.order_by('id'), 5)
    page = request.GET.get("page")
    users = paginator.get_page(page)

    # FORMULAIRE D'AJOUT
    form_add = CustomUserCreationForm()

    # FORMULAIRES D'EDITION (UN PAR UTILISATEUR)
    edit_forms = {u.id: CustomUserChangeForm(instance=u) for u in users}

    # Création utilisateur
    if request.method == "POST" and "create" in request.POST:
        form_add = CustomUserCreationForm(request.POST, request.FILES)
        if form_add.is_valid():
            form_add.save()
            messages.success(request, "Utilisateur ajouté avec succès.")
            return redirect("gerer_utilisateurs")

    # Modification utilisateur
    if request.method == "POST" and "edit" in request.POST:
        user_id = request.POST.get("user_id")
        user = get_object_or_404(CustomUser, id=user_id)

        form_edit = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form_edit.is_valid():
            form_edit.save()
            messages.success(request, "Utilisateur modifié avec succès.")
            return redirect("gerer_utilisateurs")
    forms_edit = {u.id: CustomUserChangeForm(instance=u) for u in users_qs}


    context = {
        "users": users,
        "form_add": form_add,
        "edit_forms": edit_forms,
        "search": search,
    }
    return render(request, "users/gerer_utilisateurs.html", context)


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="utilisateurs.csv"'

    writer = csv.writer(response)
    writer.writerow(["Nom", "Prénom", "Username", "Email", "Téléphone", "Rôle"])

    for u in CustomUser.objects.all():
        writer.writerow([u.nom, u.prenom, u.username, u.email, u.telephone, u.role])

    return response


def export_users_pdf(request):
    users = CustomUser.objects.all()
    template = get_template("users/pdf_export.html")
    html = template.render({"users": users})

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="utilisateurs.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response