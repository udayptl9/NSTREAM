from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Language, Category, Video, Subcategory, Notify, Upcoming
from app.models import advideo, ads, theme
from accounts.models import accounts, GuestSettings, AdSettings, Page_settings
from django.contrib import messages
from json import dumps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import smtplib

def upcoming_trailer(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']['is_superuser']:
        upcomings = Upcoming.objects.all()
        if request.method == "POST":
            title = request.POST['title']
            for i in upcomings:
                if i.title == title:
                    messages.error(request, 'Upcoming already exists')
                    return redirect('upcoming')
            thumbnail = request.FILES['thumbnail']
            trailer = request.FILES['trailer']
            newUpcoming = Upcoming(title=title, thumbnail=thumbnail, video=trailer)
            newUpcoming.save()
            messages.success(request, 'Upcoming added successfully')
            return redirect('home')
        context = {
            'upcomings': upcomings,
            'ads': ads.objects.all()[:4],
        }
        return render(request, 'videos/upcoming_form.html', context)
    else:
        messages.error(request, 'You are not allowed to perform this action')
        return redirect('home')

def upcoming_view(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        upcoming = Upcoming.objects.get(id=id)
        if request.method == "POST":
            response = {}
            if request.POST.get('action') == 'noity_me':
                try:
                    notify = Notify.objects.get(email=request.session['user']['email'], upcoming=upcoming)
                    notify.delete()
                    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.ehlo()
                        smtp.login('udayptl9@gmail.com', 'ahwoahunadxwpbvl')
                        subject = 'Notify Request'
                        body = f'Your request for notifying movie release { upcoming.title } has been cancelled \n\nTeam NSTREAM'
                        message = f'Subject: {subject} \n\n{body}'
                        smtp.sendmail('udayptl9@gmail.com', request.session['user']['email'], message)
                    response['text'] = 'already'
                except:
                    newNotify = Notify(email=request.session['user']['email'], upcoming=upcoming)
                    newNotify.save()
                    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.ehlo()
                        smtp.login('udayptl9@gmail.com', 'ahwoahunadxwpbvl')
                        subject = 'Notify Request'
                        body = f'Thank you for showing interest in {upcoming.title}. \n\nWe will notify you when full movie is released \n\nTeam NSTREAM'
                        message = f'Subject: {subject} \n\n{body}'
                        smtp.sendmail('udayptl9@gmail.com', request.session['user']['email'], message)
                    response['text'] = 'added'
                return JsonResponse(response)
        context = {
            'upcoming': upcoming,
            'ads': ads.objects.all()[:4],
        }
        try:
            notify = Notify.objects.get(email=request.session['user']['email'], upcoming=upcoming)
            context['notify'] = notify
        except:
            pass
        return render(request, 'videos/upcoming_view.html', context)
    else:
        return redirect('login')

def video_add(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.method == "POST":
            if request.POST.get('action') == 'get_subcategory':
                response = {}
                category = Category.objects.get(category=request.POST.get('category'))
                subcategories = Subcategory.objects.filter(category = category)
                subcat = [i.subcategory for i in subcategories]
                response['text'] = 'true'
                response['subcategories'] = subcat
                return JsonResponse(response)
            title = request.POST['title']
            description = request.POST['description']
            language = Language.objects.get(language=request.POST['language'])
            category = Category.objects.get(category=request.POST['category'])
            subcategory = Subcategory.objects.get(subcategory=request.POST['subcategory'])
            thumbnail = request.FILES['thumbnail']
            video = request.FILES['video']
            upcoming = request.POST['upcoming']
            if upcoming != 'No Upcomings':
                upcoming_object = Upcoming.objects.get(title=upcoming)
                notifies = Notify.objects.filter(upcoming=upcoming_object)
                user_email = request.session['user']['email']
                account = accounts.objects.get(email = user_email)
                newVideo = Video(title=title, description=description, language=language, category=category, subcategory = subcategory, thumbnail=thumbnail, video=video, video_ads='',  user=account)
                try:
                    if request.session['user']['is_superuser']:
                        newVideo.save()
                        video_notify = Video.objects.get(title=title)
                        for notify in notifies:
                            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                                smtp.ehlo()
                                smtp.starttls()
                                smtp.ehlo()
                                smtp.login('udayptl9@gmail.com', 'ahwoahunadxwpbvl')
                                subject = f'{upcoming_object.title} Released'
                                body = f'Your interested movie {upcoming_object.title} has been released. \n\nTo Watch the movie now. Please Visit: http://localhost:8000/video_view/{video_notify.id}  \n\nTeam NSTREAM'
                                message = f'Subject: {subject} \n\n{body}'
                                smtp.sendmail('udayptl9@gmail.com', notify.email, message)
                                notify.email_sent = True
                                notify.save()
                        video = Video.objects.get(title=title)
                        response = {}
                        response['text'] = video.id
                        return JsonResponse(response)
                    else:
                        messages.error(request, 'You are not allowed to perform this action')
                except Exception as e:
                    messages.error(request, f'Error: {e}')
                    return redirect('home')
            else:
                user_email = request.session['user']['email']
                account = accounts.objects.get(email = user_email)
                newVideo = Video(title=title, description=description, language=language, category=category, subcategory = subcategory, thumbnail=thumbnail, video=video, video_ads='',  user=account)
                try:
                    if request.session['user']['is_superuser']:
                        newVideo.save()
                except:
                    messages.error(request, f'Error: {e}')
                    return redirect('home')
        if request.session['user']['is_superuser'] or request.session['user']['addvideo']:
            upcomings = Upcoming.objects.all()
            context = {
                'languages': Language.objects.all(),
                'categories': Category.objects.all(),
                'ads': ads.objects.all(),
                'upcomings': upcomings,
            }
            return render(request, 'videos/video_add.html', context)
        else:
            messages.error(request, 'You are not allowed to perform this action')
            return redirect('home')
    else:
        return redirect('login2')

def video_ads(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            if request.session['user']['is_superuser'] or request.session['user']['addvideo']:
                if request.method == "POST":
                    if request.POST.get('action') == 'video_ads':
                        response_Text = {}
                        beginnerAd = request.POST.get('beginnerAds')
                        beginnerAd = " ".join(beginnerAd.split())
                        middleAds_text = request.POST.get('middleAds')
                        times_text = request.POST.get('times')
                        times_text = [i for i in times_text.split(" ")]
                        times = []
                        for i in times_text:
                            if i != "":
                                times.append(i)
                        middleAds = [i for i in middleAds_text.split("\n")]
                        middleAds_list = []
                        for i in range(0, len(middleAds)):
                            text = " ".join(middleAds[i].split())
                            if text != "":
                                middleAds_list.append(text)
                        ads = advideo.objects.all()
                        query_text = "custom slug "
                        if beginnerAd != "":
                            for ad in ads:
                                if ad.video.name == beginnerAd:
                                    query_text += f'{ad.id} 0:00 slug '
                        for i in range(0, len(middleAds_list)):
                            time_text = times[i]
                            for ad in ads:
                                if ad.video.name == middleAds_list[i]:
                                    query_text += f'{ad.id} {time_text} slug '
                        video = Video.objects.get(id=id)
                        video.video_ads = str(query_text)
                        video.save()
                        response_Text['text'] = 'true'
                        return JsonResponse(response_Text)
                    action = request.POST['action']
                    if action == 'random':
                        ads = advideo.objects.all()
                        query_text = "random slug"
                        video = Video.objects.get(id=id)
                        video.video_ads = str(query_text)
                        video.save()
                        return redirect('home')
                    elif action == 'single':
                        ad_single = request.POST['ad']
                        video = Video.objects.get(id=id)
                        query_text = "single "
                        ads = advideo.objects.all()
                        for ad in ads:
                            if ad.video.name == ad_single:
                                query_text += f'{ad.id} slug '
                        video.video_ads = str(query_text)
                        video.save()
                        return redirect('home')
                    elif action == 'noads':
                        video = Video.objects.get(id=id)
                        video.video_ads = 'noads'
                        video.save()
                        return redirect('home')
                video = Video.objects.get(id=id)
                context = {
                    'video': video,
                    'ads': advideo.objects.all()
                }
                return render(request, 'videos/video_ads.html', context)
        except Exception as e:
            messages.error(request, f' Error: {e}')
            return redirect('home')
    else:
        return redirect('login2')


def video_update(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            if request.session['user']['is_superuser'] or request.session['user']['addvideo']:
                video = Video.objects.get(id=id)
                languages = Language.objects.all()
                categories = Category.objects.all()
                subcategories = Subcategory.objects.filter(category=video.category)
                if request.method == "POST":
                    if request.FILES.get('thumbnail') == None:
                        pass
                    else:
                        video_thumbnail = request.FILES['thumbnail']
                        video.thumbnail = video_thumbnail
                    if request.FILES.get('video') == None:
                        pass
                    else:
                        video.video = request.FILES['video']
                    video.title = request.POST['title']
                    video.description = request.POST['description']
                    video.language = Language.objects.get(language=request.POST['language'])
                    video.category = Category.objects.get(category=request.POST['category'])
                    account = accounts.objects.get(email=request.session['user']['email'])
                    video.user = account
                    video.save()
                    messages.success(request, 'Video Updated Successfully!!')
                    return redirect(f'/video_view/{id}/')
                context = {
                    'video': video,
                    'title': video.title,
                    'languages': languages,
                    'categories': categories,
                    'subcategories': subcategories,
                    'ads': ads.objects.all(),
                }
                return render(request, 'videos/video_update.html', context)
        except:
            messages.error(request, 'You are not allowed to perform this action')
            return redirect('home')
    else:
        return redirect('login2')

def video_delete(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            if request.session['user']['is_superuser'] or request.session['user']['addvideo']:
                video = Video.objects.get(id=id)
                if request.method == "POST":
                    video.delete()
                    messages.success(request, 'Video deleted successfully')
                    return redirect('home')
                context = {
                    'video': video,
                    'title': video.title,
                    'ads': ads.objects.all()
                }
                return render(request, 'videos/video_delete.html', context)
        except:
            messages.success(request, 'Video deleted successfully')
            return redirect('home')
    else:
        return redirect('login2')

def video_manage(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            if request.session['user']['is_superuser']:
                videos = Video.objects.all()
                context = {
                    'videos': videos,
                    'title': 'Manage Videos',
                    'ads': ads.objects.all()
                }
                return render(request, 'videos/video_manage.html', context)
        except:
            messages.error(request, "You are not allowed to perform this action")
            return redirect('home')
    else:
        return redirect('login2')

def view_all(request, category):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            category = Category.objects.get(category=category)
        except:
            return render(request, '404.html')
        categories = Subcategory.objects.filter(category=category)
        video_list = []
        videos = Video.objects.all().order_by('-id')
        query = request.GET.get('query')
        if query:
            videos = videos.filter(title__icontains=query)
        for category in categories:
            filter_videos = videos.filter(subcategory=category)
            if len(filter_videos) > 0:
                video_list.append(filter_videos[0:6])
        ads_ = ads.objects.all()
        id_s = [i for i in range(0, len(video_list))]
        context = {
            'videos': video_list,
            'ads': ads_,
            'ids': id_s,
            'slug': 'home',
        }
        return render(request,"videos/view_all.html", context)
    else:
        try:
            server_name = request.GET.get('redirect', False)
            if server_name == 'social':
                guest_setting = GuestSettings.objects.first()
                timer = int(guest_setting.timer)
                request.session['user'] = {'email': 'guest', 'is_verified': True, 'timer': f"{timer*60000}"}
                return redirect(f'/{category}/')
            else:
                messages.error(request, 'Please LOGIN')
                return redirect('login2')
        except:
            return redirect('login2')
                
def sub_view_all(request, category, subcategory):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            subcategory = Subcategory.objects.get(subcategory=subcategory)
        except:
            return render(request, '404.html')
        videos = Video.objects.filter(subcategory=subcategory)
        per_page = Page_settings.objects.first()
        query = request.GET.get('query')
        if query:
            videos = videos.filter(title__icontains=query)
        paginator = Paginator(videos, per_page=int(per_page.per_page))
        page_number = request.GET.get('page', 1)
        try:
            page_object = paginator.page(page_number)
            page_number = int(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
            page_number = 1
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)
            page_number = paginator.num_pages
        context = {
            'videos': page_object.object_list,
            'title': subcategory.subcategory,
            'ads': ads.objects.all(),
            'paginator': paginator,
            'page_number': page_number,
            'per_page': int(per_page.per_page),
            'slug': 'home',
        }
        return render(request, 'videos/view_all_subcategory.html', context)
    else:
        try:
            server_name = request.GET.get('redirect', False)
            if server_name == 'social':
                guest_setting = GuestSettings.objects.first()
                timer = int(guest_setting.timer)
                request.session['user'] = {'email': 'guest', 'is_verified': True, 'timer': f"{timer*60000}"}
                return redirect(f'/{category}/{subcategory}/')
            else:
                messages.error(request, "Please LOGIN")
                return redirect('login2')
        except:
            return redirect('login2')

def video_view(request, id):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        ad_timer = AdSettings.objects.first()
        ad_timer = int(ad_timer.ad_timing)
        video = Video.objects.get(id=id)
        videos = Video.objects.filter(category=video.category).order_by('-id')[:6]
        video_ads_text = video.video_ads
        if video_ads_text == "noads":
            context = {
                'video': video,
                'title': video.title,
                'ads': ads.objects.all(),
                'videos': videos
            }
            return render(request, 'videos/video_view.html', context)
        video_ads_list = [i for i in video_ads_text.split('slug')]
        ad_type_list = [i for i in video_ads_list[0].split(" ")]
        ad_type = " ".join(ad_type_list[0].split())
        if ad_type == "random":
            video_ads = advideo.objects.all()
            ads_list = {'ad_urls': []}
            for ad in video_ads:
                ads_list['ad_urls'].append(ad.video.url)
            jsonData = dumps(ads_list)
            context = {
                'video': video,
                'title': video.title,
                'ad_type': 'random',
                'ad_video': jsonData,
                'ads': ads.objects.all(),
                'ad_timer': ad_timer,
                'videos': videos
            }
        elif ad_type == "single":
            ad_video_id = " ".join(ad_type_list[1].split())
            ad_video_id = int(ad_video_id)
            ad_video = advideo.objects.get(id=ad_video_id)
            context = {
                'video': video,
                'title': video.title,
                'ad_type': 'single',
                'ad_video': ad_video,
                'ads': ads.objects.all(),
                'ad_timer': ad_timer,
                'videos': videos
            }
        elif ad_type == "custom":
            ad_list_custom = video_ads_list[1:]
            ads_list_custom = []
            for i in ad_list_custom:
                text = " ".join(i.split())
                if text != "":
                    ads_list_custom.append(text)
            ads_final_list = {'urls': [], 'times': []}
            for i in ads_list_custom:
                ad_id = [j for j in i.split(" ")][0]
                ad_id = int(ad_id)
                time = [j for j in i.split(" ")][1]
                time_list = [j for j in time.split(":")]
                time_sec = int(time_list[0]) * 60 + int(time_list[1])
                ad = advideo.objects.get(id=ad_id)
                ads_final_list['urls'].append(ad.video.url)
                ads_final_list['times'].append(time_sec)
            jsonData = dumps(ads_final_list)
            context = {
                'video': video,
                'title': video.title,
                'ad_type': 'custom',
                'ad_video': jsonData,
                'ads': ads.objects.all(),
                'videos': videos
            }
        else:
            context = {
                'video': video,
                'title': video.title,
                'ads': ads.objects.all(),
                'videos': videos
            }
        return render(request, 'videos/video_view.html', context)
    else:
        try:
            server_name = request.GET.get('redirect', False)
            if server_name == 'social':
                guest_setting = GuestSettings.objects.first()
                timer = int(guest_setting.timer)
                request.session['user'] = {'email': 'guest', 'is_verified': True, 'timer': f"{timer*60000}"}
                return redirect(f'/video_view/{id}')
            else:
                return redirect('login2')
        except:
            return redirect('login2')

def category_add(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.method == 'POST':
            category = request.POST['category']
            try:
                category_test = Category.objects.get(category=category)
                return render(request, 'videos/category_add.html', {'message': 'true'})
            except:
                newCategory = Category(category=category)
                if request.session['user']['is_superuser'] or request.session['user']['addcategory']:
                    newCategory.save()
                    messages.success(request, 'Category added successfully')
                    return redirect('home')
                else:
                    return HttpResponse('You are not allowed to perform this action')
        try:
            if request.session['user']['is_superuser'] or request.session['user']['addcategory']:
                categories = Category.objects.all()
                context = {
                    'ads': ads.objects.all(),
                    'categories': categories,
                }
                return render(request, 'videos/category_add.html', context)
        except:
            messages.error(request, 'You are not allowed to perform this action')
            return redirect('home')
    else:
        return redirect('login2')

def subcategory_add(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        try:
            if request.session['user']['is_superuser'] or request.session['user']['addcategory']:
                categories = Category.objects.all()
                if request.method == "POST":
                    category = request.POST['category']
                    subcategory = request.POST['subcategory']
                    image = request.FILES['image']
                    try:
                        subcategory_test = Subcategory.objects.get(subcategory = subcategory)
                        return render(request, 'videos/subcategory_add.html', {'message': 'true', 'categories': categories})
                    except:
                        newSubCategory = Subcategory(category=Category.objects.get(category = category), subcategory = subcategory, image=image)
                        newSubCategory.save()
                        messages.success(request, "Sub Category added successfully")
                        return redirect('home')
                subcategories = Subcategory.objects.all()
                context = {
                    'subcategories': subcategories,
                    'categories': categories,
                    'title': 'Add Category',
                    'ads': ads.objects.all(),
                }
                return render(request, 'videos/subcategory_add.html', context)
        except:
            messages.error(request, 'You are not allowed to perform this action')
            return redirect('home')
    else:
        return redirect('login2')

def language_add(request):
    try:
        test_user = request.session['user']
    except:
        return redirect('logout2')
    if request.session['user']:
        if request.method == 'POST':
            language = request.POST['language']
            try:
                language_test = Language.objects.get(language=language)
                messages.error(request, "Language already existed")
                return redirect('language_add')
            except:
                newLanguage = Language(language=language)
                try:
                    if request.session['user']['is_superuser'] or request.session['user']['addlanguage']:
                        newLanguage.save()
                        messages.success(request, "Language added successfully")
                        return redirect('home')
                except:
                    messages.error(request, 'You are not allowed to perform this action')
                    return redirect('home')
        try:
            if request.session['user']['is_superuser'] or request.session['user']['addlanguage']:
                languages = Language.objects.all()
                context = {
                    'title': 'Add Language',
                    'languages': languages,
                    'ads': ads.objects.all()
                }
                return render(request, 'videos/language_add.html', context)
        except:
            messages.error(request, "You are not allowed to perform this action")
            return redirect('home')
    else:
        return redirect('login2')