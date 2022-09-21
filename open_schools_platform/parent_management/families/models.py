import uuid

import safedelete.models
from django.db import models
from safedelete.managers import SafeDeleteManager

from open_schools_platform.common.models import BaseModel
from open_schools_platform.parent_management.parents.models import ParentProfile
from open_schools_platform.student_management.students.models import StudentProfile


class FamilyManager(SafeDeleteManager):
    def create_family(self, name: str):
        family = self.model(
            name=name
        )
        family.full_clean()
        family.save(using=self.db)
        return family


class Family(BaseModel):
    _safedelete_policy = safedelete.models.SOFT_DELETE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    parent_profiles = models.ManyToManyField(ParentProfile, related_name="families")
    student_profiles = models.ManyToManyField(StudentProfile, related_name="families")
    name = models.CharField(max_length=200)
    objects = FamilyManager()

    def __str__(self):
        return self.name.__str__()
