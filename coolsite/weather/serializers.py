import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"

#class WeatherSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Weather
#        fields = ('title', 'cat_id')

#class WeatherSerializer(serializers.Serializer):
  #  title = serializers.CharField(max_length=255)
 #   content = serializers.CharField()
 #   time_create = serializers.DateTimeField(read_only=True)
 #   time_update = serializers.DateTimeField(read_only=True)
 #   is_published = serializers.BooleanField(default=True)
 #   cat_id = serializers.IntegerField()
#
#    def create(self, validated_data):
 #       return Weather.objects.create(**validated_data)

  #  def update(self, instance, validated_data):
   #     instance.title = validated_data.get("title", instance.title)
    #    instance.content = validated_data.get("content", instance.content)
    #    instance.time_update = validated_data.get("time_update", instance.time_update)
    ##    instance.is_published = validated_data.get("is_published", instance.is_published)
     #   instance.cat_id = validated_data.get("cat_id", instance.cat_id)
     #   instance.save()
     #   return instance

# def encode():
#     model = WeatherModel('27-градусная жара и ночные заморозки",', 'Content: 27-градусная жара и ночные заморозки",')
#     model_sr = WeatherSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"title":"27-градусная жара и ночные заморозки",","content":"Content: 27-градусная жара и ночные заморозки","}')
#     data = JSONParser().parse(stream)
#     serializer = WeatherSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)

