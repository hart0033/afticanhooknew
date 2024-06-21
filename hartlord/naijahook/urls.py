from django.urls import include, path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_view
from django.conf.urls.static import static


urlpatterns = [
    path('userview_post/<int:id>', views.userview_post, name='userview_post'),
    path('userview_post/<int:id>', views.userview_video, name='userview_post'),
    path('report/<int:id>/', views.report_post, name='report_post'),
    path('verify/<int:id>', views.verify_post, name='verify_post'),
    path('verify_video/<int:id>', views.verify_video, name='verify_video'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('view_post/<int:id>', views.view_post, name='view_post'),
    path('view_video/<int:id>', views.view_video, name='view_video'),
    path('view_videos/<int:id>', views.view_videos, name='view_videos'),
    path('myvideo/<int:id>', views.myvideo, name='myvideo'),
    path('delete_post/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('delete_video/<int:id>/', views.delete_video, name='delete_video'),
    path('edit_postads/<int:id>/edit/', views.edit_postads, name='edit_postads'),
    path('edit_video/<int:id>/edit/', views.edit_video, name='edit_video'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('', views.home, name='home'),
    path('videos/', views.videos, name='videos'),
    path('signin/', views.signin, name='signin'),
    path('useraccount/', views.useraccount, name='useraccount'),
    path('uservideos/', views.uservideos, name='uservideos'),
    path('signup/', views.signup, name='signup'),
    path('post/', views.post, name='post'),
    path('postvideo/', views.postvideo, name='postvideo'),
    path('signout/', views.signout, name='sigout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset/confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    
    
    
    path('password_reset', auth_view.PasswordResetView.as_view(template_name="hookup/password_reset.html"), name='password_reset'),
    path('password_reset_sent', auth_view.PasswordResetDoneView.as_view(template_name="hookup/password_reset_done.html"), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="hookup/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete', auth_view.PasswordResetCompleteView.as_view(template_name="hookup/password_reset_complete.html"), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)