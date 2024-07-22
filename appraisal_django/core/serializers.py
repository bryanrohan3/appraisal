from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from datetime import timezone, datetime


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Token.objects.create(user=user)
        return user

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class DealershipSerializer(serializers.ModelSerializer):
    dealers = serializers.SerializerMethodField()

    class Meta:
        model = Dealership
        fields = ['id', 'dealership_name', 'street_address', 'suburb', 'state', 'postcode', 'email', 'phone', 'wholesalers', 'is_active' ,'dealers']

    def get_dealers(self, obj):
        role = self.context['request'].query_params.get('role')
        
        if role and role in ['M', 'S']:
            dealers = DealerProfile.objects.filter(dealerships=obj, role=role)
        else:
            dealers = DealerProfile.objects.filter(dealerships=obj)
        
        return DealerProfileSerializer(dealers, many=True).data
    

class DealershipBasicSerializer(serializers.ModelSerializer):
    '''
    Basic serializer for Dealership. Used for Searching for Dealerships.
    '''
    class Meta:
        model = Dealership
        fields = ['id', 'dealership_name', 'phone', 'email']


class DealerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for DealerProfile model.
    """
    user = UserSerializer()
    dealerships = serializers.PrimaryKeyRelatedField(queryset=Dealership.objects.all(), many=True, required=False)
    received_requests = serializers.SerializerMethodField()
    sent_requests = serializers.SerializerMethodField()

    class Meta:
        model = DealerProfile
        fields = ['user', 'phone', 'role', 'dealerships', 'received_requests', 'sent_requests']

    def create(self, validated_data):
        """
        Custom create method to handle creation of dealer profiles.
        For 'M' (Management Dealer), authentication is bypassed.
        """
        user_data = validated_data.pop('user')
        dealership_data = validated_data.pop('dealerships', [])
        role = validated_data.get('role')

        if role == 'M':
            # Create the user without authentication check
            user = UserSerializer().create(user_data) # bypass authentication
            dealer_profile = DealerProfile.objects.create(user=user, **validated_data) 
            dealer_profile.dealerships.set(dealership_data)
            return dealer_profile

        else:
            request = self.context.get('request')
            if not request or not request.user.is_authenticated:
                raise serializers.ValidationError("Authentication credentials were not provided.")

            # Check if the authenticated user has permission to create the dealer profile
            creator_profile = DealerProfile.objects.get(user=request.user)
            if creator_profile.role != 'M':
                raise serializers.ValidationError("Only Management Dealers can create new users.")

            # Validate that the creator has access to the specified dealerships
            creator_dealership_ids = set(creator_profile.dealerships.values_list('id', flat=True))
            new_dealership_ids = set([dealership.id for dealership in dealership_data])

            if not new_dealership_ids.intersection(creator_dealership_ids):
                raise serializers.ValidationError("Cannot create dealer for dealership you don't work for")

            # Create the user and dealer profile
            user = UserSerializer().create(user_data)
            dealer_profile = DealerProfile.objects.create(user=user, **validated_data)
            dealer_profile.dealerships.set(dealership_data)
            return dealer_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        dealerships_data = validated_data.pop('dealerships', instance.dealerships.all())

        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        instance.phone = validated_data.get('phone', instance.phone)
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        instance.dealerships.set(dealerships_data)
        
        return instance
    
    def get_dealerships(self, instance):
        user = instance.user
        role = instance.role
        
        if role == 'S':  # Sales dealer
            dealerships = instance.dealerships.values_list('id', flat=True)
        elif role == 'M':  # Management dealer
            dealerships = DealerProfile.objects.filter(user=user, role='M').values_list('dealerships__id', flat=True)
        else:
            dealerships = []
        
        return list(dealerships)

    def get_received_requests(self, instance):
        # Adjusted logic to get received requests for the dealer's dealerships
        received_requests = FriendRequest.objects.filter(dealership__in=instance.dealerships.all())
        return FriendRequestSerializer(received_requests, many=True).data

    def get_sent_requests(self, instance):
        # Check if the user has a wholesaler profile before accessing it
        if hasattr(instance.user, 'wholesalerprofile'):
            sent_requests = FriendRequest.objects.filter(sender=instance.user.wholesalerprofile)
            return FriendRequestSerializer(sent_requests, many=True).data
        return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dealerships'] = self.get_dealerships(instance)
        return representation


class DealerProfileNestedSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = DealerProfile
        fields = ['id', 'first_name', 'last_name']

class DealershipNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
        fields = ['id', 'dealership_name']


class WholesalerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = WholesalerProfile
        fields = ['user', 'wholesaler_name', 'street_address', 'suburb', 'state', 'postcode', 'email', 'phone', 'is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        wholesaler_profile = WholesalerProfile.objects.create(user=user, **validated_data)
        return wholesaler_profile

    def update(self, instance, validated_data):
        # Remove 'user' from validated_data to avoid KeyError
        validated_data.pop('user', None)

        # Update fields directly
        instance.wholesaler_name = validated_data.get('wholesaler_name', instance.wholesaler_name)
        instance.street_address = validated_data.get('street_address', instance.street_address)
        instance.suburb = validated_data.get('suburb', instance.suburb)
        instance.state = validated_data.get('state', instance.state)
        instance.postcode = validated_data.get('postcode', instance.postcode)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        
        return instance
    

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'appraisal', 'photo', 'description']

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'comment', 'comment_date_time']


class OfferSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'amount', 'adjusted_amount', 'created_at']
        read_only_fields = ['user', 'adjusted_amount']

    def get_user(self, obj):
        user = obj.user
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

    def validate(self, attrs):
        user = self.context['request'].user
        if not hasattr(user, 'wholesalerprofile') or not user.wholesalerprofile.is_wholesaler:
            raise serializers.ValidationError("Only wholesalers can make an offer.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class AdjustedAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['adjusted_amount']


class DamageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Damage
        fields = ('id', 'damage_description', 'damage_location', 'damage_photos', 'repair_cost_estimate')

    def create(self, validated_data):
        damage_photos_data = validated_data.pop('damage_photos', [])
        damage = Damage.objects.create(**validated_data)

        for photo_data in damage_photos_data:
            Photo.objects.create(damage=damage, image=photo_data)

        return damage


class AppraisalSerializer(serializers.ModelSerializer):
    initiating_dealer = DealerProfileNestedSerializer(read_only=True)
    last_updating_dealer = DealerProfileNestedSerializer(read_only=True)
    dealership = DealershipNestedSerializer(read_only=True)
    # damage_photos = PhotoSerializer(many=True, read_only=True, source='damage_photos_set')
    damages = DamageSerializer(many=True)
    vehicle_photos = PhotoSerializer(many=True, read_only=True, source='vehicle_photos_set')
    sent_to_management = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    private_comments = CommentSerializer(many=True, read_only=True )
    general_comments = CommentSerializer(many=True, read_only=True )
    offers = OfferSerializer(many=True, required=False)

    class Meta:
        model = Appraisal
        fields = [
            'id', 'start_date', 'last_updated', 'is_active', 'dealership', 'initiating_dealer', 
            'last_updating_dealer', 'customer_first_name', 'customer_last_name', 'customer_email', 
            'customer_phone', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_vin', 
            'vehicle_registration', 'color', 'odometer_reading', 'engine_type', 'transmission', 
            'body_type', 'fuel_type', 'reserve_price', 'damages', 'vehicle_photos', 
            'sent_to_management', 'private_comments', 'general_comments', 'offers'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        dealer_profile = DealerProfile.objects.get(user=user)

        if not dealer_profile.dealerships.exists():
            raise serializers.ValidationError("You are not associated with any dealership.")

        dealership = dealer_profile.dealerships.first()
        validated_data['initiating_dealer'] = dealer_profile
        validated_data['dealership'] = dealership
        validated_data['last_updating_dealer'] = dealer_profile

        sent_to_management_ids = validated_data.pop('sent_to_management', [])
        damage_data = validated_data.pop('damages', [])  # Get the list of damages

        appraisal = Appraisal.objects.create(**validated_data)

        for damage_item in damage_data:
            damage_photos_data = damage_item.pop('damage_photos', [])  # Extract damage photos if needed
            damage = Damage.objects.create(appraisal=appraisal, **damage_item)

            for photo_data in damage_photos_data:
                Photo.objects.create(damage=damage, image=photo_data)

        appraisal.sent_to_management.set(sent_to_management_ids)

        return appraisal

    
class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appraisal
        fields = '__all__'  # Include all fields initially

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove 'offers' field if user is Sales Dealer
        if self.context['request'].user.groups.filter(name='SalesDealer').exists():
            del data['offers']
        return data


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.user.username')
    dealership = serializers.PrimaryKeyRelatedField(queryset=Dealership.objects.all())

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'dealership', 'status', 'created_at']
        read_only_fields = ['sender', 'status', 'created_at']

    def validate(self, data):
        '''
        Checks if user is a wholesaler or not
        '''
        user = self.context['request'].user
        if not hasattr(user, 'wholesalerprofile'):
            raise serializers.ValidationError("Only wholesalers can send requests.")
        return data

