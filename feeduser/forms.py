from django import forms

from .models import FeedUser


class FeedUserForm(forms.ModelForm):
    class Meta:
        model = FeedUser
        fields = ["username", "about", "is_local"]


    def __init__(self, *args, **kwargs):
        super(FeedUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['is_local'].widget.attrs['readonly'] = True