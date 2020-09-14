import fnmatch
import os
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import emailverifyrequest, ads, theme, advideo
import random
import string
import smtplib
from subadmin.models import Subadmin
from videos.models import Video, Category, Subcategory, Upcoming
from accounts.models import accounts, GuestSettings
from django.contrib import messages

def handler_404(request, exception):
    return render(request, '404.html')

def home(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            sub_admin = Subadmin.objects.get(email=request.session['user']['email'])
            user = request.session['user']
            if sub_admin.joined == False:
                sub_admin.joined = True
                sub_admin.save()
            if sub_admin.superuser:
                user['is_superuser'] = True
            if sub_admin.addvideo:
                user['addvideo'] = True
            if sub_admin.addcategory:
                user['addcategory'] = True
            if sub_admin.addlanguage:
                user['addlanguage'] = True
            request.session['user'] = user
        except:
            pass
        user_account = request.session['user']
        if user_account['is_verified'] == True:
            categories = Category.objects.all()
            subcategories_list = []
            subcategories = Subcategory.objects.all().order_by('-id')
            videos = Video.objects.all().order_by('-id')
            query = request.GET.get('query')
            if query:
                subcategories = subcategories.filter(subcategory__icontains=query)
                videos = videos.filter(title__icontains=query)
            for category in categories:
                filter_subcategories = subcategories.filter(category=category)
                if len(filter_subcategories) > 0:
                    subcategories_list.append(filter_subcategories)
            ads_ = ads.objects.all()
            id_s = [i for i in range(0, len(subcategories_list))]
            upcomings = Upcoming.objects.all()
            context = {
                'subcategories': subcategories_list,
                'ads': ads_,
                'ids': id_s,
                'slug': 'home',
                'upcomings': upcomings,
            }
            if query:
                if len(query) > 1:
                    context['videos'] = videos
            return render(request,"home.html", context)
        else:
            return render(request, 'home_page.html', {'verify': False})
    else:
        try:
            server_name = request.GET.get('redirect', False)
            if server_name == 'social':
                guest_setting = GuestSettings.objects.first()
                timer = int(guest_setting.timer)
                request.session['user'] = {'email': 'guest', 'is_verified': True, 'timer': f"{timer*60000}"}
                return redirect('home')
            else:
                return redirect('login2')
        except:
            return redirect('login2')

def feedback(request):
    return render(request, 'feedback.html')

def verify_email(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.session['user']['is_verified'] == True:
            return render(request, 'verify_already_done.html')
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join(random.choice(letters_and_digits) for i in range(32))
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login('udayptl9@gmail.com', 'ahwoahunadxwpbvl')
                subject = 'Verify Email'
                body = f'Thank you for using our service please verify your account by clicking here: http://localhost:8000/verify_email_check/{result_str}'
                message = f'Subject: {subject} \n\n{body}'
                smtp.sendmail('udayptl9@gmail.com', request.session['user']['email'], message)
            newVerify = emailverifyrequest(email=request.session['user']['email'], token=result_str, verified=False)
            newVerify.save()
            return render(request, 'verify_email.html', {'email': request.session['user']['email']})
        except Exception as e:
            print(f'error: {e}')
            return HttpResponse('Email verification failed')
    else:
        return redirect('login2')

def verify_email_check(request, token):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    try:
        user_email = emailverifyrequest.objects.get(token=token)
        if user_email.verified == True:
            return render(request, 'verify_already_done.html')
        request.session['user']['is_verified'] = True
        account = accounts.objects.get(email=request.session['user']['email'])
        account.is_verified = True
        account.save()
        user_email.save()
        request.session['user'] = ''
        return render(request, 'verify_email_successfull.html')
    except Exception as e:
        print(f'error: {e}')
        return HttpResponse('<h3>Eamil verification request doesnot exists</h3>')

def adImage(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.session['user']['is_superuser']:
            if request.method == "POST" and 'image' in request.FILES:
                image = request.FILES['image']
                link = request.POST['link']
                title = request.POST['title']
                newadimage = ads(image=image, link=link, title=title, user=accounts.objects.get(email=request.session['user']['email']))
                newadimage.save()
                messages.success(request, "Ad Image added successfully")
                return redirect('home')
            ads_ = ads.objects.all()
            context = {
                'ads': ads_
            }
            return render(request, 'add_ad.html', context)
        else:
            return HttpResponse('You are not allowed to perform this action')
    else:
        return redirect('login2')

def deleteadImage(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.session['user']['is_superuser']:
            adimage = ads.objects.get(id=id)
            if request.method == "POST":
                adimage.delete()
                messages.success(request, 'Ad Image deleted successfully')
                return redirect('home')
            context = {
                'adImage': adimage,
            }
            return render(request, 'delete_ad.html', context)
        else:
            return HttpResponse('You are not allowed to perform this action')
    else:
        return redirect('login2')

def adVideo(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.session['user']['is_superuser']:
            if request.method == "POST" and 'video' in request.FILES:
                video = request.FILES['video']
                newvideoad = advideo(video=video, user=accounts.objects.get(email=request.session['user']['email']))
                newvideoad.save()
                messages.success(request, "Ad Video added successfully")
                return redirect('home')
            advideos = advideo.objects.all()
            context = {
                'advideos': advideos,
            }
            return render(request, 'adVideo_add.html', context)
        else:
            return HttpResponse('You are not allowed to perform this action')
    else:
        return redirect('login2')

def deleteadVideo(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.session['user']['is_superuser']:
            video = advideo.objects.get(id=id)
            if request.method == "POST":
                video.delete()
                messages.success(request, "Ad Video deleted successfully")
                return redirect('home')
            context = {
                'adVideo': video
            }
            return render(request, 'delete_adVideo.html', context)
        else:
            return HttpResponse('You are not allowed to perform this action')
    else:
        return redirect('login2')