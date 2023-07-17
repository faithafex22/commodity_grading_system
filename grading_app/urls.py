from django.urls import path
from grading_app import views 

urlpatterns = [
    path('commodities/', views.CommodityListAPIView.as_view(), name='commodity_list'),
    path('commodity/create/', views.CommodityCreateAPIView.as_view(), name='commodity_create'),
    path('Commodity/<int:pk>/', views.CommodityDetailAPIView.as_view(), name='commodity_detail'),
    path('commodity/<int:pk>/update', views.CommodityUpdateAPIView.as_view(), name='commodity_update'),
    path('commodity/<int:pk>/delete', views.CommodityDeleteAPIView.as_view(), name='commodity_delete'),
    path('parameters/', views.ParameterListAPIView.as_view(), name='parameter_list'),
    path('parameter/<int:pk>/', views.ParameterDetailAPIView.as_view(), name='parameter_detail'),
    path('parameter/create/', views.ParameterCreateAPIView.as_view(), name='parameter_create'),
    path('parameter/<int:pk>/update', views.ParameterUpdateAPIView.as_view(), name='parameter_update'),
    path('parameter/<int:pk>/delete', views.ParameterDeleteAPIView.as_view(), name='parameter_delete'),
    path('commodities/<str:commodity_name>/grade_create/', views.CommodityGradeCreateAPIView.as_view(), name='commodity_grade_create'),
    path('commodities/<str:commodity_name>/grades', views.CommodityGradeListAPIView.as_view(), name='commodity_grade_list'),
    path('commodities/<str:commodity_name>/grade/<int:pk>/', views.CommodityGradeDetailAPIView.as_view(), name='commodity_grade_detail'),
    path('commodities/<str:commodity_name>/grade/<int:pk>/update/', views.CommodityGradeUpdateAPIView.as_view(), name='commodity_grade_update'),
    
]