from .serializer import *
from accounts.models import CustomUser
from accounts.serializer import CustomUserSerializer
from service.models import Service
from service.serializer import ServiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# for specific business only
class ProfileViewForBusiness(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            queryset = Profile.objects.filter(user=user)
            serialize_profile = ProfileSerializer(queryset, many=True)
            query = CustomUser.objects.filter(id=user.id)
            print('yeah')
            serialize_user = CustomUserSerializer(query, many=True)
            email = serialize_user.data[0].get('email')
            serialize_profile.data[0].update({'email': email})
            return Response({
                'data': serialize_profile.data,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })

    def post(self, request):
        print('...............................')
        try:
            user = {'user': request.user.id}
            print('12----------------')
            data = request.data
            print('y')
            data = {**data, **user}
            print('me')
            serializer = ProfileSerializer(data=data)
            print('here')
            if serializer.is_valid():
                print('there')
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Your Profile has been updated successfully!',
                    'data': serializer.data,
                })
            return Response({
                'status': '400',
                'message': 'Something went wrong:(',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': '400',
                'message': 'Something went wrong:(',
                'data': {}
            })


# business can make skill and get whole profile+skill
class SkillViewForBusiness(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            queryset = Skills.objects.filter(user=user)
            serialize = SkillSerializer(queryset, many=True)
            print(serialize.data)

            query_user = CustomUser.objects.filter(id=user.id)
            serialize_user = CustomUserSerializer(query_user, many=True)
            email = serialize_user.data[0].get('email')

            query_profile = Profile.objects.filter(user=user.id)
            serialize_profile = ProfileSerializer(query_profile, many=True)
            print(serialize_profile.data)
            serialize_profile.data[0].update({'email': email})

            return Response({
                'data': serialize_profile.data + serialize.data
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })

    def post(self, request):
        try:
            user = {'user': request.user.id}
            data = request.data
            data = {**data, **user}
            serializer = SkillSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Your Skill has been added successfully!',
                    'data': serializer.data,
                })
            return Response({
                'status': '400',
                'message': 'Something went wrong:(',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


# customer can view profile along with names of skills for that user
class ProfileViewForCustomer(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_profiles = Profile.objects.all()
            serializer = ProfileSerializer(user_profiles, many=True)

            for i in serializer.data:
                user = i.get('user')
                query = CustomUser.objects.filter(id=user)
                serializer_user = CustomUserSerializer(query, many=True)
                email = serializer_user.data[0].get('email')
                print(email)
                i.update({'email': email})

                queryset_skill = Skills.objects.filter(user=user)
                serializer_skill = SkillSerializer(queryset_skill, many=True)
                skill = []
                for j in serializer_skill.data:
                    skill.append(j.get('skill_name'))
                print(i)
                print(skill)
                i.update({'skill': skill})
                print(i)

            return Response({
                'data':  serializer.data
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


# all skills for customer
class SkillViewForCustomer(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            all_skills = Skills.objects.all()
            serializer = SkillSerializer(all_skills, many=True)
            print('good to go')
            return Response({
                'data': serializer.data,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


# skill for particular user
class ParticularBusinessSkillViewForCustomer(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.data.get('user')
            queryset = Skills.objects.filter(user=user)
            serializer = SkillSerializer(queryset, many=True)

            return Response({
                'data':   serializer.data,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


class ServicesStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            print(user)
            query_skill = Skills.objects.filter(user=user)
            serializer_skill = SkillSerializer(query_skill, many=True)
            print(serializer_skill.data)

            skills = []
            for i in serializer_skill.data:
                skills.append(i.get('id'))
            print(skills)

            services = []
            pending_services = []
            accepted_not_completed_services = []
            completed_services = []
            for i in skills:
                query_service = Service.objects.filter(skill=i)
                serializer_service = ServiceSerializer(query_service, many=True)
                for j in serializer_service.data:
                    print(j)
                    status = j.get('status')
                    if status == '1':
                        pending_services.append(j)
                    elif status == '2':
                        if j.get('is_completed'):
                            completed_services.append(j)
                        else:
                            accepted_not_completed_services(j)

                    services.append(j.get('id'))
            # print(completed_services)
            # print(accepted_not_completed_services)
            # print(pending_services)
            serializer = []
            serializer.append({'completed' : completed_services})
            serializer.append({'pending' : pending_services})
            serializer.append({'accepted_not_completed' : accepted_not_completed_services})
            return Response({
                'data': serializer
            })


        except Exception as e:
                print(e)
                return Response({
                    'status': 400,
                    'message': 'Something went wrong',
                    'data': {},
            })
