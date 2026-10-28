"""agrishiled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from agrishiled import settings
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login1', views.login1),
    path('logouts',views.logouts),
    path('login_post', views.login_post),
    path('adm_add_expert', views.adm_add_expert),
    path('adm_add_exp_post', views.adm_add_exp_post),
    path('adm_edit_expert/<id>', views.adm_edit_expert),
    path('adm_edit_expert_post/<id>', views.adm_edit_expert_post),
    path('adm_dlt_expert/<id>', views.adm_dlt_expert),
    path('adm_view_expert', views.adm_view_expert),
    path('adm_view_farmer', views.adm_view_farmer),
    path('adm_view_complaint', views.adm_view_complaint),
    path('adm_send_reply/<id>', views.adm_send_reply),
    path('adm_send_reply_post/<id>', views.adm_send_reply_post),
    path('adm_changepsswd', views.adm_changepsswd),
    path('adm_changepsswd_post', views.adm_changepsswd_post),
    path('adm_home',views.adm_home),
    #expert================
    path('exp_add_tip',views.exp_add_tip),
    path('exp_add_tip_post',views.exp_add_tip_post),
    path('exp_home',views.exp_home),
    path('exp_edit_tip/<id>', views.exp_edit_tip),
    path('exp_edit_tip_post/<id>', views.exp_edit_tip_post),
    path('exp_delete_tip/<id>', views.exp_delete_tip),
    path('exp_view_tip', views.exp_view_tip),
    path('exp_add_news', views.exp_add_news),
    path('exp_add_news_post', views.exp_add_news_post),
    path('exp_edit_news/<id>', views.exp_edit_news),
    path('exp_delete_news/<id>', views.exp_delete_news),
    path('exp_edit_news_post/<id>', views.exp_edit_news_post),
    path('exp_view_news', views.exp_view_news),
    path('exp_add_price', views.exp_add_price),
    path('exp_add_price_post', views.exp_add_price_post),
    path('exp_edit_price/<id>', views.exp_edit_price),
    path('exp_edit_price_post/<id>', views.exp_edit_price_post),
    path('exp_delete_price/<id>', views.exp_delete_price),
    path('exp_view_price', views.exp_view_price),
    path('exp_add_subsidy', views.exp_add_subsidy),
    path('exp_edit_subsidy/<id>', views.exp_edit_subsidy),
    path('exp_edit_subsidy_post/<id>', views.exp_edit_subsidy_post),
    path('exp_add_subsidy_post', views.exp_add_subsidy_post),
    path('exp_delete_subsidy/<id>', views.exp_delete_subsidy),
    path('exp_view_subsidy', views.exp_view_subsidy),
    path('exp_add_scheme', views.exp_add_scheme),
    path('exp_add_scheme_post', views.exp_add_scheme_post),
    path('exp_edit_scheme/<id>', views.exp_edit_scheme),
    path('exp_edit_scheme_post/<id>', views.exp_edit_scheme_post),
    path('exp_view_scheme', views.exp_view_scheme),
    path('exp_delete_scheme/<id>', views.exp_delete_scheme),
    path('exp_changepsswd', views.exp_changepsswd),
    path('exp_changepsswd_post', views.exp_changepsswd_post),
    path('', views.index),


    ######################3 USER 3###############################

    path('fregister',views.fregister),
    path('userlogin',views.userlogin),
    path('viewtips',views.viewtips),
    path('viewsubsidydetails',views.viewsubsidydetails),
    path('viewreplay',views.viewreplay),
    path('viewprofile',views.viewprofile),
    path('viewnews',views.viewnews),
    path('viewmarketprocess',views.viewmarketprocess),
    path('viewgovtscheme',views.viewgovtscheme),
    path('sendcomplaint',views.sendcomplaint),
    path('user_getweather',views.user_getweather),
    path('user_sendchat',views.user_sendchat),
    path('user_viewchat',views.user_viewchat),
    path('viewchat_farmer',views.viewchat_farmer),
    path('chatrply',views.chatrply),
    path('chatt/<u>',views.chatt),
    path('chatsnd/<u>',views.chatsnd),
    path('forgotpassword',views.forgotpassword),
    path('forgotpasswordbuttonclick',views.forgotpasswordbuttonclick),
    path('otp',views.otp),
    path('otpbuttonclick',views.otpbuttonclick),
    path('forgotpswdpswed',views.forgotpswdpswed),
    path('forgotpswdpswedbuttonclick',views.forgotpswdpswedbuttonclick),
    path('forgotemail', views.forgotemail),
    path('forgotpass', views.forgotpass),
    path('soil_crop_recommendation', views.soil_crop_recommendation),

    path('crop_predict',views.crop_predict),
    path('flutter_add_chatbot',views.flutter_add_chatbot),
    path('flutter_view_chatbot',views.flutter_view_chatbot),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)