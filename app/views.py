from rest_framework import response, status, viewsets
from rest_framework.permissions import IsAuthenticated

from app.models import Todo
from app.permissions import UserIsOwner
from app.serializers import TodoSerializer


class TodoAPIView(viewsets.GenericViewSet):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, UserIsOwner)

    def get_object(self):
        todo = Todo.objects.filter(id=self.kwargs.get('pk'), user=self.request.user)
        if todo.exists():
            todo = todo.first()
            self.check_object_permissions(self.request, todo)
            return todo
        return None

    def create(self, request, *args, **kwargs):
        """
        Add a todos task
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return response.Response(status=status.HTTP_201_CREATED)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        List all the todos associated to this user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        filters = dict(user=request.user)
        boolean_dict = dict(false=False, true=True)
        todos_completed = request.GET.get('todos_completed')
        if todos_completed in boolean_dict.keys():
            filters.update(is_complete=boolean_dict[todos_completed])
        todos = Todo.objects.filter(**filters)
        return response.Response(data=self.serializer_class(todos, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        """
        Get todos task by id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        todo = self.get_object()
        if todo:
            serialized = self.serializer_class(todo)
            return response.Response(data=serialized.data, status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """
        Update the title, is_complete status, completion_time by id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        todo = self.get_object()
        if todo:
            serializer = self.serializer_class(instance=todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a todos task by id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        todo = self.get_object()
        if todo:
            todo.delete()
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_404_NOT_FOUND)
