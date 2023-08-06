from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import authentication,generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([authentication.SessionAuthentication])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)

        obj = Product.objects.all()
        data = ProductSerializer(obj, many=True).data
        return Response(data)
    elif method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            
product_list_create_view = ProductListCreateAPIView.as_view()