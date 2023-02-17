from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, UserLoginForm, VerifyCodeForm, EditUserForm, PasswordChangingForm, \
    AddressForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from utils import send_otp_code
from .models import OtpCode, User, Address
from orders.models import Order


class UserRegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = form.cleaned_data
            send_otp_code(cd['phone'], random_code)
            OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone'], 'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('product/home.html')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                if user.is_staff():
                    return redirect(to=reverse('admin:index'))
                else:
                    messages.success(request, 'you logged in successfully', 'info')
                    return redirect('product:home')
            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('product:home')


class UserRegisterVerifyCode(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    @csrf_exempt
    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(phone_number=user_session['phone_number'], email=user_session['email'],
                                         full_name=user_session['full_name'],
                                         password=user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registered.', 'success')
                return redirect('product:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('product:home')


class EditUserView(LoginRequiredMixin, View):
    template_name = 'accounts/edit_profile.html'
    form = EditUserForm

    def get(self, request):
        form = self.form(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'profile edited successfully', 'success')
        return redirect('product:home')


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('product:home')


class AddressUserView(View):
    template_name = 'accounts/addresses.html'

    def get(self, request):
        context = {
            "addresses": Address.objects.filter(customer_id=request.user.id)
        }
        return render(request, self.template_name, context)


class EditAddressView(View):
    template_name = 'accounts/edit_address.html'
    form = AddressForm

    def get(self, request, address_id):
        address = Address.objects.get(pk=address_id)
        form = self.form(instance=address)
        return render(request, self.template_name, {'address': address, 'form': form})

    def post(self, request, address_id):
        address = Address.objects.get(pk=address_id)
        form = self.form(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'address edited successfully', 'success')
        return redirect('accounts:addresses_user')


class RemoveAddressView(View):
    template_name = 'accounts:addresses_user'

    def get(self, request, address_id):
        address = Address.objects.get(pk=address_id)
        address.delete()
        return redirect(self.template_name)


class AddAddressView(View):
    template_name = 'accounts/add_address.html'
    form = AddressForm

    def get(self, request):

        form = self.form(initial={'customer': request.user})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST, initial={'customer': request.user})
        if form.is_valid():
            form.save()
            messages.success(request, 'new address added successfully', 'success')
        return redirect('accounts:addresses_user')


class OrdersHistoryView(View):
    template_name = 'accounts/orders.html'

    def get(self, request):
        context = {
            "orders": Order.objects.filter(user_id=request.user.id)
        }
        return render(request, self.template_name, context)
