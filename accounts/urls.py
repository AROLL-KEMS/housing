from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [

    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),

    # path('accounts/login/', views.login_view, name="login"),
    path('accounts/register/', views.register, name="register"),
    path('accounts/verify/', views.verify_otp, name="verify_otp"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)