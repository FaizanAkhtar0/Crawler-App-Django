"""Crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from Core.views import user_link_post, admin_dashboard, admin_crawl_status, admin_url_status, \
    admin_crawled_data, get_updated_queue, start_crawler, stop_crawler, get_updated_dequeue

urlpatterns = [
    path('super_admin/', admin.site.urls),
    path('admin/', admin_dashboard, name="dashboard"),
    path('admin_crawl_status/', admin_crawl_status, name="crawl_status"),
    path('admin_crawl_status/queue/', get_updated_queue),
    path('admin_url_status/dequeue/', get_updated_dequeue),
    path('admin_crawl_status/start_queue/', start_crawler),
    path('admin_crawl_status/stop_queue/', stop_crawler),
    path('admin_crawl_data/', admin_crawled_data, name="crawl_data"),
    path('admin_url_status/', admin_url_status, name="crawl_url"),
    path('', user_link_post, name='user_url_post')
]
