"""
URLs для приложения myshop.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
  ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# if settings.DEBUG::  Этот код выполняется только в режиме отладки
#(когда settings.DEBUG равно True).
    # * urlpatterns += static(...):  Добавляет URL-шаблоны для обработки
    # статических файлов к списку urlpatterns.
        # * settings.MEDIA_URL:  Это URL-префикс для статических файлов
        #(например, /media/).
        # * settings.MEDIA_ROOT:  Это путь к папке, где хранятся статические файлы.
        