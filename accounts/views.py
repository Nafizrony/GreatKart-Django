from django.shortcuts import render,redirect,HttpResponse
from .forms import AccountForm
from .models import Account
from django.contrib import  messages,auth
from django.contrib.auth.decorators import login_required
from .models import Account
from cart.models import Cart,Cart_Items
from cart.views import _cart_id
# Active user account with email varification
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
# from urllib.parse import urlparse

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please active your account'
            message = render_to_string('accounts/account_varification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Thanks for registering with us.We have sent you a verification email to your email.Please verify it. ')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = AccountForm()
    context = {'form':form}
    return render(request,'accounts/register.html',context)

# login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                existcartitems = Cart_Items.objects.filter(cart=cart).exists()
                print(existcartitems)
                if existcartitems:
                    cartitems = Cart_Items.objects.filter(cart=cart)
                    product_variation = []
                    for item in cartitems:
                        variations = item.item_variation.all()
                        product_variation.append(list(variations))
                    
                    ex_product_variation = []
                    id = []
                    cartitems = Cart_Items.objects.filter(user=user)
                    for item in cartitems:
                        variations = item.item_variation.all()
                        ex_product_variation.append(list(variations))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_product_variation:
                            index = ex_product_variation.index(pr)
                            item_id = id[index]
                            item = Cart_Items.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            item = Cart_Items.objects.get(cart=cart)
                            item.user = user
                            item.save()
            except:
                pass
            auth.login(request,user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('query=>',query)
                params = dict(x.split('=') for x in query.split('&'))

                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

                # requests.get(url, params=params)
            except:
                return redirect('dashboard')
        else:
            messages.error(request,"Invalid Credentials!!")
            return redirect('login')
    
    return render(request,'accounts/login.html')

# logout
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

# active user account
def activate(request, uidb64, token):  
    try:  
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        user.is_active = True 
        user.save()  
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')  
    else:  
        messages.error('Activation link is invalid!')  
        return redirect('register')
    
# dashboard
def dashboard(request):
    context = {}
    return render(request,'accounts/dashboard.html',context)

# forgot password
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Your reset password email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account Does not exist')
    return render(request,'accounts/forgotpassword.html')

# reset password
def reset_password(request,uidb64, token):
    try:  
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect(resetpassword)
    else:
        messages.error(request,'This link has been expired!!')
        return redirect('login')
    
    

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request,'Password fields does not match')
    else:
        return render(request,'accounts/resetpassword.html')
