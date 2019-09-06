from django.urls import path, include
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
# from .views import SnippetHighlight, SnippetDetail, SnippetList, UserList, UserDetail, api_root
from .views import SnippetViewSet, UserViewSet, api_root


# snippet_list = SnippetViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
#
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
#
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })
#
# urlpatterns = [
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
#     path('snippets/<int:pk>/highlight', snippet_highlight, name='snippet-highlight'),
#
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>', user_detail, name='user-detail'),
#
#     path('', api_root),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)

# Create a router and register out viewsets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet)
router.register(r'users', UserViewSet)

schema_view = get_schema_view(title="Pastebin API")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
]

# urlpatterns = format_suffix_patterns(urlpatterns)