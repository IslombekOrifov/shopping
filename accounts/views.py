from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, OuterRef

# for email
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

# token
from .tokens import activation_token
from .models import CustomUser, Profile
from .forms import *

# other apps
from orders.models import Order, OrderItem
from wishlists.models import WishedProduct
from products.models import ProductItem, ProductImage
from general.models import Currency
from general.services import get_currency_from_session
from common.services import get_price_like_float
from carts.cart import Cart
from carts.forms import CartAddProductForm


# Create your views here. Registration
def user_register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        # profile_form = ProfileRegisterForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            try: 
                user = CustomUser.objects.filter(Q(username=cd['username']) | Q(email=cd['email']))[:1].get()
            except:
                user = None
            if user is not None:
                if not user.is_active:
                    activateEmail(request, user, user.email)
                else:
                    if user.username == cd['username']:
                        messages.error(request, "Bunday username mavjud. Boshqa username tanlashingizni so'raymiz/")
                    elif user.email == cd['email']:
                        messages.error(request, "Bunday email mavjud. Boshqa emaildan foydalanishingiz yoki email orqali parolingizni tiklashingiz mumkin!")
                    return redirect('accounts:register')
            else:
                new_user = user_form.save(commit=False)
                new_user.set_password(cd['password'])
                new_user.is_active = False
                new_user.save()
                activateEmail(request, new_user, cd['email'])
                return redirect('general:index')
    else:
        user_form = UserRegisterForm()
        # profile_form = ProfileRegisterForm()

    context = {
        'user_form': user_form,
    }
    return render(request, 'accounts/registration/registration.html', context)

# account activation and password reset confirmation email
def activateEmail(request, user, to_email, pass_reset=None):
    if not pass_reset:
        mail_subject = 'Akkountingizni aktivlashtiring!'
        template = 'accounts/registration/template_activate_account.html'
    else:
        mail_subject = "Parolingizni qayta tiklang!"
        template = 'accounts/registration/password_reset_email.html'
    message = render_to_string(template, {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Akkatuntingiz muvaffaqiyatli yaratildi. {user} akkauntini aktivlashtirish uchun \
                            {to_email} pochtangizni yuborilgan link ustiga bosing va ro'yxatdan o'tishni yakunlang! <b>Muhim</b> Spam katalogini tekshiring!"
        )
    else:
        messages.error(request, f"{to_email} pochtaga xabar yuborishda xatolik. To'g'ri elektron manzil kiritilganini tekshiring!")


def user_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
    except:
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Emailni tasdiqlash muvaffaqiyatli amalga oshirildi. Akkountingizga kirishingiz mumkin.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Tasdiqlash linki muddati o'tgan, Boshqattan ro'yxatdan o'tishingizni so'raymiz!")
    return redirect("accounts:register")
# end account activation and password reset confirmation email

# password reset 
def password_reset(request):
    if request.method == 'POST':
        form = request.POST.get('email')
        user = CustomUser.objects.get(email=form)
        if user and form:
            activateEmail(request, user, form, pass_reset=True)
            messages.success(request, "Parolni tiklash uchun link elektron pochtangizga yuborildi.")
            return redirect('accounts:password_reset_done')
        else:
            messages.error(request, "Kiritilgan emailga bog'liq akkount topilmadi. Tekshirib qaytadan urinib ko'ring!")
    return render(request, "accounts/registration/password_reset_form.html")


def password_reset_done(request):
    return render(request, "accounts/registration/password_reset_done.html")
     

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=uid)
    except:
        user = None
    if user and activation_token.check_token(user, token):
        if request.method == 'POST':
            form = PassResetForm(request.POST)
            if form.is_valid():
                if user:
                    user.set_password(form.cleaned_data['password2'])
                    user.save()
                    messages.success(request, "Parolingiz muvaffaqiyatli almashtirildi. Akkountingizga kirishingiz mumkin!")
                    return redirect('accounts:password_reset_complete')
        else:
            form = PassResetForm()
        return render(request, 'accounts/register/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Tasdiqlash linki muddati o'tgan. Boshqattan so'rov yuborishingiz mumkin.")
        return redirect('general:index')


def password_reset_complete(request):
    return render(request, 'accounts/resiter/password_reset_complete.html')
# is not validni so'ra!!!!!!!!!!!
# end password reset 

# login
def user_login(request):
    if request.method == "POST":
        form = UserLogForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect('general:index')
                    elif user.role == CustomUser.CHOICE_ROLE[0][0]:
                        return redirect("accounts:dashboard")
                    else:
                        return redirect("accounts:seller_dashboard")
                        
                else:
                    if not user.last_login:
                        messages.error(request, "Akkauntiniz aktivlashtirilmagan. Aktivlashtirish linki elektron pochtangizga yuborilgan."\
                            "Agar aktivlashtirish linki muddati o'tgan bo'lsa registratsiya bo'limidagi aktivlashtirish ni ustiga bosing!"
                        )
                    else:
                        messages.error(request, "Akkountingiz adminstratsiya tomonidan bloklangan. Support bilan bog'laning!")
            else:
                messages.error(request, "Bunday akkount mavjud emas. Login va parolingizni tekshirib qaytadan urinib ko'ring!")
        else:
            messages.error(request, "Login yoki parol to'ldirilishida xatolik mavjud. Tekshirib qaytadan urinib ko'ring")
    else:
        form = UserLogForm()
    return render(request, 'accounts/registration/login.html', {'form':form})
# end login

# logout
def user_logout(request):
    logout(request)
    return redirect('general:index')
# endlogout

# update user details
def user_details(request):
    if request.method == "POST":
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileUpdateForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ma'lumotlar muvaffaqiyatli o'zgartirildi.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Ma'lumotlar to'ldirilishida xatolik mavjud.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'section': 'details'
    }
    return render(request, 'accounts/customer/details_pages/details.html', context)

# update user details

# password change
def password_change(request):
    if request.method == "POST":
        pass_form = PassUpdateForm(request.POST)
        if  pass_form.is_valid():
            user = CustomUser.objects.get(id=request.user.id)
            if user.check_password(pass_form.cleaned_data['old_password']):
                user.set_password(pass_form.cleaned_data['new_password2'])
                user.save()
                messages.success(request, "Parol muvaffaqiyatli almashtirildi.")
                return redirect('accounts:details')
            else:
                messages.error(request, "Joriy parol xato!")
        else:
            messages.error(request, "Formani to'ldirishda xatolik mavjud.")
    else:
        pass_form = PassUpdateForm()
    context = {
        'pass_form': pass_form,
        'section': 'password_change'
    }
    return render(request, 'accounts/customer/details_pages/password_change.html', context)
# end password update

# user orders
def user_orders(request):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price

    orders = Order.objects.filter(client=request.user).annotate(
        price_currency=get_price_like_float('total_price') / currency_price,
    )
    context = {
        'orders': orders,
        'section': 'orders'
    }
    return render(request, 'accounts/customer/details_pages/orders.html', context)


def user_wishlist(request):
    currency_price = Currency.objects.get(code=get_currency_from_session(request)).price
    user = request.user
    if user.is_authenticated and user.role == CustomUser.CHOICE_ROLE[0][0]:
        product_ids = WishedProduct.objects.values_list()
        product_items = ProductItem.objects.filter(is_deleted=False, is_archive=False,
            wishlists__client=user).annotate(price_currency=get_price_like_float('price') / currency_price, 
            image=ProductImage.objects.filter(product_item=OuterRef('pk')
            ).values('image_middle')[:1]).order_by('-wishlists__created')
        return render(request, 'accounts/customer/details_pages/wishlist.html', {'product_items': product_items, 'section': 'wishlist'})
    else:
        return HttpResponse("Sizga wishlist qo'shish mumkin emas")


def user_carts(request):
    cart = Cart(request)
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'accounts/customer/details_pages/carts.html', {'cart': cart})


def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'section': 'dashboard', 
        'profile': profile
    }
    return render(request, 'accounts/customer/details_pages/dashboard.html', context)


# seller pages
def seller_dashboard(request):
    return render(request, 'accounts/seller/index.html')