from django import forms
from django.contrib.auth.models import User
from .models import Report, Service, postads,review,adsvideos, verify_Post, verify_video, videosreview
from phonenumber_field.formfields import PhoneNumberField

class postads_form(forms.ModelForm):
    number = PhoneNumberField(region="NG", widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px;','placeholder': 'Phone Number',
        
        }))
    whatsapp = PhoneNumberField(region="NG", required=False, widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px;','placeholder': 'Whatsapp Number',
        }))
    telegram = PhoneNumberField(region="NG", required=False, widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px;','placeholder': 'Telegram Number',
        }))
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = postads
        fields=( "name", "bio","email","number","whatsapp","telegram","State", "shot_time", "full_night","main","picture1","picture2","picture3","services")
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                'placeholder': 'Your Display Name'
                }),
            'bio': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 700px;',
                'placeholder': 'About Your Posts'
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                'placeholder': 'Email'
                },),
            'State': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            'shot_time': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Amount',
                'style': 'max-width: 600px;',
                }),
            'full_night': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Amount',
                'style': 'max-width: 600px;',
                }),
            'main': forms.FileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            'picture1': forms.ClearableFileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            'picture2': forms.ClearableFileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            'picture3': forms.ClearableFileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            }
class adsvideos_form(forms.ModelForm):
    
    number = PhoneNumberField(region="NG",required=False, widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px;','placeholder': 'Phone Number',
        
        }))
    whatsapp = PhoneNumberField(region="NG", required=False, widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px;','placeholder': 'Whatsapp Number',
        }))
    telegram = PhoneNumberField(region="NG", required=False, widget=forms.TextInput(attrs={'class': 'form-control','style': 'width: 350px;','placeholder': 'Telegram Number',
        }))
    class Meta:
        model = adsvideos
        fields=( "name", "bio","email","number","whatsapp","telegram","State", "shot_time", "full_night","video")
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                'placeholder': 'Your Display Name'
                }),
            'bio': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 700px;',
                'placeholder': 'About Your Posts'
                }),
            'email': forms.EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                'placeholder': 'Email'
                },),
            'State': forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            'shot_time': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Amount',
                'style': 'max-width: 600px;',
                }),
            'full_night': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': 'Amount',
                'style': 'max-width: 600px;',
                }),
            'video': forms.ClearableFileInput(attrs={
                'class': "form-control",
                'style': 'max-width: 600px;',
                }),
            }                
class review_form(forms.ModelForm):
    class Meta:
        model = review
        fields = ("name", "body")
        widgets = {
                'name': forms.TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Name',
                    }),
                'body': forms.Textarea(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Your Review',
                    }),
                }
        
class videoreview_form(forms.ModelForm):
    class Meta:
        model = videosreview
        fields = ("name", "body")
        widgets = {
                'name': forms.TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Name',
                    }),
                'body': forms.Textarea(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Your Review',
                    }),
                }
    
    
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'reason']
        widgets = {
                'name': forms.TextInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Name',
                    }),
                'reason': forms.Textarea(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Your Review',
                    }),
                }
        
class verifyForm(forms.ModelForm):
    class Meta:
        model = verify_Post
        fields = ['Picture_With_ID', 'ID_Front']
        widgets = {
                'Picture_With_ID': forms.ClearableFileInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Name',
                    }),
                'ID_Front': forms.ClearableFileInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Your Review',
                    }),
                }
class verifyvideoForm(forms.ModelForm):
    class Meta:
        model = verify_video
        fields = ['Picture_With_ID', 'ID_Front']
        widgets = {
                'Picture_With_ID': forms.ClearableFileInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Name',
                    }),
                'ID_Front': forms.ClearableFileInput(attrs={
                    'class': "form-control",
                    'style': 'max-width: 300px;',
                    'placeholder': 'Your Review',
                    }),
                }
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')
