
from django.contrib import admin
import debug_toolbar
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views

from core.customer import views as customer_views
from core.courier import views as courier_views, apis as courier_apis

customer_urlpatterns = [
    path('',customer_views.home, name='home'),
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




    path('api/jobs/available/',courier_apis.available_jobs_api, name="available-jobs-api"),
    path('api/jobs/current/<id>/update/',courier_apis.current_job_api, name="current-job-update-api")



]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('',views.home),

    path('sign-in/', auth_views.LoginView.as_view(template_name='sign-in.html')),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='/')),
    path('sign-up/',views.sign_up),

    path('customer/', include((customer_urlpatterns, 'customer'))),
    path('courier/',include((courier_urlpatterns, 'courier'))),

    path('__debug__/', include(debug_toolbar.urls)),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

