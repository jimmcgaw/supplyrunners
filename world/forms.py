from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('kind', 'display_name', 'is_publicly_visible',
            'contact_preference', 'contact_details')

    USER_KIND_CHOICES = (
        (UserProfile.VOLUNTEER, "I'm a resident volunteering to help at-risk residents"),
        (UserProfile.SHELTERED, "I'm a sheltered at-risk resident looking for volunteer assistance"),
    )
    kind = forms.ChoiceField(widget=forms.RadioSelect(), required=True, choices=USER_KIND_CHOICES)

    CONTACT_PREFERENCE_CHOICES = (
        (UserProfile.EMAIL, 'Email'),
        (UserProfile.PHONE, 'Phone'),
    )
    display_name = forms.CharField(required=True,
        help_text="This is the name we will display to other users on the site.")

    is_publicly_visible = forms.BooleanField(help_text="Uncheck this if you don't want to appear to other users on the site.")
    contact_preference = forms.ChoiceField(choices=CONTACT_PREFERENCE_CHOICES, required=True)

    contact_details = forms.CharField(required=True,
        help_text="An email or phone number at which people may reach you. (This will be hidden behind a reCAPTCHA so bots cannot scrape it.)")