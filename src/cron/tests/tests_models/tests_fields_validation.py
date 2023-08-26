from django.forms import ValidationError
from django.test import TestCase

from cron.models import JobSchedule, Job


class JobScheduleValidateModelFieldsTestCase(TestCase):
    """Test class for the validate_allowed_chars function of the JobSchedule model."""

    def setUp(self):
        self.job_name = "Test job name"
        self.job = Job.objects.create(
            name=self.job_name, owner="Sergio", script="test_script.py"
        )

    def test_validate_minute_with_numbers(self):
        field_value = "1,2,3,4,5"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            minute=field_value,
        )

        self.assertEquals(self.job_schedule.minute, field_value)

    def test_validate_minute_with_consecutive_commas(self):
        field_value = "1,2,3,4,,5"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            minute=field_value,
        )

        self.assertEquals(self.job_schedule.minute, field_value)

    def test_validate_minute_with_asterisk(self):
        field_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            minute=field_value,
        )

        self.assertEquals(self.job_schedule.minute, field_value)

    def test_validate_minute_with_default(self):
        default_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

        self.assertEquals(self.job_schedule.minute, default_value)

    def test_validate_minute_with_numbers_out_of_range(self):
        field_value = "1,30,61"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                minute=field_value,
            )

    def test_validate_minute_with_invalid_values(self):
        field_value = "1-30/2"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                minute=field_value,
            )

    def test_validate_hour_with_numbers(self):
        field_value = "1,2,3,4,5"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            hour=field_value,
        )

        self.assertEquals(self.job_schedule.hour, field_value)

    def test_validate_hour_with_asterisk(self):
        field_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            hour=field_value,
        )

        self.assertEquals(self.job_schedule.hour, field_value)

    def test_validate_hour_with_default(self):
        default_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

        self.assertEquals(self.job_schedule.minute, default_value)

    def test_validate_hour_with_numbers_out_of_range(self):
        field_value = "1,30,61,62"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                hour=field_value,
            )

    def test_validate_hour_with_invalid_values(self):
        field_value = "1-30/2"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                hour=field_value,
            )

    def test_validate_day_of_month_with_numbers(self):
        field_value = "1,2,3,4,5"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            day_of_month=field_value,
        )

        self.assertEquals(self.job_schedule.day_of_month, field_value)

    def test_validate_day_of_month_with_asterisk(self):
        field_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            day_of_month=field_value,
        )

        self.assertEquals(self.job_schedule.day_of_month, field_value)

    def test_validate_day_of_month_with_default(self):
        default_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

        self.assertEquals(self.job_schedule.minute, default_value)

    def test_validate_day_of_month_with_numbers_out_of_range(self):
        field_value = "1,10,32"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                day_of_month=field_value,
            )

    def test_validate_day_of_month_with_invalid_values(self):
        field_value = "1-30/2"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                day_of_month=field_value,
            )

    def test_validate_month_with_numbers(self):
        field_value = "1,2,3,4,5"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            month=field_value,
        )

        self.assertEquals(self.job_schedule.month, field_value)

    def test_validate_month_with_asterisk(self):
        field_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            month=field_value,
        )

        self.assertEquals(self.job_schedule.month, field_value)

    def test_validate_month_with_default(self):
        default_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

        self.assertEquals(self.job_schedule.minute, default_value)

    def test_validate_month_with_numbers_out_of_range(self):
        field_value = "10,11,12,13"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                month=field_value,
            )

    def test_validate_month_with_invalid_values(self):
        field_value = "1-5"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                month=field_value,
            )

    def test_validate_day_of_week_with_numbers(self):
        field_value = "1,2,3,4,5"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            day_of_week=field_value,
        )

        self.assertEquals(self.job_schedule.day_of_week, field_value)

    def test_validate_day_of_week_with_asterisk(self):
        field_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            day_of_week=field_value,
        )

        self.assertEquals(self.job_schedule.day_of_week, field_value)

    def test_validate_day_of_week_with_default(self):
        default_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

        self.assertEquals(self.job_schedule.minute, default_value)

    def test_validate_day_of_week_with_numbers_out_of_range(self):
        field_value = "0,5,6,7,8"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                day_of_week=field_value,
            )

    def test_validate_day_of_week_with_invalid_values(self):
        field_value = "1-5"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                day_of_week=field_value,
            )

    def test_validate_year_with_numbers(self):
        field_value = "2023,2024"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            year=field_value,
        )

        self.assertEquals(self.job_schedule.year, field_value)

    def test_validate_year_with_asterisk(self):
        field_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
            year=field_value,
        )

        self.assertEquals(self.job_schedule.year, field_value)

    def test_validate_year_with_default(self):
        default_value = "*"

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

        self.assertEquals(self.job_schedule.minute, default_value)

    def test_validate_year_with_numbers_out_of_range(self):
        field_value = "2023, 10000"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                year=field_value,
            )

    def test_validate_year_with_invalid_values(self):
        field_value = "2023-2025"

        with self.assertRaises(ValidationError):
            self.job_schedule = JobSchedule.objects.create(
                job=self.job,
                description="Test description",
                year=field_value,
            )
