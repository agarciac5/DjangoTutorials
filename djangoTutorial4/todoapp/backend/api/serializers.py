from rest_framework import serializers
from todo.models import ToDo


class ToDoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        fields = ['title', 'memo', 'created', 'completed']


class ToDoToggleCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        fields = ['completed']