from django.db import models


# Create your models here.
# More data will be added later on
class Student(models.Model):
    student_no = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return "{} {}({})".format(self.first_name, self.last_name, self.student_no)

    def full_name(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()
