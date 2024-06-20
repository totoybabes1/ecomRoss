from django.contrib import admin
from django.urls import path, include
from.import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include ('cart.urls')),
    path('payment/', include ('payment.urls')),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
