from django.contrib import admin
from django.urls import path, include

from dailyrentflat.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dailyrentflat.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = page_not_found

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Посуточно квартиры от собственника"
