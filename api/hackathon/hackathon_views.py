from rest_framework.views import APIView

from db.hackathon import Hackathon
from utils.permission import CustomizePermission
from utils.response import CustomResponse
from utils.types import DEFAULT_HACKATHON_FORM_FIELDS
from utils.utils import DateTimeUtils
from .serializer import HackathonCreateUpdateDeleteSerializer, HackathonRetrivalSerailzier


class HackathonManagementAPI(APIView):
    authentication_classes = [CustomizePermission]

    def get(self, request):
        hackathons_queryset = Hackathon.objects.all()
        for i in hackathons_queryset:
            print(i.created_at, DateTimeUtils.get_current_utc_time(),
                  i.created_at > DateTimeUtils.get_current_utc_time())

        serializer = HackathonRetrivalSerailzier(hackathons_queryset, many=True)
        return CustomResponse(response=serializer.data).get_success_response()

    def post(self, request):
        serializer = HackathonCreateUpdateDeleteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(general_message="Hackathon Created").get_success_response()
        return CustomResponse(message=serializer.errors).get_failure_response()

    def put(self, request, hackathon_id):
        hackathon = Hackathon.objects.filter(id=hackathon_id).first()
        if hackathon is None:
            return CustomResponse(general_message='Hackathon Does Not Exist').get_failure_response()
        serializer = HackathonCreateUpdateDeleteSerializer(hackathon, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomResponse(general_message='Hackathon Updated').get_success_response()
        return CustomResponse(message=serializer.errors).get_failure_response()

    def delete(self, request, hackathon_id):
        hackathon = Hackathon.objects.filter(id=hackathon_id).first()
        if hackathon is None:
            return CustomResponse(general_message='Hackathon Does Not Exist').get_failure_response()
        serializer = HackathonCreateUpdateDeleteSerializer()
        serializer.destroy(hackathon)
        return CustomResponse(general_message='Hackathon Deleted').get_success_response()


class GetDefaultFieldsAPI(APIView):
    authentication_classes = [CustomizePermission]

    def get(self, request):
        return CustomResponse(response=DEFAULT_HACKATHON_FORM_FIELDS).get_success_response()
