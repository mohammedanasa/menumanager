
from django.contrib import admin
import debug_toolbar

from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views, consumers
from django.views.generic import TemplateView

from restaurant import views as restaurant_views
from accounts import views as api_auth_views
from api import views as api_endpoint_views
from core.customer import views as customer_views
from core.courier import views as courier_views, apis as courier_apis
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'menus', api_endpoint_views.MenuViewSet, basename='menu')

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
    path('loc/', restaurant_views.restaurant_list, name="rest-list"),
    path('loc/<lid>/', restaurant_views.get_restaurant, name='restaurant'),
    #----------------------------------------TEST------------------------------------------#
    #Create menu for a single restaurant
    #path('loc/<lid>/menu/', restaurant_views.create_menu_location, name='menu-location'),
    #Update menu for a location
    #path('loc/<lid>/<menuid>/update/', restaurant_views.update_menu, name='menu-update-location'),

    path('loc/<lid>/update_address/', restaurant_views.update_restaurant_address, name="update_address"),

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

    #Menu Global
    path('menus/', restaurant_views.menu_list_view, name='menu_list'),
    path('menu/create/', restaurant_views.menu_create_view, name='menu_create'),
    path('menu/<uuid:menuid>/update/', restaurant_views.menu_update_view, name='menu_update'),
    
    #Not working

    #----------------------------------------TESTING---------------------------------------------------#
    #Create menu for a location
    
    #path('menus/', restaurant_views.menu_list, name='all-menus'),
    #path('<lid>/store1/', restaurant_views.restaurant_menus, name='store-cm'),




]

api_urlpatterns = [

    path("auth/signup/", api_auth_views.SignUpView.as_view(),name="signupapi"),
    path("auth/signin/", api_auth_views.LoginViewAPI.as_view(),name="lognapi"),
    path("auth/jwt/create/", TokenObtainPairView.as_view(),name="jwt"),
    path("auth/jwt/refresh/", TokenRefreshView.as_view(),name="jwtrefresh"),
    path("auth/jwt/verify/", TokenVerifyView.as_view(),name="jwtverify"),

    path("category/",api_endpoint_views.CategoryListCreateView.as_view(), name="apicategory"), 
    path("current-user/",api_endpoint_views.get_posts_for_current_user , name="apicategorycurrentuser"),  
    path("menu/",api_endpoint_views.MenuViewSet, name="apicategory"), 







]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('',restaurant_views.dashboard),
    path('firebase-messaging-sw.js', (TemplateView.as_view(template_name="firebase-messaging-sw.js", content_type= "application/javascript",))),


    path('sign-in/', auth_views.LoginView.as_view(template_name='sign-in.html')),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='/')),
    path('sign-up/',views.sign_up),

    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/',include((courier_urlpatterns, 'courier'))),
    path('restaurant/',include((restaurant_urlpatterns,'restaurant'))),
    path('api/', include((api_urlpatterns, 'api'))),

    #Test
    path('test/', include(router.urls)),
    path('woo/',restaurant_views.fetch_products),

    





    




    path('__debug__/', include(debug_toolbar.urls)),
    
]


websocket_urlpatterns = [
    path('ws/jobs/<job_id>/', consumers.JobConsumer.as_asgi())
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

