from django.urls import path
from . import views

urlpatterns = [
    path('user-notes/', views.UserNotesList.as_view()),
    path('published-notes/', views.PublishedNotesList.as_view()),
    path('note/', views.NoteCreate.as_view()),
    path('note/<int:id>/', views.NoteRetrieveUpdateDestroy.as_view()),
]