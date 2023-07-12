from django.urls import path
from grading_app import views 

urlpatterns = [
    path('comodities/', views.CommodityListAPIView.as_view(), name='commodity_list'),
    path('commodity/create/', views.CommodityCreateAPIView.as_view(), name='commodity_create'),
    path('commodity/<int:pk>/update', views.CommodityUpdateAPIView.as_view(), name='commodity_update'),
    path('commodity/<int:pk>/delete', views.CommodityDeleteAPIView.as_view(), name='commodity_delete'),
    path('parameters/', views.ParameterListAPIView.as_view(), name='parameter_list'),
    path('parameters/<int:pk>/', views.ParameterListAPIView.as_view(), name='parameter_detail'),
    path('parameter/create/', views.ParameterCreateAPIView.as_view(), name='parameter_create'),
    path('parameter/<int:pk>/update', views.ParameterUpdateAPIView.as_view(), name='parameter_update'),
    path('parameter/<int:pk>/delete', views.ParameterDeleteAPIView.as_view(), name='parameter_delete'),
    path('commodity/grade_create', views.CommodityGradeCreateAPIView.as_view(), name='commodity_grade_create'),
    path('commodity/grades', views.CommodityGradeListAPIView.as_view(), name='commodity_grade_list'),
    path('commodity/grade/<int:pk>/', views.CommodityGradeDetailAPIView.as_view(), name='commodity_grade_detail'),
    path('commodity/grade/<int:pk>/update/', views.CommodityGradeUpdateAPIView.as_view(), name='commodity_grade_update'),
    
    ]
