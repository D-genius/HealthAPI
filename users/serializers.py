from rest_framework import serializers
from users.models import CustomUser
from patients.models import Patient
from doctors.models import Doctor, Availability
from appointments.models import Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'user_type','is_patient', 'is_doctor')
        read_only_fields = ('is_patient', 'is_doctor','user_type')
        # extra_kwargs = {'password': {'write_only': True}}

class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(**validated_data)
    #     return user

class PatientUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')

class PatientSerializer(serializers.ModelSerializer):
    user = PatientUserSerializer()

    class Meta:
        model = Patient
        fields = ('user', 'id_number', 'insurance_number','phone','address')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            user_type='patient'
        )

        return Patient.objects.create(user=user, **validated_data)

class DoctorUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name')

class DoctorSerializer(serializers.ModelSerializer):
    user = DoctorUserSerializer()

    class Meta:
        model = Doctor
        fields = ('user', 'specialization', 'phone', 'hospital')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            user_type='doctor'
        )
        return Doctor.objects.create(user=user, **validated_data)

#TODO: Re construct the availability classes

# class DoctorAvailabilitySerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password', 'first_name', 'last_name')

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('doctor','start_datetime','end_datetime','is_available')

    # def create(self, validated_data):
    #     user_data = validated_data.pop('doctor')
    #     user = CustomUser.objects.view_availability(
    #         email=user_data['email'],
    #         password=user_data['password'],
    #         first_name=user_data.get('first_name', ''),
    #         last_name=user_data.get('last_name', ''),
    #         user_type='doctor'
    #     )
    #     return Availability.objects.create(doctor=user, **validated_data)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'doctor', 'scheduled_datetime', 'follow_up_datetime', 'status')
