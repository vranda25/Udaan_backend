from .serializer import *
from accounts.models import CustomUser
from accounts.serializer import CustomUserSerializer
from business.models import Profile
from business.models import Skills
from business.serializer import ProfileSerializer
from business.serializer import SkillSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from collections import OrderedDict

# Create your views here.
class ServiceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            customer = request.user
            queryset = Service.objects.filter(customer=customer)
            serializer = ServiceSerializer(queryset, many=True)

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

    def post(self, request):
        try:
            customer = {'customer': request.user.id}
            print('12----------------')
            data = request.data
            print('y')
            data = {**data, **customer}
            serializer = ServiceSerializer(data=data)
            print('here')
            if serializer.is_valid():
                print('there')
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Your service request has been sent successfully!',
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


class StatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            service = request.data.get('service')
            service = Service.objects.filter(id=service)
            service = service.first()
            status = request.data.get('status')
            service.status = status
            service.save()
            return Response({
                'status': 200,
                'message': 'Status updated',
                'data': {},
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


class CompletedView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            service = request.data.get('service')
            service = Service.objects.filter(id=service)
            service = service.first()
            if service.status == "2":
                service.is_completed = True
                service.save()

                skill = service.skill
                print(skill)
                skill = Skills.objects.filter(id=skill.id)
                skill = skill.first()
                user = skill.user
                print(user)
                profile = Profile.objects.filter(user=user)
                profile = profile.first()
                profile.jobs_completed += 1
                profile.save()

                return Response({
                    'status': 200,
                    'message': 'Job completed^_~',
                    'data': {},
                })
            return Response({
                    'status': 200,
                    'message': 'Job was not accepted',
                    'data': {},
                })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })

class RatingView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            service = request.data.get('service')
            print(service)
            queryset = Rating.objects.filter(service=service)
            serializer = RatingSerializer(queryset, many=True)
            return Response({
                'status': 200,
                'message': 'Rating',
                'data': serializer.data,
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
            service = request.data.get('service')
            print(service)
            service = Service.objects.get(id=service)
            print(service)
            is_completed = service.is_completed
            if is_completed:
                services = {'customer': service}
                data = request.data
                print('y')
                data = {**data, **services}
                serializer = RatingSerializer(data=data)
                print('here')
                if serializer.is_valid():
                    print('there')
                    serializer.save()
                    service.is_rated = True
                    service.save()
                    return Response({
                        'status': 200,
                        'message': 'Your service feedback has been recorded successfully!',
                        'data': serializer.data,
                    })
                return Response({
                    'status': '400',
                    'message': 'Something went wrong:(',
                    'data': serializer.errors
                })
            return Response({
                'status': '400',
                'message': 'Service is not completed:|',
                'data': {}
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


class AllRatingOfParticularBusiness(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.data.get('user')
            print(user)
            query_skill = Skills.objects.filter(user=user)
            serializer_skill = SkillSerializer(query_skill, many=True)
            print(serializer_skill.data)

            skills = []
            for i in serializer_skill.data:
                skills.append(i.get('id'))
            print(skills)

            services = []
            for i in skills:
                query_service = Service.objects.filter(skill=i)
                serializer_service = ServiceSerializer(query_service, many=True)
                for j in serializer_service.data:
                    services.append(j.get('id'))
            print(services)

            serializer = []
            for j in services:
                queryset = Rating.objects.filter(service=j)
                serializer_rating = RatingSerializer(queryset, many=True)
                print(serializer_rating.data)
                if len(serializer_rating.data) > 0:
                    serializer.append(serializer_rating.data[0])

            return Response({
                'status': 200,
                'message': 'Rating',
                'data': serializer,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })


class ServicesCompletedByParticularBusiness(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.data.get('user')
            print(user)
            query_skill = Skills.objects.filter(user=user)
            serializer_skill = SkillSerializer(query_skill, many=True)
            print(serializer_skill.data)

            skills = []
            for i in serializer_skill.data:
                skills.append(i.get('id'))
            print(skills)

            services = []
            for i in skills:
                customer_name = []
                skill_name = []
                query_service = Service.objects.filter(skill=i)
                serializer_service = ServiceSerializer(query_service, many=True)
                for j in serializer_service.data:
                    customer = j.get('customer')
                    customer = CustomUser.objects.filter(id=customer)
                    customer = customer.first()
                    customer_name.append(customer.first_name)

                    skill = j.get('skill')
                    skill = Skills.objects.filter(id=skill)
                    skill = skill.first()
                    skill_name.append(skill.skill_name)

                    services.append(j.get('id'))

            print(services)
            print(skill_name)
            print(customer_name)

            rating = []
            for j in services:
                queryset = Rating.objects.filter(service=j)
                serializer_rating = RatingSerializer(queryset, many=True)
                print(serializer_rating.data)
                if len(serializer_rating.data) > 0:
                    rating.append(serializer_rating.data[0])

            serializer = []
            serializer.append({'customer_name' : customer_name})
            serializer.append({'skill_name' : skill_name})
            serializer.append({'rating' : rating})

            return Response({
                'status': 200,
                'message': 'Rating',
                'data': serializer,
            })

        except Exception as e:
                print(e)
                return Response({
                    'status': 400,
                    'message': 'Something went wrong',
                    'data': {},
                })

