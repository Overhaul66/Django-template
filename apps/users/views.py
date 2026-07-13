from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CustomUserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = CustomUserSerializer(request.user)
    return Response(serializer.data)
