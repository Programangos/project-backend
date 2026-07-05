from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.services.buildings_service import BuildingsService
from core.serializers.building_serializer import BuildingCommentSerializer


class BuildingCommentListCreateController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BuildingsService()

    def get(self, request, building_id):
        comments = self.service.get_comments(building_id)
        serializer = BuildingCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, building_id):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            return Response({'error': 'Debes iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)

        content = request.data.get('content', '').strip()
        if not content:
            return Response({'error': 'El comentario es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = self.service.create_comment(building_id, user_id, content)
        serializer = BuildingCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BuildingCommentDeleteController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BuildingsService()

    def delete(self, request, building_id, comment_id):
        try:
            self.service.delete_comment(comment_id, request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionError:
            return Response({'error': 'No tienes permiso para eliminar este comentario.'}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
