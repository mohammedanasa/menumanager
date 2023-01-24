
from django.contrib import admin
import debug_toolbar
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views, consumers
from django.views.generic import TemplateView

from restaurant import views as restaurant_views
from core.customer import views as customer_views
from core.courier import views as courier_views, apis as courier_apis

customer_urlpatterns = [
    path('',customer_views.customerHome, name='dashboard'),
    path('profile/', customer_views.profile_page, name='profile'),
    path('payment-method/', customer_views.payment_method_page, name='payment-method'),
    path('create-job/', customer_views.create_job_page, name='create-job'),

    path('jobs/current/', customer_views.current_jobs_page, name='current-jobs'),
    path('jobs/archived/', customer_views.archived_jobs_page, name='archived-jobs'),
    path('jobs/<job_id>/', customer_views.job_page, name='job'),    
]

courier_urlpatterns = [
    path('',courier_views.home, name='home'),
    path('jobs/available/',courier_views.available_jobs_page, name='available-jobs'),
    path('jobs/available/<id>/',courier_views.available_job_page, name='available-job'),
    path('jobs/current/', courier_views.current_job_page, name='current-job'),
    path('jobs/current/<id>/take-photo/', courier_views.current_job_take_photo_page, name='current-job-take-photo'),
    path('jobs/complete/', courier_views.job_complete_page, name='job-complete'),
    path('jobs/archived/', courier_views.archived_jobs_page, name='archived-jobs'),
    path('profile/', courier_views.profile_page, name='profile'),
    path('payout-method/', courier_views.payout_method_page, name='payout-method'),
    
    path('api/jobs/available/',courier_apis.available_jobs_api, name="available-jobs-api"),
    path('api/jobs/current/<id>/update/',courier_apis.current_job_api, name="current-job-update-api"),
    path('api/fcm-token/update/',courier_apis.fcm_token_update_api, name="fcm-token-update-api"),
]


restaurant_urlpatterns = [
    path("", restaurant_views.dashboard, name="rest-dashboard"),

    path('product/', restaurant_views.create_or_update_product, name='create-product'),
    path('products/', restaurant_views.ProductList.as_view(), name='products'),
    path('product/<slug:pid>/', restaurant_views.create_or_update_product, name='update-product'),
    path('product/delete-product/<slug:pid>/', restaurant_views.delete_product, name='delete-product'),

    path('categories/', restaurant_views.CategoryList.as_view(), name='categories'),
    path('category/', restaurant_views.create_or_update_category, name='create-category'),
    path('category/<slug:cid>/', restaurant_views.create_or_update_category, name='update-category'),
    path('category/delete-category/<slug:cid>/', restaurant_views.delete_category, name='delete-category'),

    path('modifier-groups/', restaurant_views.MGList.as_view(), name='mgs'),
    path('modifier-group/', restaurant_views.MGCreate.as_view(), name='create-mg'),
    path('modifier-group/<slug>/', restaurant_views.MGUpdate.as_view(), name='update-mg'),
    path('modifier-group/delete-modifier-group/<slug>/', restaurant_views.MGDelete.as_view(), name='delete-mg'),

    path('modifiers/', restaurant_views.ModifierList.as_view(), name='modifiers'),
    path('modifier/', restaurant_views.ModifierCreate.as_view(), name='create-modifier'),
    path('modifier/<slug>/', restaurant_views.ModifierUpdate.as_view(), name='update-modifier'),
    path('modifier/delete-modifier/<slug>/', restaurant_views.ModifierDelete.as_view(), name='delete-modifier'),


]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('',views.home),
    path('firebase-messaging-sw.js', (TemplateView.as_view(template_name="firebase-messaging-sw.js", content_type= "application/javascript",))),


    path('sign-in/', auth_views.LoginView.as_view(template_name='sign-in.html')),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='/')),
    path('sign-up/',views.sign_up),

    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/',include((courier_urlpatterns, 'courier'))),
    path('restaurant/',include((restaurant_urlpatterns,'restaurant'))),

    path('__debug__/', include(debug_toolbar.urls)),
    
]


websocket_urlpatterns = [
    path('ws/jobs/<job_id>/', consumers.JobConsumer.as_asgi())
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

