from django.shortcuts import render, redirect
from .models import accounts, password_verify_request, GuestSettings, AdSettings, Page_settings
import bcrypt
from django.http import HttpResponse, JsonResponse
import random
import string
import smtplib
from django.contrib import messages

def register(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        return redirect('logout2')
    else:
        if request.method == "POST":
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            age = request.POST['age']
            mobileno = request.POST['mobileno']
            qualification = request.POST['qualification']
            gender = request.POST['gender']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
            password = password1.encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            newaccount = accounts(email=email, first_name=first_name, last_name=last_name, age=age, mobileno=mobileno, qualification=qualification, gender=gender, password=hashed_password.decode('utf-8'))
            newaccount.save()
            messages.success(request, 'User registered successfully')
            return redirect('login2')
        return render(request, 'accounts/register.html')

def login(request):
    if request.session['user']:
        return HttpResponse("Could not logout properly please <a href='/accounts/logout/'>logout</a> again")
    else:
        if request.method == "POST":
            email = request.POST['email']
            try:
                account = accounts.objects.get(email=email)
                password = request.POST['password'].encode('utf-8')
                account_password = account.password.encode('utf-8')
                if bcrypt.checkpw(password, account_password):
                    user = {'email': email, 'is_verified': account.is_verified, 'is_superuser': account.is_superuser, 'first_name': account.first_name, 'gender': account.gender}
                    request.session['user'] = user
                    messages.success(request, 'Logged in successfully')
                    return redirect('home')
                else:
                    messages.error(request, 'Please check the email or password')
                    return redirect('login2')
            except:
                messages.error(request, 'Please check the email or password')
            return redirect('login2')
        return render(request, 'accounts/login.html')

def profile(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']['email'] != 'guest':
        user = accounts.objects.get(email=request.session['user']['email'])
        context = {
            'user': user,
            'ads': ads.objects.all()[:6]
        }
        return render(request, 'accounts/profile.html', context)

def guest_login(request):
    try:
        guest_setting = GuestSettings.objects.first()
    except:
        guest_setting = GuestSettings(timer='15')
        guest_setting.save()
        guest_setting = GuestSettings.objects.first()
    timer = int(guest_setting.timer)
    request.session['user'] = {'email': 'guest', 'is_verified': True, 'timer': f"{timer*60000}", 'first_name': 'guest'}
    if request.POST.get('action') == 'update_time':
        request.session['user']['timer'] = request.POST.get('timer')
        messages.success(request, "Guest seetings updated successfully")
    return redirect('home')

def guest_settings(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.session['user']['is_superuser']:
            guest_settings_model = GuestSettings.objects.first()
            ad_timer = AdSettings.objects.first()
            per_page = Page_settings.objects.first()
            if request.method == "POST":
                timer = str(request.POST['timer'])
                ad_timing = str(request.POST['ad_timer'])
                per_page_number = str(request.POST['per_page'])
                try:
                    guest_settings_model = GuestSettings.objects.first()
                    guest_settings_model.timer = timer
                except:
                    guest_settings_model = GuestSettings(timer=timer)
                try:
                    ad_timer = AdSettings.objects.first()
                    ad_timer.ad_timing = ad_timing
                except:
                    ad_timer = AdSettings(ad_timing=ad_timing)
                try:
                    per_page = Page_settings.objects.first()
                    per_page.per_page = per_page_number
                except:
                    per_page = Page_settings(per_page=per_page_number)
                ad_timer.save()
                guest_settings_model.save()
                per_page.save()
                return redirect('home')
            context = {
                'guest': guest_settings_model,
                'ad_timer': ad_timer,
                'per_page': per_page,
            }
            return render(request, 'accounts/guest_settings.html', context)
        else:
            return HttpResponse('You are not allowed to perform this action')
    else:
        return redirect('login2')

def logout(request):
    try:
        if request.session['user']:
            request.session['user'] = ''
            return render(request, 'accounts/logout.html')
        else:
            request.session['user'] = ''
            return redirect('login2')
    except:
        request.session['user'] = ''
        return render(request, 'accounts/logout.html')

def password_reset(request):
    response = {}
    if request.POST.get('action') == 'password_reset':
        email = request.POST.get('email')
        try:
            account = accounts.objects.get(email=email)
            try:
                letters_and_digits = string.ascii_letters + string.digits
                result_str = ''.join(random.choice(letters_and_digits) for i in range(32))
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()
                    smtp.login('udayptl9@gmail.com', 'ahwoahunadxwpbvl')
                    subject = 'Password Reset Request'
                    body = f'Password Reset can be done by clicking here: http://localhost:8000/accounts/password_reset_verify/{result_str}'
                    message = f'Subject: {subject} \n\n{body}'
                    smtp.sendmail('udayptl9@gmail.com', email, message)
                newVerify = password_verify_request(email=email, token=result_str, is_verified=False)
                newVerify.save()
                response['text'] = 'true'
                return JsonResponse(response)
            except Exception as e:
                print(f'error: {e}')
                return HttpResponse('Password Reset failed')
        except:
            response['response'] = 'false'
            response['message'] = 'User doesnot exists'
            return JsonResponse(response)
    return render(request, 'accounts/password_reset.html')

def password_reset_sent(request):
    return render(request, 'accounts/password_reset_verify.html')

def password_reset_confirm(request, token):
    response = {}
    try:
        check_request = password_verify_request.objects.get(token=token)
        if request.POST.get('action') == 'password_reset_request':
            try:
                account = accounts.objects.get(email=check_request.email)
                password = request.POST.get('password')
                password = password.encode('utf-8')
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                hashed_password = hashed_password.decode('utf-8')
                account.password = hashed_password
                account.save()
                check_request.is_verified = True
                response['text'] = 'true'
                request.session['user'] = ''
                return JsonResponse(response)
            except Exception as e:
                print('Error', e)
        return render(request, 'accounts/password_reset_page.html', {'token': token})
    except Exception as e:
        print(f'error: {e}')
        return HttpResponse('Page doesnot exists')