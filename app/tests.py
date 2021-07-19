from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory

from app.models import Todo
from app.serializers import TodoSerializer
from app.views import TodoAPIView


class GetAllTodos(TestCase):
    """ Test module for GET all Todos API """

    def setUp(self):
        """
        Set up the data
        :return:
        """
        self.factory = APIRequestFactory()
        self.user = User(username='mirza1')
        self.user.set_password('Password1@#')
        self.user.save()

        self.view = TodoAPIView.as_view({'get': 'list'})
        Todo.objects.create(title='Todo task 1', user=self.user)

    def test_get_all_todos_with_status(self):
        """
        Get all the completed/incompleted tasks based on parameter
        """
        # get API response
        # Make an authenticated request to the view...
        request = self.factory.get('/api/todo/?todos_completed=true')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        # # get data from db
        todos = Todo.objects.filter(is_complete=True)
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
