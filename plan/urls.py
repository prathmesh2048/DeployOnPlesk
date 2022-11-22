from django.urls import path
from .api import CreatePlan, ReadPlans, UpdatePlan, DeletePlan


urlpatterns = [
    path("create", CreatePlan.as_view()),
    path("read", ReadPlans.as_view()),
    path("update/<str:id>", UpdatePlan.as_view()),
    path("delete/<str:id>", DeletePlan.as_view()),
]