from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from posts.views import *
from posts import views


urlpatterns = [
    path('', home_page_view),
    path('home/', home_page_view),
    path('admin/', admin.site.urls),
    path('clup/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),#new
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),#new
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),  #new
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('contact_us/', contact_page_view),
    path('about_us/', about_us_page_view),
    path('signin/', signup_signin_page_view, name='customer_login'),
    path('signout/', signout_page_view, name='customer_sign_out'),
    path('business_sign_in/',business_login_view),
    path('business_sign_up/',business_signup_view),
    path('reset/', forgot_password_view),
    path('control_panel/', control_panel_view),
    path('signup/', customer_signup_view, name='customer_signup_view'),
    path('profile_setting/', profile_setting_view),
    path('please_login/', please_login_view),
    path('line_up/', line_up_view),
    path('store_details/', store_details_view),
    path('leave_line/', leave_line_view),
    path('my_business_scheduled/', my_business_scheduled_view),
    path('customer_schedule/', customer_schedule_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

