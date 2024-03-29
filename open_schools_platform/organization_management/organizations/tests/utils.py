from typing import List

from open_schools_platform.common.filters import SoftCondition
from open_schools_platform.organization_management.employees.services import create_employee
from open_schools_platform.organization_management.organizations.models import Organization
from open_schools_platform.organization_management.organizations.selectors import get_organizations
from open_schools_platform.organization_management.organizations.services import create_organization
from open_schools_platform.user_management.users.models import User


def create_test_employees(user: User, organizations: List[Organization]):
    employees = []

    for organization in organizations:
        employee = create_employee(name="Andrey", position="Director", user=user, organization=organization)
        employees.append(employee)

    return employees


def create_test_organizations():
    data_organization_list = [
        {
            "name": "LamArt",
            "inn": "1"
        },
        {
            "name": "LamaBox",
            "inn": "1"
        },
        {
            "name": "Gameloft",
            "inn": "2"
        },
        {
            "name": "EA",
            "inn": "3"
        },
        {
            "name": "Rockstar Games",
            "inn": "4"
        },
    ]

    organizations = []

    for data in data_organization_list:
        organization = create_organization(**data)
        organizations.append(organization)

    return organizations


def create_test_organization(inn: str = "1111111111", name: str = "test_org"):
    return create_organization(inn=inn, name=name)


def get_deleted_organizations():
    organizations = get_organizations(filters={'DELETED': SoftCondition.DELETED_ONLY})
    return organizations
