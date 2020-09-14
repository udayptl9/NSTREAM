from django.shortcuts import render, redirect
from .models import Subadmin
from django.http import HttpResponse
from app.models import ads
from accounts.models import accounts

def subdomain_add(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']['is_superuser']:
        if request.method == "POST":
            email = request.POST.get('email')
            action = request.POST.get('action', False)
            if action == 'superuser':
                newSubDomain = Subadmin(email=email, superuser=True)
                newSubDomain.save()
                return redirect('subadmin_view')
            else:
                newSubDomain = Subadmin(email=email, superuser=False, addvideo=True, addcategory=True, addlanguage=True)
                newSubDomain.save()
                return redirect('subadmin_view')
        context = {
            'ads': ads.objects.all()
        }
        return render(request, 'subadmin/subadmin_add.html', context)
    else:
        return HttpResponse('You are not allowed to visit this page')

def subadmin_view(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    subadmins = Subadmin.objects.all()
    if len(subadmins) > 0:
        context = {
            'subadmins': subadmins,
            'ads': ads.objects.all()
        }
    else:
        context = {}
    return render(request, 'subadmin/view_all.html', context)

def subadmin_detail(request, subadminid):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']['is_superuser']:
        try:
            subadmin = Subadmin.objects.get(id=subadminid)
            if request.method == 'POST':
                email = request.POST.get('email')
                subadmin.email = email
                action = request.POST.get('action', False)
                if action == 'superuser':
                    subadmin.superuser = True
                    subadmin.addvideo = False
                    subadmin.addcategory = False
                    subadmin.addlanguage = False
                    subadmin.save()
                else:
                    subadmin.superuser = False
                    subadmin.addvideo = True
                    subadmin.addcategory = True
                    subadmin.addlanguage = True
                    subadmin.save()
                return redirect('subadmin_view')
        except Exception as e:
            print(f'error: {e}')
            return HttpResponse(f'Subadmin doesnt exists with id: {subadminid}')
        context = {
                'subadmin': subadmin,
                'ads': ads.objects.all()
            }
        return render(request, 'subadmin/view_one.html', context)
    else:
        return HttpResponse('You are not allowed to visit this page')

def subadmin_delete(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']['is_superuser']:
        subadmin = Subadmin.objects.get(id=id)
        if request.method == "POST":
            subadmin.delete()
            return redirect('subadmin_view')
        context = {
            'email': subadmin.email,
            'ads': ads.objects.all()
        }
        return render(request, 'subadmin/subadmin_delete.html', context)
    else:
        return HttpResponse('You are not allowed to visit this page')