from django.views.generic import TemplateView
from .models import *
from django.db.models import Q
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django. contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
class SignUpView(TemplateView):
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email').lower()
        full_name = request.POST.get('full_name').upper()
        password = request.POST.get('password')

        if email and password:
            user = CustomUser(
                email=email,
                full_name=full_name,
                password=make_password(password)  # Hash the password
            )
            user.save()
            login(request, user)  # Log the user in after signup
            return redirect('user_list')  # Redirect to user list after signup
        
        return render(request, self.template_name)

class UserListView(TemplateView):
    template_name = 'user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all().exclude(is_superuser=True).order_by('-id')  # Get all users
        return context

class ParticularUserDataListView(TemplateView):
    template_name = 'user_data_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search', '')
        user_data = UserData.objects.all().order_by('-id')

        if query:
            user_data = user_data.filter(
                Q(particulars__icontains=query) |
                Q(remarks__icontains=query) |
                Q(citizen_ship__icontains=query) |
                Q(licence_no__icontains=query) |
                Q(expiry_date__icontains=query)
            )

        context['user_data'] = user_data
        context['search'] = query
        return context


class ParticularUserDataFormView(TemplateView):
    template_name = 'user_data_form.html'

    def post(self, request, *args, **kwargs):
        particulars = request.POST.get('particulars').upper()
        email = request.POST.get('email').lower()
        remarks = request.POST.get('remarks').upper()
        citizen_ship = request.POST.get('citizen_ship').upper()
        licence_no = request.POST.get('licence_no').upper()

        # Get expiry_date from the form
        expiry_date_str = request.POST.get('expiry_date', '')
        expiry_date = timezone.datetime.fromisoformat(expiry_date_str).astimezone(timezone.get_current_timezone()) if expiry_date_str else None

        # Create new UserData entry
        UserData.objects.create(
            particulars=particulars,
            email=email,
            remarks=remarks,
            citizen_ship=citizen_ship,
            licence_no=licence_no,
            expiry_date=expiry_date
        )

        return redirect('user_data_list')


class PartcularUserDataUpdateView(TemplateView):
    template_name = 'user_data_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        user_data = get_object_or_404(UserData, pk=pk)
        context['user_data'] = user_data
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_data = get_object_or_404(UserData, pk=pk)

        # Update the fields from the form
        user_data.particulars = request.POST.get('particulars').upper()
        user_data.email = request.POST.get('email').lower()
        user_data.remarks = request.POST.get('remarks').upper()
        user_data.citizen_ship = request.POST.get('citizen_ship').upper()
        user_data.licence_no = request.POST.get('licence_no').upper()

        # Get and set expiry_date from the form
        expiry_date_str = request.POST.get('expiry_date', '')
        user_data.expiry_date = timezone.datetime.fromisoformat(expiry_date_str).astimezone(timezone.get_current_timezone()) if expiry_date_str else None

        # Reset email_sent to False
        user_data.email_sent = False
        user_data.save()

        return redirect('user_data_list')

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_data_list')
        else:
            messages.error(request, 'Invalid email or password.')
            return self.get(request, *args, **kwargs)
