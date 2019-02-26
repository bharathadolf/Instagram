from rest_framework import generics
from .serialisers import *


class SearchApi(generics.ListCreateAPIView):
    serializer_class = ProfileSerialisers

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user__username__icontains=self.kwargs['slug'])
        queryset =self.get_serializer_class().setup_eager_loading(queryset=queryset)
        return queryset
