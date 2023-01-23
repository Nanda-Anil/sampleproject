from django.urls import path
from .views import *
urlpatterns=[
    path('register/',regis),
    path('email/',email_send),
    path('registration/',registration),
    path('verify/<auth_token>',verify),
#     ee token string and integer mix ayond ahn <> ithil auth token enn kodthekunnath.
#     ivide namak eshtamulla name kodkam..bt ath thanne venam functnl pass chyan
    path('login/',login)
]