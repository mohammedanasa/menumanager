from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import APIView, api_view, permission_classes,action

from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.request import Request
from rest_framework.response import Response
from restaurant.models import Category,Menu,Restaurant,Product
from api.serializer import *
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

#New Tests
class ListCreateMenuView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(category__=category_id)
        return queryset.prefetch_related('product')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class MenuViewWithProducts(generics.GenericAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        category_id = self.request.query_params.get('category_cid', None)
        if category_id is not None:
            try:
                category = Category.objects.get(id=category_cid)
                menus = self.queryset.filter(owner=self.request.user, category=category)
                products = []
                for menu in menus:
                    products += menu.product.all()
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
            except Category.DoesNotExist:
                raise Http404("Category does not exist")
        raise Http404("category_id is not provided")


class MenuProductListView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Menu.objects.filter(owner=self.request.user)
        return queryset


    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Restaurant.objects.filter(owner=self.request.user)
        for restaurant in queryset:
            menus = Menu.objects.filter(restaurant=restaurant, owner=self.request.user)
            for menu in menus:
                category = Category.objects.filter(menu__in=[menu], owner=self.request.user)
                products = Product.objects.filter(categories__in=category, owner=self.request.user)
                for product in products:
                    modifier_groups = ModifierGroup.objects.filter(product=product, owner=self.request.user)
                    for modifier_group in modifier_groups:
                        modifiers = Modifier.objects.filter(modifier_group=modifier_group, owner=self.request.user)
                        modifier_group.modifiers.set(modifiers)
                    product.modifier_groups.set(modifier_groups)
                menu.category.set(category)
                menu.product = products
            restaurant.menu.set(menus)
            address = Address.objects.filter(restaurant=restaurant, owner=self.request.user)
            restaurant.address.set(address)
        return queryset



class LocationMenuListView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        location_id = self.kwargs['lid']
        queryset = Menu.objects.filter(restaurant__lid=location_id, owner=self.request.user)
        products = Product.objects.filter(owner=self.request.user)
        
        return queryset


class LocationMenuCreateListView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin
):

    """
    a view for creating and listing posts
    """

    serializer_class = RestaurantSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)
        return super().perform_create(serializer)

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

#Working
@api_view(['GET'])
def list_menus(request):
    store_id = request.headers.get('store-id')
    location = get_object_or_404(Restaurant, pk=store_id)
    menus = Menu.objects.filter(restaurant=location)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer

    def get_queryset(self):
        store_id = self.request.headers.get('store-id')
        store = get_object_or_404(Restaurant, pk=store_id)
        return Menu.objects.filter(restaurant=store)

    def create(self, request, *args, **kwargs):
        store_id = request.headers.get('store-id')
        store = get_object_or_404(Restaurant, pk=store_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=store)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
