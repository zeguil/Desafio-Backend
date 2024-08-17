import datetime

from rest_framework import serializers

from .models import Task

TITLE_LENGTH = 100


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['is_deleted']

    @staticmethod
    def validate_title(value):
        if not value.strip():
            raise serializers.ValidationError('O título não pode estar vazio.')
        if len(value) > TITLE_LENGTH:
            raise serializers.ValidationError('O título deve ter no máximo 100 caracteres.')
        return value

    @staticmethod
    def validate_description(value):
        if not value.strip():
            raise serializers.ValidationError('A descrição não pode estar vazia.')
        return value

    @staticmethod
    def validate_due_date(value):
        if value < datetime.date.today():
            raise serializers.ValidationError('A data de vencimento não pode estar no passado.')
        return value

    @staticmethod
    def validate(data):
        if not data.get('title'):
            raise serializers.ValidationError({'title': 'O campo título é obrigatório.'})
        if not data.get('description'):
            raise serializers.ValidationError({'description': 'O campo descrição é obrigatório.'})
        if not data.get('due_date'):
            raise serializers.ValidationError({'due_date': 'O campo data de vencimento é obrigatório.'})
        return data
