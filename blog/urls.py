from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name='home'),
    path('blog/', views.post_list, name='blog'),
    path('blog/<title>', views.category_view, name='cat'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]

urlpatterns += [
                   # ... the rest of your URLconf goes here ...
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
