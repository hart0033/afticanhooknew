from django.contrib import admin
from .models import Report, postads, slide,slide2,slide3,review,adsvideos, verify_Post, videosreview, State, Service
# Register your models here.
admin.site.register(postads)
admin.site.register(slide)
admin.site.register(slide2)
admin.site.register(slide3)
admin.site.register(review)
admin.site.register(videosreview)
admin.site.register(adsvideos)
admin.site.register(State)
admin.site.register(Service)
admin.site.register(Report)
admin.site.register(verify_Post)