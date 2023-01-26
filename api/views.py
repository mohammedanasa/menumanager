from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.request import Request
from rest_framework.response import Response
from restaurant.models import Category
from api.serializer import CategorySerializer,CurrentUserCategorySerializer
from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def homepage(request: Request):

    if request.method == "POST":
        data = request.data

        response = {"message": "Hello World", "data": data}

        return Response(data=response, status=status.HTTP_201_CREATED)

    response = {"message": "Hello World"}
    return Response(data=response, status=status.HTTP_200_OK)


class CategoryListCreateView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):

    """
    a view for creating and listing posts
    """

    serializer_class = CategorySerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserCategorySerializer(instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)