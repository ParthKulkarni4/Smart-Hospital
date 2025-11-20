from datetime import timezone
from rest_framework import serializers
from .models import Ambulance, AmbulanceTrip
from ambulance.models import Ambulance
class AmbulanceSerializer(serializers.ModelSerializer):
    class Meta: model=Ambulance; fields='__all__'



class AmbulanceTripSerializer(serializers.ModelSerializer):
    class Meta: model=AmbulanceTrip; fields='__all__'
    def create(self,validated_data):

        if 'booked_by' not in validated_data:
            validated_data['booked_by']=self.context['request'].user
        return super().create(validated_data)
    
    # Handle status updates
    def update(self,instance,validated_data):
        new_status=validated_data.get('status',instance.status)

# Dispatching ambulance

        if new_status  == 'dispatched' and instance.status == 'requested':
            #  Auto assign available ambulance
            available_ambulance=Ambulance.objects.filter(status='available').first()
            if not available_ambulance:
                raise serializers.ValidationError("No available ambulances to dispatch.")
            validated_data['ambulance'] = available_ambulance
            
            validated_data['start_time']= validated_data.get('start_time',instance.start_time or timezone.now())
            available_ambulance.status='busy'
            available_ambulance.save()

            # compelting trip
            #set end time and free ambulannce
        elif new_status == 'completed' and instance.status in ['dispatched','arrived']:
            
            if not validated_data.get('end_time'):
                validated_data['end_time']=timezone.now()
            if instance.ambulance:
                instance.ambulance.status='available'
                instance.ambulance.save()
        return super().update(instance,validated_data)
 