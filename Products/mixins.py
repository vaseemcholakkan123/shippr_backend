from rest_framework.generics import CreateAPIView , UpdateAPIView , DestroyAPIView
from rest_framework.response import  Response
from rest_framework import status
from .models import Images , Category


class UserAsVendorAPIView(CreateAPIView , UpdateAPIView , DestroyAPIView):

    def perform_update(self, serializer):

        images = self.request.data.getlist("images[]")
        if not images or len(images) < 1:
            raise serializer.ValidationError({"message": "No images Provided"})

        product = serializer.save()

        product_images = Images.objects.filter(product=product)

        for current_image in product_images:
            if current_image.image.url not in images:
                current_image.delete()

        for img in images:
            if not isinstance(img,str):
                Images.objects.create(product=product , image = img)



    def create(self , request , *args , **kwargs):
        updated_data = self.request.POST.copy()
        updated_data['vendor'] = self.request.user.id
        images = self.request.data.getlist("images[]")
        updated_data['images'] = images

        serializer = self.get_serializer(data=updated_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserInSerializerContext:
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['context'] = {'user': self.request.user}
        return serializer_class(*args, **kwargs)
