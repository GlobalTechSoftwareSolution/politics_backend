from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
from .serializers import UserSerializer, UserRegistrationSerializer, UserApprovalSerializer, PendingInfoSerializer, ActiveInfoSerializer
from .models import PendingInfo, ActiveInfo

def require_admin(func):
    """Decorator to require admin privileges (password-based, no cookies/tokens)"""
    def wrapper(request, *args, **kwargs):
        # Get password from request data
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password required for admin operations'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get superuser (we know the superuser email)
        try:
            user = User.objects.get(email='superuser@gmail.com')
        except User.DoesNotExist:
            return Response({'error': 'Superuser not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verify password
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user has admin privileges
        if not user.is_user and not user.is_superuser:
            return Response({'error': 'Admin privileges required'}, status=status.HTTP_403_FORBIDDEN)
        
        return func(request, user, *args, **kwargs)
    return wrapper

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully. Please wait for approval.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    """User login endpoint - Simple password authentication"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        if not user.is_approved:
            return Response({
                'error': 'Account not approved yet. Please contact admin for approval.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'note': 'Simple password authentication - no cookies or tokens'
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_user_profile(request):
    """Get current user profile - Requires password"""
    password = request.data.get('password')
    if not password:
        return Response({'error': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email='superuser@gmail.com')
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'message': 'User profile retrieved successfully',
            'user': UserSerializer(user).data,
            'note': 'Password-based authentication working'
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@require_admin
def approve_user(request, user, user_id):
    """Approve a user (Admin only) - Session based, no JWT"""
    # Only superusers can approve users and make them admins
    if not user.is_superuser:
        return Response({
            'error': 'Only superusers can approve users'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        target_user = User.objects.get(id=user_id)
        target_user.approve_user(approved_by=user)
        return Response({
            'message': f'User {target_user.email} has been approved and made admin',
            'user': UserSerializer(target_user).data
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@require_admin
def get_pending_users(request, user):
    """Get list of users waiting for approval (Admin only) - Session based, no JWT"""
    # Only superusers and admins can view pending users
    if not user.can_approve_users():
        return Response({
            'error': 'Only superusers and admins can view pending users'
        }, status=status.HTTP_403_FORBIDDEN)
    
    pending_users = User.objects.filter(is_approved=False)
    serializer = UserSerializer(pending_users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def protected_endpoint(request):
    """Example protected endpoint that only approved users can access"""
    # For now, just return a simple response without authentication
    return Response({
        'message': 'Welcome to the protected area!',
        'note': 'Authentication removed - no JWT tokens required'
    })

@api_view(['POST'])
def submit_info(request):
    """Submit information for approval"""
    # For regular users, just require email and password
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_approved:
        return Response({'error': 'Account not approved yet'}, status=status.HTTP_403_FORBIDDEN)
    
    # Handle both JSON and multipart form data (for file uploads)
    if request.content_type and 'multipart/form-data' in request.content_type:
        # Multipart form data (file upload)
        serializer = PendingInfoSerializer(data=request.data)
    else:
        # JSON data
        serializer = PendingInfoSerializer(data=request.data)
    
    if serializer.is_valid():
        # Check if user is superuser or admin - if so, approve directly
        if user.can_approve_users():
            # Superuser/admin: Create ActiveInfo directly
            active_info = ActiveInfo.objects.create(
                heading=serializer.validated_data['heading'],
                description=serializer.validated_data['description'],
                image=serializer.validated_data.get('image'),
                submitted_by=user,
                approved_by=user,
                approved_at=timezone.now()
            )
            return Response({
                'message': 'Information submitted and approved directly (admin privilege)',
                'active_info': ActiveInfoSerializer(active_info).data
            }, status=status.HTTP_201_CREATED)
        else:
            # Regular user: Create PendingInfo
            pending_info = serializer.save(submitted_by=user)
            return Response({
                'message': 'Information submitted successfully for approval',
                'pending_info': PendingInfoSerializer(pending_info).data
            }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@require_admin
def get_pending_info(request, user):
    """Get all pending information (Admin only)"""
    
    pending_info = PendingInfo.objects.filter(status='pending').order_by('-submitted_at')
    serializer = PendingInfoSerializer(pending_info, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_active_info(request):
    """Get all active/approved information (Available to all approved users)"""
    # For regular users, just require email and password
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_approved:
        return Response({'error': 'Account not approved yet'}, status=status.HTTP_403_FORBIDDEN)
    
    active_info = ActiveInfo.objects.all().order_by('-approved_at')
    serializer = ActiveInfoSerializer(active_info, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@require_admin
def approve_info(request, user, info_id):
    """Approve pending information (Admin only)"""
    try:
        pending_info = PendingInfo.objects.get(id=info_id, status='pending')
        pending_info.approve(approved_by=user)
        return Response({
            'message': 'Information approved successfully',
            'pending_info': PendingInfoSerializer(pending_info).data
        })
    except PendingInfo.DoesNotExist:
        return Response({'error': 'Pending information not found or already processed'}, status=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@require_admin
def reject_info(request, user, info_id):
    """Reject pending information (Admin only)"""
    try:
        pending_info = PendingInfo.objects.get(id=info_id, status='pending')
        pending_info.reject(rejected_by=user)
        return Response({
            'message': 'Information rejected successfully',
            'pending_info': PendingInfoSerializer(pending_info).data
        })
    except PendingInfo.DoesNotExist:
        return Response({'error': 'Pending information not found or already processed'}, status=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def get_my_submissions(request):
    """Get current user's submissions"""
    # For regular users, just require email and password
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_approved:
        return Response({'error': 'Account not approved yet'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get pending submissions
    pending_submissions = PendingInfo.objects.filter(submitted_by=user).order_by('-submitted_at')
    pending_serializer = PendingInfoSerializer(pending_submissions, many=True)
    
    # Get approved submissions
    approved_submissions = ActiveInfo.objects.filter(submitted_by=user).order_by('-approved_at')
    approved_serializer = ActiveInfoSerializer(approved_submissions, many=True)
    
    return Response({
        'pending_submissions': pending_serializer.data,
        'approved_submissions': approved_serializer.data
    })
