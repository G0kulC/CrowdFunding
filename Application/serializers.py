from rest_framework import serializers
from .models import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            "project_name",
            "Project_location",
            "Latitude",
            "Longitude",
            "Project_value",
            "Kickoff_date",
            "Returns_projection_type",
            "Returns_projection_value",
            "Other_expense",
            "Total_share",
            "Per_share_value",
            "Expected_return_date",
            "status",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        print(fields)
        extra_kwargs = {"password": {"write_only": True}}
