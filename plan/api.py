from helper import helper
from .serializers import PlanSerializer
from .models import Plan
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
)


# Create Plan
# post
# /v1/plan/create
class CreatePlan(CreateAPIView):
    permission_classes = [helper.permission.IsAdmin]
    serializer_class = PlanSerializer

    def post(self, request):
        helper.check_parameters(request, ["name", "price", "description"])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return helper.createResponse(helper.message.MODULE_STORE_SUCCESS("Plan"))


# Read Plans
# get
# /v1/plan/read
class ReadPlans(ListAPIView):
    http_method_names = ["get"]

    def list(self, request):
        queryset = Plan.objects.filter().order_by("price")

        return helper.createResponse(
            helper.message.MODULE_LIST("Plan"), PlanSerializer(
                queryset, many=True).data
        )


# Update Plan
# put
# /v1/plan/update/<str:id>
class UpdatePlan(UpdateAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def update(self, request, id):
        helper.check_parameters(request, ["name", "price", "description"])
        plan = helper.checkRecord(id, Plan, "Plan")

        plan.name = request.data["name"]
        plan.price = request.data["price"]
        plan.description = request.data["description"]
        plan.save()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Plan", "updated")
        )


# Delete Plan
# delete
# /v1/plan/delete/<str:id>
class DeletePlan(DestroyAPIView):
    permission_classes = [helper.permission.IsAdmin]

    def delete(self, request, id):
        plan = helper.checkRecord(id, Plan, "Plan")
        plan.delete()

        return helper.createResponse(
            helper.message.MODULE_STATUS_CHANGE("Plan", "deleted")
        )
