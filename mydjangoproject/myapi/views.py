from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from .serializers import PersonSerializer
from .models import Person
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .face_recongnition_api import check_face_exist


class PersonViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.AllowAny]

    queryset = Person.objects.all().order_by('id')
    serializer_class = PersonSerializer
    parser_classes = (MultiPartParser, FormParser)

    @ api_view(['GET', 'POST', 'DELETE'])
    def person_list(request):
        if request.method == 'GET':
            persons = Person.objects.all()

            title = request.query_params.get('title', None)
            if title is not None:
                persons = persons.filter(title__icontains=title)

            persons_serializer = PersonSerializer(persons, many=True)
            return JsonResponse(persons_serializer.data, safe=False)
            # 'safe=False' for objects serialization

        elif request.method == 'POST':
            person_data = JSONParser().parse(request)
            person_serializer = PersonSerializer(data=person_data)
            if person_serializer.is_valid():
                person_serializer.save()
                print(person_serializer.data['image_url'])

                if not check_face_exist(person_serializer.data['image_url']):
                    person_data.delete()
                    return JsonResponse(person_serializer.errors, {'message': '{} Provide image with 1 face!'})
                return JsonResponse(person_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            count = Person.objects.all().delete()
            return JsonResponse({'message': '{} Persons were deleted successfully!'.format(count[0])},
                                status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET', 'PUT', 'DELETE'])
    def person_by_id(request, pk):
        try:
            person = Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            return JsonResponse({'message': 'The person does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            person_serializer = PersonSerializer(person)
            return JsonResponse(person_serializer.data)

        elif request.method == 'PUT':
            person_data = JSONParser().parse(request)
            person_serializer = PersonSerializer(person, data=person_data)
            if person_serializer.is_valid():
                person_serializer.save()
                return JsonResponse(person_serializer.data)
            return JsonResponse(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            person.delete()
            return JsonResponse({'message': 'Person was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
