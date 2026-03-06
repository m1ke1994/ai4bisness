from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "message": "Django backend is running",
            }
        )
