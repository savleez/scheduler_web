from django.forms import ValidationError
from django.test import TestCase

from cron.models import JobSchedule, Job


class JobScheduleValidationFunctionsTestCase(TestCase):

    def setUp(self):
        self.job_name = "Test job name"
        Job.objects.create(name=self.job_name, owner="Sergio", script="test_script.py")

    def test_validate_allowed_chars_with_numbers(self):
        job = Job.objects.get(name=self.job_name)
        job_schedule = JobSchedule.objects.create(name="Test", )

    def test_validate_all_char_with_asterisk_only(self):
        job_schedule = JobSchedule(day_of_week="*")
        self.assertTrue(job_schedule.validate_all_char("*", "day_of_week"))
    
    def test_validate_all_char_with_many_asterisks_only(self):
        job_schedule = JobSchedule(day_of_week="*,*")

    def test_validate_all_char_with_asterisk_and_numbers(self):
        job_schedule = JobSchedule(day_of_week="1,2,*")
        with self.assertRaisesMessage(
            ValidationError, "Cannot use * with other numbers in day_of_week"
        ):
            job_schedule.validate_all_char("1,2,*", "day_of_week")

    def test_validate_all_char_without_asterisk(self):
        job_schedule = JobSchedule(day_of_week="1,2,3")
        self.assertFalse(job_schedule.validate_all_char("1,2,3", "day_of_week"))

    def test_validate_values_in_range_valid_values(self):
        job_schedule = JobSchedule()
        job_schedule.validate_values_in_range(
            [1, 7], ["1", "2", "3"], "day_of_week"
        )  # No exception expected

    def test_validate_values_in_range_invalid_value(self):
        job_schedule = JobSchedule()
        with self.assertRaisesMessage(
            ValidationError, "day_of_week value must be between 1 and 7."
        ):
            job_schedule.validate_values_in_range([1, 7], ["0", "8"], "day_of_week")
