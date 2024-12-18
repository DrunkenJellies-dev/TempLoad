from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from store.sitemaps import StaticViewSiteMap

sitemaps = {
    'static': StaticViewSiteMap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
