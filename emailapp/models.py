from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    # user enn parayunnath oru onetoone field ahn... athin connection User lek ahn
    auth_token=models.CharField(max_length=100)
    # oro user register avumbozhum oru authentication token generate avum...ath save cheyan ahn auth_token variable
    is_verified=models.BooleanField(default=False)
    # mailil varunna tokenil click avumbozhe verified user avu...athvare varification false ayit set cheyum
    created_at=models.DateTimeField(auto_now_add=True)
    # nammalu register avunna date and time save chyth vekan olla field.
    # auto_now_add---> OS il ninn correct ayt nammal register aya cirrect data and time ee fieldlot keyeran

