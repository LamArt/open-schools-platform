import rules

from open_schools_platform.common.rules import predicate_input_type_check
from open_schools_platform.organization_management.teachers.models import TeacherProfile
from open_schools_platform.user_management.users.models import User


@rules.predicate
@predicate_input_type_check
def is_teacher_profile_owner(user: User, teacher_profile: TeacherProfile):
    return teacher_profile.user == user


rules.add_perm("teachers.teacher_profile_access", is_teacher_profile_owner)