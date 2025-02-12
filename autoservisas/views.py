from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from .models import Paslauga, Uzsakymas, Masina, User, Modelis, Gamintojas, UzsakymoEilute, Klientas
from .forms import UzsakymasReviewForm, ProfileUpdateForm, UserUpdateForm
from .utils import check_pasword


def index(request):
    paslaugu_kiekis = Paslauga.objects.count()
    visu_uzsakymu_kiekis = Uzsakymas.objects.count()
    atliktu_uzsakymu_kiekis = Uzsakymas.objects.filter(statusas__exact='a').count()
    automobiliu_kiekis = Masina.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'paslaugu_kiekis': paslaugu_kiekis,
        'visu_uzsakymu_kiekis': visu_uzsakymu_kiekis,
        'atliktu_uzsakymu_kiekis': atliktu_uzsakymu_kiekis,
        'automobiliu_kiekis': automobiliu_kiekis,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)


def get_autos(request):
    autos = Masina.objects.all()
    paginator = Paginator(autos, 8)
    page_number = request.GET.get('page')
    paged_autos = paginator.get_page(page_number)
    context = {'autos': paged_autos}
    return render(request, 'autos.html', context=context)


def get_one_auto(request, auto_id):
    one_auto = get_object_or_404(Masina, pk=auto_id)
    context = {'one_auto': one_auto}
    return render(request, 'auto.html', context=context)


class UzsakymasListView(generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymas_list'
    template_name = 'orders.html'
    paginate_by = 5


class UzsakymasDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Uzsakymas
    context_object_name = 'uzsakymas'
    template_name = 'order.html'
    form_class = UzsakymasReviewForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.uzsakymas_object = self.get_object()
        form.instance.uzsakymas = self.uzsakymas_object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order-one', kwargs={'pk': self.uzsakymas_object.id})


def search(request):
    query_text = request.GET.get('search_text')
    # https://docs.djangoproject.com/en/4.2/ref/models/lookups/
    search_results = Masina.objects.filter(
        Q(klientas__vardas__icontains=query_text) |
        Q(klientas__pavarde__icontains=query_text) |
        Q(modelis__pavadinimas__icontains=query_text) |
        Q(modelis__gamintojas__pavadinimas__icontains=query_text) |
        Q(reg_numeris__icontains=query_text) |
        Q(vin_kodas__icontains=query_text)
    )

    context = {'query_text': query_text,
               'masina_list': search_results}

    return render(request, 'search_results.html', context=context)


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    context_object_name = 'uzsakymas_list'
    template_name = 'user_orders.html'

    def get_queryset(self):
        return Uzsakymas.objects.filter(uzsakovas=self.request.user)


@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not check_pasword(password):
            messages.error(request, 'Slaptažodis, mažiausiai 8 simboliai!!!')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Slaptažodžiai nesutampa')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Vartotojo vardas {username} jau egzistuoja')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email {email} jau egzistuoja')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, f'Vartotojas {username} sėkmingai užregistruotas!')
        return redirect('login')


@login_required()
def get_user_profile(request):

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, "Profilis atnaujintas")
        else:
            messages.error(request, "Profilis neatnaujintas")
        return redirect('user-profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form
    }

    return render(request, 'profile.html', context=context)
