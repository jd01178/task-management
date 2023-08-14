from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# views.py
from rest_framework.views import APIView

from accounts.api.serializers import EmployeeSerializer
from accounts.models import Employee
from core.permissions import IsEmployeeUser
from .serializers import ChangePasswordSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsEmployeeUser]

    def post(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")

            if not user.check_password(old_password):
                return Response({"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({"error": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            #
            # # If you're using DRF Token Authentication
            # Token.objects.filter(user=user).delete()

            return Response({"message": "Password successfully changed."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        employee, _ = Employee.objects.get_or_create(user=self.request.user)
        return employee

    def perform_update(self, serializer):
        serializer.save()
