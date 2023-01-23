from django import forms

# how to convert a forms.py to an html document?

class register(forms.Form):
    name=forms.CharField(max_length=20)
    phone=forms.IntegerField()
    image=forms.FileField()


# e mail send cheyyan ayakanda alude mail id and message venam.
# athinulla class creation.

class contactusform(forms.Form):
    Name=forms.CharField(max_length=30)
    Email=forms.EmailField()
    Message=forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows':3,'col':30}))
    # widget---> valya text area messagenu kittan vendi use cheyunu.
    # text rea yile rand attributes ahn rows and colomns