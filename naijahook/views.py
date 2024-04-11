from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.urls import reverse
from hartlord import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from . tokens import generate_tokens
from django.utils.http import urlsafe_base64_encode
from .models import Service, postads, State, slide, slide2,slide3,adsvideos
from .form import PasswordResetForm, ReportForm, adsvideos_form, postads_form, review_form, verifyForm, verifyvideoForm, videoreview_form
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





def home(request):
    s = request.GET.get('State')
    if s == None:
        ads = postads.objects.filter(suspended=False).order_by('-verification')
    else:
        ads = postads.objects.filter(State__State=s, suspended=False,).order_by('-verification')
        
    paginator = Paginator(ads, 10 )  # Show 10 ads per page
    
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
        video = adsvideos.objects.filter(suspended=False).order_by('-verification')
    else:
        video = adsvideos.objects.filter(State__State=s, suspended=False,).order_by('-verification') 
    s = State.objects.all()
    
    paginator = Paginator(video, 10 )  # Show 10 ads per page
    
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
    sl3 = slide3.objects.first()
    sl2 = slide2.objects.first()
    sl = slide.objects.first()
    s = State.objects.all()
    ads = postads.objects.all().order_by('-date_post')
    context = {
    'sl3' : sl3,
    'sl2' : sl2,
    'sl' : sl,
    's' : s,
    'ads': ads,
    }

    if request.method =="POST":
        username = request.POST['username']
        pass1 = request.POST["pass1"]
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, "web/index.html", context)
            else:
                messages.error(request, 'Your account is suspended.')
        else:
            messages.error(request, 'Username or password is incorrect')
            return redirect('signin')
    
    return render (request, 'hookup/login.html')

def signup_client(request):
    
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, 'USERNAME HAS BEEN USED PLEASE CREATE A NEW ONE')
            return redirect('signup')
            
        if User.objects.filter(email=email):
            messages.error(request, 'YOU CANT USER THIS EMAIL AGAIN IT HAS BEEN USED BEFORE')
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, 'USERNAME MOST BE NUMBER AND LETTLERS ONLY') 
            return redirect('signup')
        if pass1 == pass2:
            
          client = User.objects.create_user(username, email, pass1)
          User.is_client = True
          client.first_name = fname
          client.last_name = lname
          client.is_active = True
          client.save()
          
          subject = "WELCOME TO NIAJAHOOKUP "
          message = "HELLO " + client.first_name + '!!/n'+ "YOUR ACCOUNT WAS SUCCESSFULLY CREATED '!!/n' "
          from_email = settings.EMAIL_HOST_USER
          to_list = {client.email}
          send_mail(subject, message, from_email, to_list, fail_silently=True)
          
          return redirect('signin')
      
      
        else:
          messages.error(request, "PASSWORD DON'T MATCH")
          return redirect('signup')
    return render (request, 'hookup/signup2.html')


def signup(request):
    
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, 'USERNAME HAS BEEN USED PLEASE CREATE A NEW ONE')
            return redirect('signup')
            
        if User.objects.filter(email=email):
            messages.error(request, 'YOU CANT USER THIS EMAIL AGAIN IT HAS BEEN USED BEFORE')
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, 'USERNAME MOST BE NUMBER AND LETTLERS ONLY') 
            return redirect('signup')
        if pass1 == pass2:
            
          myuser = User.objects.create_user(username, email, pass1)
          User.is_myuser = True
          myuser.first_name = fname
          myuser.last_name = lname
          myuser.is_active = True
          myuser.save()
          
          subject = "WELCOME TO NIAJAHOOKUP "
          message = "HELLO " + myuser.first_name + '!!/n'+ "YOUR ACCOUNT WAS SUCCESSFULLY CREATED '!!/n' "
          from_email = settings.EMAIL_HOST_USER
          to_list = {myuser.email}
          send_mail(subject, message, from_email, to_list, fail_silently=True)
          
          return redirect('signin')
      
      
        else:
          messages.error(request, "PASSWORD DON'T MATCH")
          return redirect('signup')
    return render (request, 'hookup/signup.html')

@login_required(login_url="/signin")
def useraccount(request):
    user = request.user
    user_ads = postads.objects.filter(author=request.user).order_by('-date_post')
    
    paginator = Paginator(user_ads, 10 )  # Show 10 ads per page
    
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
    
    paginator = Paginator(user_video, 10 )  # Show 10 ads per page
    
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
         messages.success(request, 'Your ads has been posted successfuly')
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
         messages.success(request, 'Your ads has been posted successfuly')
         return redirect('uservideos')
    else:
        form = adsvideos_form()
    return render (request, 'hookup/postvideos.html', {'form':form})

def view_videos(request, id):       
    video = adsvideos.objects.get(id=id)
    video.view_count += 1
    video.save()
    if request.method == 'POST':
       form = videoreview_form(request.POST)
       if form.is_valid():
         videoreview = form.save(commit=False)
         videoreview.video = video
         videoreview.save()
         form = videoreview_form()
    else:
        form = videoreview_form()
    return render(request, 'web/view_videos.html', {'video': video, 'form':form})


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
    return render(request, 'web/view_post.html', {'ads': ads, 'form':form, 'serv': serv, 'ads_formatted_view_count': ads_formatted_view_count})
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
        messages.success(request, 'YOUR POST HAS BEEN DELETED. ')
        return redirect('useraccount')

    return render(request, 'hookup/delete_post.html', {'user_ads': user_ads})
@login_required(login_url="/signin")
def delete_video(request, id):
    user_video = get_object_or_404(adsvideos, id=id)
    if request.method == 'POST':
        user_video.delete()
        messages.success(request, 'YOUR POST HAS BEEN DELETED. ')
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
            messages.success(request, 'Post reported successfully.')
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
            return redirect('view_video', id=id)
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
            messages.success(request, 'Your password has been updated.')
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
                reset_link = f"http://example.com/reset/{user.id}"
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
    