from rest_framework import generics, status
from rest_framework.response import Response
from .models import FamilyGroup, Membership
from .serializers import FamilyGroupSerializer, MembershipSerializer
from drf_yasg.utils import swagger_auto_schema

# View for listing all family groups
class FamilyGroupListAPIView(generics.ListAPIView):
    queryset = FamilyGroup.objects.all()
    serializer_class = FamilyGroupSerializer

    @swagger_auto_schema(operation_description="Retrieve all family groups", responses={200: FamilyGroupSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        family_groups = self.get_queryset()
        if not family_groups.exists():
            response_data = {
                'status': 404,
                'success': False,
                'message': 'No family groups found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(family_groups, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

# View for creating a new family group
class FamilyGroupCreateAPIView(generics.CreateAPIView):
    queryset = FamilyGroup.objects.all()
    serializer_class = FamilyGroupSerializer

    @swagger_auto_schema(operation_description="Create a new family group", request_body=FamilyGroupSerializer, responses={201: FamilyGroupSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Family group successfully created',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'status': 400,
            'success': False,
            'message': 'Validation Error',
            'errors': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific family group by its ID
class FamilyGroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FamilyGroup.objects.all()
    serializer_class = FamilyGroupSerializer

    @swagger_auto_schema(operation_description="Retrieve a family group", responses={200: FamilyGroupSerializer})
    def get(self, request, *args, **kwargs):
        try:
            family_group = self.get_object()
        except FamilyGroup.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Family group not found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(family_group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update a family group", request_body=FamilyGroupSerializer, responses={200: FamilyGroupSerializer})
    def put(self, request, *args, **kwargs):
        try:
            family_group = self.get_object()
        except FamilyGroup.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Family group not found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(family_group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a family group", responses={204: 'No Content'})
    def delete(self, request, *args, **kwargs):
        try:
            family_group = self.get_object()
        except FamilyGroup.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Family group not found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        family_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# View for listing all memberships
class MembershipListAPIView(generics.ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    @swagger_auto_schema(operation_description="Retrieve all memberships", responses={200: MembershipSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        memberships = self.get_queryset()
        if not memberships.exists():
            response_data = {
                'status': 404,
                'success': False,
                'message': 'No memberships found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(memberships, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

# View for creating a new membership
class MembershipCreateAPIView(generics.CreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    @swagger_auto_schema(operation_description="Create a new membership", request_body=MembershipSerializer, responses={201: MembershipSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Membership successfully created',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'status': 400,
            'success': False,
            'message': 'Validation Error',
            'errors': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific membership by its ID
class MembershipDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    @swagger_auto_schema(operation_description="Retrieve a membership", responses={200: MembershipSerializer})
    def get(self, request, *args, **kwargs):
        try:
            membership = self.get_object()
        except Membership.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Membership not found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(membership)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Update a membership", request_body=MembershipSerializer, responses={200: MembershipSerializer})
    def put(self, request, *args, **kwargs):
        try:
            membership = self.get_object()
        except Membership.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Membership not found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(membership, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a membership", responses={204: 'No Content'})
    def delete(self, request, *args, **kwargs):
        try:
            membership = self.get_object()
        except Membership.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Membership not found'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
