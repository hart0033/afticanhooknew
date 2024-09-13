from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from hartlord import settings
from django.core.mail import BadHeaderError , EmailMessage , send_mail 
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from . tokens import generate_tokens
from django.utils.http import urlsafe_base64_encode
from .models import Service, postads, State, slide, slide2,slide3,adsvideos
from .form import PasswordResetForm, ReportForm, adsvideos_form, postads_form, review_form, verifyForm, verifyvideoForm, videoreview_form
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.conf import settings

# Initialize Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY['CLOUD_NAME'],
    api_key=settings.CLOUDINARY['API_KEY'],
    api_secret=settings.CLOUDINARY['API_SECRET']
)


def home(request):
    s = request.GET.get('State')
    if s == None:
        ads = postads.objects.filter(suspended=False).order_by('-verification', '-date_post')
    else:
        ads = postads.objects.filter(State__State=s, suspended=False,).order_by('-verification', '-date_post')
        
    paginator = Paginator(ads, 9 )  # Show 10 ads per page
    
    page_number = request.GET.get('page')
    try:
        ads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        ads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        ads = paginator.page(paginator.num_pages)
    
    sl3 = slide3.objects.first()
    sl2 = slide2.objects.first()
    sl = slide.objects.first()
    s = State.objects.all()
    context = {
    'sl3' : sl3,
    'sl2' : sl2,
    'sl' : sl,
    's' : s,
    'ads': ads,
  }
    return render (request, 'web/index.html' , context,)
def videos(request):
    s = request.GET.get('State')
    if s == None:
        video = adsvideos.objects.filter(suspended=False).order_by('-verification', '-date_post')
    else:
        video = adsvideos.objects.filter(State__State=s, suspended=False,).order_by('-verification', '-date_post')
    s = State.objects.all()
    
    paginator = Paginator(video, 9 )  # Show 10 ads per page
    
    page_number = request.GET.get('page')
    try:
        video = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        video = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        video = paginator.page(paginator.num_pages)
        
    context = {
    's' : s,
    'video': video,
  }
    return render (request, 'web/video.html' , context,)

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        pass1 = request.POST.get('pass1')
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.POST.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account is suspended.')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    next_url = request.GET.get('next', 'home')
    return render(request, 'hookup/login.html', {'next': next_url})


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # Prepare the initial context with form data
        context = {
            'username': username,
            'fname': fname,
            'lname': lname,
            'email': email,
            'pass1': pass1,
            'pass2': pass2,
        }
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'USERNAME HAS BEEN USED PLEASE CREATE A NEW ONE')
            return render(request, 'hookup/signup.html', context)
            
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'YOU CAN\'T USE THIS EMAIL AGAIN IT HAS BEEN USED BEFORE')
            return render(request, 'hookup/signup.html', context)
        
        # Check if username is alphanumeric
        if not username.isalnum():
            messages.error(request, 'USERNAME MUST BE NUMBER AND LETTERS ONLY') 
            return render(request, 'hookup/signup.html', context)
        
        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "PASSWORDS DON'T MATCH")
            return render(request, 'hookup/signup.html', context)
        
        # Create user if all checks pass
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
          
        # Send welcome email
        subject = "WELCOME TO AFRICANHOOKUP.COM"
        message = f"HELLO {myuser.first_name}!!\nYOUR ACCOUNT WAS SUCCESSFULLY CREATED!!\n YOUR CAN NOW POST ADS AND POST VIDEOS SOON YOU CAN MAKE MONEY FROM EVERY VIDEO YOU POST "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]  # Use a list instead of a set for email recipients
        send_mail(subject, message, from_email, to_list, fail_silently=True)
         
        user = authenticate(username=username, password=pass1) 
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("home")
      
    return render(request, 'hookup/signup.html')


@login_required(login_url="/signin")
def useraccount(request):
    user = request.user
    user_ads = postads.objects.filter(author=request.user).order_by('-date_post')
    
    paginator = Paginator(user_ads, 9 )  # Show 10 ads per page
    
    page_number = request.GET.get('page')
    try:
        user_ads = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        user_ads = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        user_ads = paginator.page(paginator.num_pages)
    return render (request, 'web/myaccount.html', {'user_ads':user_ads, 'user':user})

@login_required(login_url="/signin")
def uservideos(request):
    user = request.user
    user_video = adsvideos.objects.filter(author=request.user).order_by('-date_post')
    
    paginator = Paginator(user_video, 9 )  # Show 10 ads per page
    
    page_number = request.GET.get('page')
    try:
        user_video = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        user_video = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        user_video = paginator.page(paginator.num_pages)
    return render (request, 'web/myvideos.html', {'user':user, 'user_video':user_video})

def signout(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/signin")
def post(request,):
    if request.method == 'POST':
       form = postads_form(request.POST, request.FILES)
       if form.is_valid():
         postads = form.save(commit=False)
         postads.author = request.user
         postads.save()
         return redirect('useraccount')
    else:
        form = postads_form()
    return render (request, 'hookup/post.html', {'form':form})

#postvideos
@login_required(login_url="/signin")
def postvideo(request,):
    if request.method == 'POST':
       form = adsvideos_form(request.POST, request.FILES)
       if form.is_valid():
         postads = form.save(commit=False)
         postads.author = request.user
         postads.save()
         return redirect('uservideos')
    else:
        form = adsvideos_form()
    return render (request, 'hookup/postvideos.html', {'form':form})

def view_videos(request, id):       
    video = adsvideos.objects.get(id=id)
    video.view_count += 1
    video.save()
     # Fetch related videos by name
    related_videos = list(adsvideos.objects.filter(name=video.name).exclude(id=id)[:6])
    related_count = len(related_videos)
    if related_count == 0:
        related_videos = list(adsvideos.objects.filter(author=video.author).exclude(id=id)[:6])
    # If fewer than 6 related videos by name, add videos by author to complete the list
    elif related_count < 6:
        additional_videos = adsvideos.objects.filter(author=video.author).exclude(id__in=[v.id for v in related_videos] + [video.id])[:6 - related_count]
        related_videos.extend(additional_videos)

    if request.method == 'POST':
       form = videoreview_form(request.POST)
       if form.is_valid():
         videoreview = form.save(commit=False)
         videoreview.video = video
         videoreview.save()
         form = videoreview_form()
    else:
        form = videoreview_form()
    return render(request, 'web/view_videos.html', {
        'video': video,
        'form': form,
        'related_videos': related_videos
    })

@login_required(login_url="/signin")
def myvideo(request, id):       
    video = adsvideos.objects.get(id=id)
    video.save()
    return render(request, 'web/myvideo.html', {'video': video})

@login_required(login_url="/signin")
def edit_video(request, id):
    video = adsvideos.objects.get(id=id)
    form = adsvideos_form(instance=video)
    if request.method == 'POST':
        form = adsvideos_form(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('myvideo', id=id)
    else:
        form = adsvideos_form(instance=video)

    return render(request, 'hookup/edit_video.html', {'form': form})


def format_view_count(view_count):
    if view_count < 1000:
        return str(view_count)
    elif view_count < 1000000:
        return '{:.1f}k'.format(view_count / 1000)
    else:
        return '{:.1f}M'.format(view_count / 1000000)
def view_post(request, id):       
    ads = postads.objects.get(id=id)
    ads_formatted_view_count = format_view_count(ads.view_count)
    ads.view_count +=1
    ads.save()
    related_posts = postads.objects.filter(State=ads.State).exclude(id=ads.id)[:4]
    serv = Service.objects.all()
    if request.method == 'POST':
       form = review_form(request.POST)
       if form.is_valid():
         review = form.save(commit=False)
         review.ads = ads
         review.save()
         form = review_form()
    else:
        form = review_form()
    return render(request, 'web/view_post.html', {'ads': ads, 'form':form, 'serv': serv, 'ads_formatted_view_count': ads_formatted_view_count, 'related_posts': related_posts})
@login_required(login_url="/signin")
def userview_post(request, id):
    user_ads = postads.objects.get(id=id)
    user_ads_formatted_view_count = format_view_count(user_ads.view_count)
    return render(request, 'hookup/userview_post2.html', {'user_ads':user_ads,'user_ads_formatted_view_count': user_ads_formatted_view_count})
@login_required(login_url="/signin")
def userview_video(request, id):
    user_video = adsvideos.objects.get(id=id)
    user_video_formatted_view_count = format_view_count(user_video.view_count)
    return render(request, 'hookup/userview_post3.html', {'user_video':user_video,'user_video_formatted_view_count': user_video_formatted_view_count})

def view_video(request, id):       
    ads = postads.objects.get(id=id)
    ads_formatted_view_count = format_view_count(ads.view_count)
    if request.method == 'POST':
       form = review_form(request.POST)
       if form.is_valid():
         review = form.save(commit=False)
         review.ads = ads
         review.save()
         form = review_form()
    else:
        form = review_form()
    return render(request, 'web/view_video.html', {'ads': ads, 'form':form,'ads_formatted_view_count': ads_formatted_view_count})

@login_required(login_url="/signin")
def edit_postads(request, id):
    post = postads.objects.get(id=id)
    form = postads_form(instance=post)
    if request.method == 'POST':
        form = postads_form(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('userview_post', id=id)
    else:
        form = postads_form(instance=post)

    return render(request, 'hookup/edit_post.html', {'form': form})
@login_required(login_url="/signin")
def delete_post(request, id):
    user_ads = get_object_or_404(postads, id=id)

    if request.method == 'POST':
        user_ads.delete()
        return redirect('useraccount')

    return render(request, 'hookup/delete_post.html', {'user_ads': user_ads})
@login_required(login_url="/signin")
def delete_video(request, id):
    user_video = get_object_or_404(adsvideos, id=id)
    if request.method == 'POST':
        user_video.delete()
        return redirect('useraccount')

    return render(request, 'hookup/delete_video.html', {'user_video': user_video})
def report_post(request, id):
    ads = postads.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_post = ads
            report.save()
            return redirect('view_post', id=id)  
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('report_post', id=id)
    else:
        form = ReportForm()
    return render(request, 'web/report_post.html', {'form': form, 'ads': ads})
@login_required(login_url="/signin")
def verify_post(request, id):
    user_ads = postads.objects.get(pk=id)
    if request.method == 'POST':
        form = verifyForm(request.POST, request.FILES)
        if form.is_valid():
            verify = form.save(commit=False)
            verify.Post = user_ads
            verify.save()
            messages.success(request, 'Post verification submitted successfully it takes 24 hours for your post to be verified.')
            return redirect('view_post', id=id)
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('verify_post', id=id)
    else:
        form = verifyForm()
    return render(request, 'web/verify_post.html', {'form': form, 'user_ads': user_ads})
@login_required(login_url="/signin")
def verify_video(request, id):
    user_video = adsvideos.objects.get(pk=id)
    if request.method == 'POST':
        form = verifyvideoForm(request.POST, request.FILES)
        if form.is_valid():
            verify = form.save(commit=False)
            verify.Post = user_video
            verify.save()
            messages.success(request, 'Post verification submitted successfully it takes 24 hours for your videos to be verified.')
            return redirect('myvideo', id=id)
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('verify_video', id=id)
    else:
        form = verifyForm()
    return render(request, 'web/verify_video.html', {'form': form, 'user_video': user_video})
@login_required(login_url="/signin")
def edit_profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('useraccount')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'hookup/updateaccount.html', {'form': form})
    
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                reset_link = f"http://africanhook.com/reset/{user.id}"
                message = f"Click the following link to reset your password: {reset_link}"
                send_mail('Password Reset', message, settings.DEFAULT_FROM_EMAIL, [email])
                
                return render(request, 'password_reset_done.html')
            except User.DoesNotExist:
                pass  # Handle invalid email address error here
    
    else:
        form = PasswordResetForm()
    
    return render(request, 'hookup/password_reset.html', {'form': form})



class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = SetPasswordForm

    def get_success_url(self):
        return reverse('password_reset_complete')
def password_reset_done(request):
    return render (request, 'hookup/password_reset_done.html')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Message from {name} <{email}>\n\n{message}"

        email_message = EmailMessage(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,  # Use your authorized email address here
            ['support@africanhook.com'],  # The recipient email address
            reply_to=[email],  # Add the user's email as a reply-to address
        )

        try:
            email_message.send(fail_silently=False)
            return render(request, 'web/success.html')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}')

    return render (request, 'web/contact.html')

def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_encode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_tokens.check_token(myuser, token):
        myuser.is_active
        myuser.save()
        login( request, myuser)
        return redirect('postads')
    else: return render(request, 'activation_fail.html')
    