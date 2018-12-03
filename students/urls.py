from django.urls import path
from . import views


urlpatterns = [
    path('registro/', views.add_user, name='registro'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    # path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('registro/', views.add_user, name='student_registration'),
    path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', views.StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<pk>/', views.StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<pk>/<module_id>/', views.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
]