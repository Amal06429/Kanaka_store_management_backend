from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import User, UploadedFile
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer,
    UploadedFileSerializer, FileUploadSerializer
)


class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint"""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Serialize user data
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register endpoint for creating new users"""
    serializer = UserCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Serialize user data
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """Get current logged-in user"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User CRUD operations"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        user = self.request.user
        if user.role == 'admin':
            # Admin can see all users
            return User.objects.all()
        else:
            # Regular users can only see themselves
            return User.objects.filter(id=user.id)
    
    def get_serializer_class(self):
        """Use different serializer for create action"""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Admin required for create, update, destroy"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def regular_users(self, request):
        """Get all regular users (non-admin)"""
        if request.user.role != 'admin':
            return Response(
                {'detail': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        users = User.objects.filter(role='user')
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class UploadedFileViewSet(viewsets.ModelViewSet):
    """ViewSet for UploadedFile CRUD operations"""
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        print(f"Files list requested by: {request.user.username} (role: {request.user.role})")
        queryset = self.get_queryset()
        print(f"Total files in queryset: {queryset.count()}")
        serializer = self.get_serializer(queryset, many=True)
        print(f"Files being returned: {len(serializer.data)}")
        return Response(serializer.data)
    
    def get_queryset(self):
        user = self.request.user
        queryset = UploadedFile.objects.all()
        
        if user.role != 'admin':
            queryset = queryset.filter(user=user)
        
        user_id = self.request.query_params.get('user_id', None)
        if user_id and user.role == 'admin':
            queryset = queryset.filter(user_id=user_id)
        
        date = self.request.query_params.get('date', None)
        if date:
            queryset = queryset.filter(uploaded_at__date=date)
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(heading__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-uploaded_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FileUploadSerializer
        return UploadedFileSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to ensure JSON error responses"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("==== CREATE METHOD ERROR ====")
            print("Error:", str(e))
            print("Error type:", type(e).__name__)
            import traceback
            traceback.print_exc()
            print("==== CREATE METHOD ERROR END ====")
            
            # Return JSON error instead of letting Django return HTML
            return Response(
                {
                    'detail': f'Upload failed: {str(e)}',
                    'error_type': type(e).__name__
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # 🔥 UPDATED UPLOAD DEBUG FUNCTION WITH ERROR HANDLING
    def perform_create(self, serializer):
        print("==== FILE UPLOAD DEBUG START ====")

        try:
            file_obj = serializer.save(user=self.request.user)

            print("User:", self.request.user.username)
            print("Storage class:", type(file_obj.file.storage))
            print("File name:", file_obj.file.name)
            
            try:
                print("File URL:", file_obj.file.url)
            except Exception as url_error:
                print("File URL error:", str(url_error))

            try:
                exists = file_obj.file.storage.exists(file_obj.file.name)
                print("Exists in storage:", exists)
            except Exception as e:
                print("Storage check error:", str(e))

            print("==== FILE UPLOAD DEBUG END ====")
            
        except Exception as e:
            print("==== FILE UPLOAD ERROR ====")
            print("Error:", str(e))
            print("Error type:", type(e).__name__)
            import traceback
            traceback.print_exc()
            print("==== FILE UPLOAD ERROR END ====")
            raise  # Re-raise to be handled by DRF

    # 🔥 DELETE FROM R2 + DB
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        print("==== DELETE DEBUG START ====")
        print("Deleting file:", instance.file.name)

        if instance.file:
            storage = instance.file.storage
            file_name = instance.file.name

            try:
                if storage.exists(file_name):
                    storage.delete(file_name)
                    print("File removed from R2:", file_name)
                else:
                    print("File not found in R2:", file_name)
            except Exception as e:
                print("Delete error:", str(e))

        instance.delete()

        print("==== DELETE DEBUG END ====")

        return Response(
            {"detail": "File deleted successfully"},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def my_files(self, request):
        files = UploadedFile.objects.filter(user=request.user)
        serializer = self.get_serializer(files, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        
        if user.role == 'admin':
            total_files = UploadedFile.objects.count()
            total_users = User.objects.filter(role='user').count()
        else:
            total_files = UploadedFile.objects.filter(user=user).count()
            total_users = 1
        
        return Response({
            'total_files': total_files,
            'total_users': total_users,
        })
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        file_obj = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['pending', 'verified', 'rejected']:
            return Response(
                {'detail': 'Invalid status. Must be pending, verified, or rejected.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file_obj.status = new_status
        file_obj.save()
        
        serializer = self.get_serializer(file_obj)
        return Response(serializer.data)



