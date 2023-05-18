from django.urls import path
from . import views


urlpatterns = [
    path('api/snippets/',views.Overview.as_view(),name='overview'),
    path('api/snippet/<int:id>/',views.Details.as_view(),name='detail'),
    path('api/snippet/create/',views.Create.as_view(),name='create'),
    path('api/snippet/<int:snippetid>/update/',views.Update.as_view(),name='update'),
    path('api/snippet/<int:snippetid>/delete/',views.Delete.as_view(),name='delete'),
    path('api/tag/',views.TagList.as_view(),name='taglist'),
    path('api/tag/<int:tagid>/',views.TagDetails.as_view(),name='tagdetails'),
    path('',views.ShowAllApiDoc.as_view(),name='apilist'),
    
]
