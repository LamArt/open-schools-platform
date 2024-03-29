from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from open_schools_platform.api.mixins import ApiAuthMixin
from open_schools_platform.api.pagination import get_paginated_response
from open_schools_platform.api.swagger_tags import SwaggerTags
from open_schools_platform.common.utils import get_dict_excluding_fields
from open_schools_platform.common.views import convert_dict_to_serializer
from open_schools_platform.errors.exceptions import AlreadyExists
from open_schools_platform.organization_management.circles.filters import CircleFilter
from open_schools_platform.organization_management.circles.models import Circle
from open_schools_platform.organization_management.circles.paginators import ApiCircleListPagination
from open_schools_platform.organization_management.circles.selectors import get_circle, get_circles_by_students
from open_schools_platform.organization_management.circles.serializers import GetListCircleSerializer
from open_schools_platform.parent_management.families.selectors import get_family
from open_schools_platform.parent_management.families.services import add_student_profile_to_family
from open_schools_platform.query_management.queries.selectors import get_queries, get_query_with_checks
from open_schools_platform.query_management.queries.serializers import GetStudentJoinCircleSerializer
from open_schools_platform.student_management.students.selectors import get_student_profile, get_students, get_student
from open_schools_platform.student_management.students.serializers import GetStudentProfileSerializer, \
    CreateAutoStudentJoinCircleSerializer, UpdateStudentJoinCircleSerializer, \
    CreateStudentJoinCircleSerializer, UpdateStudentProfileSerializer, CreateStudentProfileSerializer, \
    GetStudentSerializer, UpdateStudentSerializer
from open_schools_platform.student_management.students.services import \
    create_student_profile, update_student_profile, update_student_join_circle_body, \
    autogenerate_family_logic, query_creation_logic, update_student


class StudentProfileApi(ApiAuthMixin, APIView):
    create_student_profile_serializer = CreateStudentProfileSerializer

    @swagger_auto_schema(
        operation_description="Creates Student profile via provided age, name and family id \n"
                              "Returns Student profile data",
        request_body=create_student_profile_serializer,
        responses={201: convert_dict_to_serializer({"student_profile": GetStudentProfileSerializer()}),
                   404: "No such family",
                   403: "Current user do not have permission to perform this action"},
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS]
    )
    def post(self, request):
        student_profile_serializer = self.create_student_profile_serializer(data=request.data)
        student_profile_serializer.is_valid(raise_exception=True)
        family = get_family(
            filters={"id": str(student_profile_serializer.validated_data['family'])},
            user=request.user,
            empty_exception=True,
        )
        student_profile = create_student_profile(
            **get_dict_excluding_fields(student_profile_serializer.validated_data, ["family"]))
        add_student_profile_to_family(student_profile=student_profile, family=family)
        return Response(
            {"student_profile": GetStudentProfileSerializer(student_profile, context={'request': request}).data},
            status=201)


class StudentProfileUpdateApi(ApiAuthMixin, APIView):
    @swagger_auto_schema(
        operation_description="Update student profile",
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        request_body=UpdateStudentProfileSerializer,
        responses={200: convert_dict_to_serializer({"student_profile": GetStudentProfileSerializer()}),
                   404: "No such student profile or family",
                   403: "Current user do not have permission to perform this action"}
    )
    def patch(self, request, student_profile_id):
        student_profile_update_serializer = UpdateStudentProfileSerializer(data=request.data)
        student_profile_update_serializer.is_valid(raise_exception=True)
        student_profile = get_student_profile(
            filters={'id': str(student_profile_id)},
            user=request.user,
            empty_exception=True,
        )

        if student_profile_update_serializer.validated_data['family']:
            get_family(
                filters={"id": student_profile_update_serializer.validated_data['family']},
                user=request.user,
                empty_exception=True,
            )
        update_student_profile(student_profile=student_profile,
                               data=get_dict_excluding_fields(student_profile_update_serializer.validated_data, []))
        return Response(
            {"student_profile": GetStudentProfileSerializer(student_profile, context={'request': request}).data},
            status=200)


class StudentProfileDeleteApi(ApiAuthMixin, APIView):
    @swagger_auto_schema(
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        operation_description="Delete student-profile.",
        responses={204: "Successfully deleted", 404: "No such student-profile"}
    )
    def delete(self, request, student_profile_id):
        student_profile = get_student_profile(filters={'id': student_profile_id}, empty_exception=True,
                                              user=request.user)
        student_profile.delete()
        return Response(status=204)


class AutoStudentJoinCircleQueryApi(ApiAuthMixin, APIView):
    @swagger_auto_schema(
        operation_description="Creates student profile, student and family.\n"
                              "Forms query for adding created student to circle",
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        request_body=CreateAutoStudentJoinCircleSerializer(),
        responses={201: convert_dict_to_serializer({"query": GetStudentJoinCircleSerializer()}),
                   400: "Current user already has family"}
    )
    def post(self, request):
        student_join_circle_req_serializer = CreateAutoStudentJoinCircleSerializer(data=request.data)
        student_join_circle_req_serializer.is_valid(raise_exception=True)
        if get_family(filters={"parent_profiles": str(request.user.parent_profile.id)}):
            raise AlreadyExists("Family for that user already exists")

        student_profile = autogenerate_family_logic(student_join_circle_req_serializer.validated_data, request.user)

        circle = get_circle(
            filters={'id': student_join_circle_req_serializer.validated_data["circle"]},
            empty_exception=True,
        )

        query = query_creation_logic(student_join_circle_req_serializer.validated_data, circle,
                                     student_profile, request.user)

        return Response({"query": GetStudentJoinCircleSerializer(query, context={'request': request}).data}, status=201)


class StudentJoinCircleQueryApi(ApiAuthMixin, APIView):
    @swagger_auto_schema(
        operation_description="Forms query for adding created student to circle",
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        request_body=CreateStudentJoinCircleSerializer(),
        responses={201: convert_dict_to_serializer({"query": GetStudentJoinCircleSerializer()}),
                   404: "No such student profile"}
    )
    def post(self, request, student_profile_id):
        student_join_circle_req_serializer = CreateStudentJoinCircleSerializer(data=request.data)
        student_join_circle_req_serializer.is_valid(raise_exception=True)
        student_profile = get_student_profile(
            filters={"id": str(student_profile_id)},
            user=request.user,
            empty_exception=True,
        )

        circle = get_circle(
            filters={'id': student_join_circle_req_serializer.validated_data["circle"]},
            empty_exception=True,
        )

        query = query_creation_logic(student_join_circle_req_serializer.validated_data, circle,
                                     student_profile, request.user)
        return Response({"query": GetStudentJoinCircleSerializer(query, context={'request': request}).data}, status=201)


class StudentJoinCircleQueryUpdateApi(ApiAuthMixin, APIView):
    @swagger_auto_schema(
        operation_description="Update body of student join circle query",
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        request_body=UpdateStudentJoinCircleSerializer(),
        responses={201: convert_dict_to_serializer({"query": GetStudentJoinCircleSerializer()}),
                   400: "Cant update query because it's status is not SENT",
                   404: "No such query"}
    )
    def patch(self, request):
        query_update_serializer = UpdateStudentJoinCircleSerializer(data=request.data)
        query_update_serializer.is_valid(raise_exception=True)

        query = get_query_with_checks(
            update_query_check=True,
            pk=str(query_update_serializer.validated_data["query"]),
            user=request.user,
        )
        update_student_join_circle_body(
            query=query,
            data=query_update_serializer.validated_data["body"],
        )
        return Response({"query": GetStudentJoinCircleSerializer(query, context={'request': request}).data}, status=200)


class StudentQueriesListApi(ApiAuthMixin, APIView):
    @swagger_auto_schema(
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        responses={200: convert_dict_to_serializer({"results": GetStudentJoinCircleSerializer(many=True)})},
        operation_description="Get all queries for provided student profile",
    )
    def get(self, request, student_profile_id):
        get_student_profile(
            filters={'id': str(student_profile_id)},
            empty_exception=True,
            empty_message='There is no such student profile'
        )

        student_profile = get_student_profile(filters={"id": str(student_profile_id)}, user=request.user)
        queries = get_queries(
            filters={'sender_id': str(student_profile.id)},
            empty_exception=True,
            empty_message='There are no queries with such sender'
        )
        return Response(
            {"results": GetStudentJoinCircleSerializer(queries, many=True, context={'request': request}).data},
            status=200)


class StudentCirclesListApi(ApiAuthMixin, ListAPIView):
    queryset = Circle.objects.all()
    filterset_class = CircleFilter
    pagination_class = ApiCircleListPagination
    serializer_class = GetListCircleSerializer

    @swagger_auto_schema(
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        operation_description="Get all circles for provided student profile",
    )
    def get(self, request, student_profile_id):
        student_profile = get_student_profile(
            filters={"id": str(student_profile_id)},
            user=request.user,
            empty_exception=True,
        )
        students = get_students(
            filters={'student_profile': str(student_profile.id)},
        )
        circles = get_circles_by_students(students=students, filters=request.GET.dict())
        response = get_paginated_response(
            pagination_class=ApiCircleListPagination,
            serializer_class=GetListCircleSerializer,
            queryset=circles,
            request=request,
            view=self
        )
        return response


class StudentDeleteApi(ApiAuthMixin, APIView):
    serializer_class = UpdateStudentSerializer

    @swagger_auto_schema(
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        operation_description="Delete student.",
        responses={204: "Successfully deleted", 404: "No such student"}
    )
    def delete(self, request, student_id):
        student = get_student(filters={'id': student_id}, empty_exception=True, user=request.user)
        student.delete()
        return Response(status=204)

    @swagger_auto_schema(
        tags=[SwaggerTags.STUDENT_MANAGEMENT_STUDENTS],
        operation_description="Patch student.",
        request_body=UpdateStudentSerializer,
        responses={200: convert_dict_to_serializer({"student": GetStudentSerializer()}), 404: "No such student"}
    )
    def patch(self, request, student_id):
        update_student_serializer = UpdateStudentSerializer(data=request.data)
        update_student_serializer.is_valid(raise_exception=True)

        student = get_student(filters={'id': student_id}, empty_exception=True, user=request.user)

        student = update_student(student=student, data=update_student_serializer.validated_data)

        return Response({"student": GetStudentSerializer(student, context={'request': request}).data}, status=200)
