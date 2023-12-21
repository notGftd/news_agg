from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('scrape1/', views.scrape1, name="scrape1"),
    path('znbc/', views.site1, name="site1"),
    path('scrape2/', views.scrape2, name="scrape2"),
    path('zambianobserver/', views.site2, name="site2"),
    path('scrape3/', views.scrape3, name="scrape3"),
    path('lusakatimes/', views.site3, name="site3"),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
]