from django.db import models
from django.urls import reverse


# Create your models here.
class Student(models.Model):
    student_no = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # ML Predict Data
    aggregate_YOS1 = models.FloatField()
    aggregate_YOS2 = models.FloatField()
    coms_avg_YOS1 = models.FloatField()
    coms_avg_YOS2 = models.FloatField()
    maths_avg_YOS1 = models.FloatField()
    maths_avg_YOS2 = models.FloatField()

    prediction = models.CharField(max_length=2)

    def predict_data(self):
        out_data = dict(
            AggregateYOS1=[self.aggregate_YOS1],
            AggregateYOS2=[self.aggregate_YOS2],
            FYComsAvg=[self.coms_avg_YOS1],
            SYComsAvg=[self.coms_avg_YOS2],
            FYMathAvg=[self.maths_avg_YOS1],
            SYMathAvg=[self.maths_avg_YOS2],
        )
        return out_data

    HIGH = 'H'
    LOW = 'L'
    MEDIUM = 'M'
    PRED_CHOICES = (
        (HIGH, 'High'),
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
    )

    def __str__(self):
        return "{} {}({})".format(self.first_name, self.last_name, self.student_no)

    def full_name(self):
        return self.first_name.capitalize() + " " + self.last_name.capitalize()

    def get_absolute_url(self):
        return reverse('student_predictor:show_all_students_selected', args=(self.pk,))

    def prediction_text(self):
        if self.prediction == "H":
            return "High Risk"
        if self.prediction == "M":
            return "Medium Risk"
        if self.prediction == "L":
            return "Low Risk"
        # If none of the above are true I 'think' this method won't crash
