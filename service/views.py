from django.shortcuts import render,get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from service.models import ServiceRequest
from service.serializers import RegisterSerializer,ServiceRequestSerializer


# 1. User Registration
class SignUpView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                
            )

        return Response(
            serializer.errors,
            
        )


# 2. Get Logged-in User
class GetMeView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = RegisterSerializer(request.user)

        return Response(serializer.data)


# 3. List and Create Service Requests
class ServiceRequestListCreateView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        instance = ServiceRequest.objects.filter(
            user=request.user
        )

        serializer = ServiceRequestSerializer(
            instance,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceRequestSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                serializer.data,
                
            )

        return Response(
            serializer.errors,
            
        )


# 4. Retrieve, Update and Delete Own Service Requests
class ServiceRequestDetailView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        return get_object_or_404(
            ServiceRequest,
            pk=pk,
            user=request.user
        )

    def get(self, request, pk):
        instance = self.get_object(request, pk)

        serializer = ServiceRequestSerializer(instance)

        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(request, pk)

        serializer = ServiceRequestSerializer(
            instance,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                
            )

        return Response(
            serializer.errors,
            
        )

    def patch(self, request, pk):
        instance = self.get_object(request, pk)

        serializer = ServiceRequestSerializer(
            instance,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                
            )

        return Response(
            serializer.errors,
            
        )

    def delete(self, request, pk):
        instance = self.get_object(request, pk)
        instance.delete()

        return Response(
            
        )


# 5. Filter by Service Type, Priority and Status
class ServiceRequestFilterView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        instance = ServiceRequest.objects.filter(
            user=request.user
        )

        service_type = request.query_params.get("service_type")
        priority = request.query_params.get("priority")
        status_value = request.query_params.get("status")

        if service_type:
            instance = instance.filter(
                service_type__iexact=service_type.strip()
            )

        if priority:
            instance = instance.filter(
                priority__iexact=priority.strip()
            )

        if status_value:
            instance = instance.filter(
                status__iexact=status_value.strip()
            )

        serializer = ServiceRequestSerializer(
            instance,
            many=True
        )

        return Response(serializer.data)


# 6. Search by Vehicle Number and Model
class ServiceRequestSearchView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        instance = ServiceRequest.objects.filter(
            user=request.user
        )

        vehicle_number = request.query_params.get("vehicle_number")
        vehicle_model = request.query_params.get("vehicle_model")

        if vehicle_number:
            instance = instance.filter(
                vehicle_number__icontains=vehicle_number.strip()
            )

        if vehicle_model:
            instance = instance.filter(
                vehicle_model__icontains=vehicle_model.strip()
            )

        serializer = ServiceRequestSerializer(
            instance,
            many=True
        )

        return Response(serializer.data)


# 7. Pending Service Requests
class PendingServiceRequestView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        instance = ServiceRequest.objects.filter(
            user=request.user
        ).exclude(status="Delivered")

        serializer = ServiceRequestSerializer(
            instance,
            many=True
        )

        return Response(serializer.data)


# 8. Total Count and Status-wise Count
class ServiceRequestCountView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        instance = ServiceRequest.objects.filter(user=request.user)

        total_requests = instance.count()

        status_count = list(instance.values("status").annotate(count=Count("id")).order_by("status"))

        response_data = {
            "total_requests": total_requests,
            "status_count": status_count,
        }

        return Response(response_data)


# 9. High and Critical Service Requests
class ServiceRequestPriorityView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        instance = ServiceRequest.objects.filter(
            user=request.user,
            priority__in=["High", "Critical"]
        )

        serializer = ServiceRequestSerializer(instance,many=True)

        return Response(serializer.data)