from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .emails import *


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email, password=password)
                print(email)
                print(password)
                if user is None:
                    return Response({
                        'status': 400,
                        'message': 'Invalid mail or password',
                        'data': serializer.errors,
                    })
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'Success!',
                    'message': 'Get ready for new Udaan!!',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
                # is_verified = user.is_verified
                # print(is_verified)
                # if is_verified:
                #     refresh = RefreshToken.for_user(user)
                #     return Response({
                #         'status': 'Success!',
                #         'message': 'Get ready for new Udaan!!',
                #         'refresh': str(refresh),
                #         'access': str(refresh.access_token),
                #    })
                #
                # return Response({
                #     'status': '400',
                #     'message': 'Please verify your mail first'
                # })

            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = CustomUserSerializer(data=data)
            print('0............')
            if serializer.is_valid():
                print('1............')
                user = CustomUser.objects.create_user(email=serializer.data['email'], password=serializer.data['password'],
                                                      first_name=serializer.data['first_name'], last_name=serializer.data['last_name'],
                                                      contact_no=serializer.data['contact_no'], location=serializer.data['location'],
                                                      is_business=serializer.data['is_business'], is_customer=serializer.data['is_customer'])
                user.save()
                print('2............')
                # send_verification_mail(serializer.data['email'], serializer.data['first_name'])
                return Response({
                    'status': 200,
                    'message': 'registration successfull!! check mail',
                    'data': serializer.data.get('email'),
                })

            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors,
            })
        except Exception as e:
            print(e, '______________________________')
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })



class VerfiyOTPView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyEmailSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = CustomUser.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 200,
                        'message': 'Something went wrong',
                        'data': 'invalid email',
                    })

                if not user[0].otp == otp:
                    return Response({
                        'status': 200,
                        'message': 'Something went wrong',
                        'data': 'Incorrect otp',
                    })
                print(user.first())
                user = user.first()
                user.is_verified = True
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Verification successful',
                    'data': {},
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors,
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': {},
            })



