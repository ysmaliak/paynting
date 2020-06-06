from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from lab3_ts.settings import LOGGING
from .models import Masterpiece, Search, Sort, MadeWith
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import MasterpieceUpdateMultiForm, MasterpieceCreationMultiForm, SignUpForm
from .tokens import account_activation_token
import logging.config


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class HomePageView(ListView):
    model = Masterpiece
    template_name = 'base.html'


class MasterpieceCreateView(CreateView):
    model = Masterpiece
    form_class = MasterpieceCreationMultiForm
    template_name = 'create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save_user(self.request.user)
        md = MadeWith(hardware=form.cleaned_data['made_with']['hardware'], software=form.cleaned_data['made_with']['software'])
        md.save()
        form.save_made_with(md)
        logger.debug("new masterpiece")
        return super().form_valid(form)


class MasterpieceUpdateView(UpdateView):
    model = Masterpiece
    form_class = MasterpieceUpdateMultiForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(MasterpieceUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'masterpiece': self.object,
            'made_with': self.object.made_with,
        })
        logger.debug("update masterpiece")
        return kwargs


def account_view(request, username):
    user = User.objects.get(username=username)
    masterpiece_list = Masterpiece.objects.all().filter(uploaded_by__username=username)
    logger.debug("visit account")
    return render(request, 'account.html', {"user": user, "masterpiece_list": masterpiece_list})


def masterpiece_detail_view(request, primary_key):
    masterpiece = get_object_or_404(Masterpiece, pk=primary_key)
    logger.debug('visit detail view')
    return render(request, 'masterpiece.html', context={'masterpiece': masterpiece})


def signup_view(request):
    logger.debug("attempt to signup")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activation_sent_view(request):
    logger.debug("activation sent")
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        logger.debug("activation")
        return redirect('home')
    else:
        logger.debug("activation fail")
        return render(request, 'activation_invalid.html')


class MasterpieceDeleteView(DeleteView):
    model = Masterpiece
    success_url = reverse_lazy('home')


class SearchView(ListView):
    model = Search
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        logger.debug("new search: " + query)
        search = Search(search=query)
        search.save()
        object_list = Masterpiece.objects.filter(
            Q(masterpiece_name__icontains=query) | Q(uploaded_by__username__icontains=query)
        )
        return object_list


def sort_view(request):
    sort_type = request.GET.get('sort_type')
    if sort_type is not None:
        logger.debug("new sort: " + sort_type)
        sort = Sort(sort_type=sort_type)
        sort.save()
        if sort_type == 'az':
            masterpieces_sorted = Masterpiece.objects.all().order_by('masterpiece_name')
        else:
            masterpieces_sorted = Masterpiece.objects.all().order_by('-masterpiece_name')
    else:
        masterpieces_sorted = Masterpiece.objects.all()
    return render(request, 'sort.html', {"masterpieces_sorted": masterpieces_sorted})
