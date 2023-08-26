from django.forms import ValidationError
from django.test import TestCase

from cron.models import JobSchedule, Job


class JobScheduleValidateAllowedCharsFunctionTestCase(TestCase):
    """Test class for the validate_allowed_chars function of the JobSchedule model."""

    def setUp(self):
        self.job_name = "Test job name"
        self.job = Job.objects.create(
            name=self.job_name, owner="Sergio", script="test_script.py"
        )

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

    def test_validate_allowed_chars_with_numbers(self):
        field_value = "1,2,3,4,5"
        field_name = "day_of_week"

        self.assertTrue(
            self.job_schedule.validate_allowed_chars(
                field_value=field_value,
                field_name=field_name,
            )
        )

    def test_validate_allowed_chars_with_asterisk(self):
        field_value = "*"
        field_name = "day_of_week"

        self.assertTrue(
            self.job_schedule.validate_allowed_chars(
                field_value=field_value,
                field_name=field_name,
            )
        )

    def test_validate_allowed_chars_with_non_allowed_chars(self):
        field_value = "1-5"
        field_name = "day_of_week"
        expected_message = f"Invalid characters in {field_name} field"

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=expected_message,
        ):
            self.job_schedule.validate_allowed_chars(
                field_value=field_value,
                field_name=field_name,
            )


class JobScheduleValidateAsteriskUseTestCase(TestCase):
    """Test class for the validate_asterisk_use function of the JobSchedule model."""

    def setUp(self):
        self.job_name = "Test job name"
        self.job = Job.objects.create(
            name=self.job_name, owner="Sergio", script="test_script.py"
        )

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

    def test_validate_asterisk_use_with_asterisk_only(self):
        field_value = "*"
        field_name = "day_of_week"

        self.assertTrue(
            self.job_schedule.validate_asterisk_use(
                field_value=field_value,
                field_name=field_name,
            )
        )

    def test_validate_asterisk_use_with_many_consecutive_asterisks(self):
        field_value = "**"
        field_name = "day_of_week"
        expected_message = f"Only one * is allowed in {field_name}"

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=expected_message,
        ):
            self.job_schedule.validate_asterisk_use(
                field_value=field_value,
                field_name=field_name,
            )

    def test_validate_asterisk_use_with_many_comma_separated_asterisks(self):
        field_value = "*,*"
        field_name = "day_of_week"
        expected_message = f"Only one * is allowed in {field_name}"

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=expected_message,
        ):
            self.job_schedule.validate_asterisk_use(
                field_value=field_value,
                field_name=field_name,
            )

    def test_validate_asterisk_use_with_asterisk_and_numbers(self):
        field_value = "1,2,*"
        field_name = "day_of_week"
        expected_message = f"Cannot use * with other numbers in {field_name}"

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=expected_message,
        ):
            self.job_schedule.validate_asterisk_use(
                field_value=field_value,
                field_name=field_name,
            )

    def test_validate_asterisk_use_without_asterisk(self):
        field_value = "1,2,3"
        field_name = "day_of_week"

        self.assertFalse(
            self.job_schedule.validate_asterisk_use(
                field_value=field_value,
                field_name=field_name,
            )
        )


class JobScheduleValidateValuesInRangeTestCase(TestCase):
    """Test class for the validate_values_in_range function of the JobSchedule model."""

    def setUp(self):
        self.job_name = "Test job name"
        self.job = Job.objects.create(
            name=self.job_name, owner="Sergio", script="test_script.py"
        )

        self.job_schedule = JobSchedule.objects.create(
            job=self.job,
            description="Test description",
        )

    def test_validate_values_in_range_with_asterisk(self):
        field_value = "1,2,*"
        field_name = "day_of_week"
        expected_message = f"Cannot use * with other numbers in {field_name}"

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=expected_message,
        ):
            self.job_schedule.validate_asterisk_use(
                field_value=field_value,
                field_name=field_name,
            )

    def test_validate_values_in_range_values_in_range(self):
        value_range = [1, 7]  # [min, max]
        field_value = "1,2,3,4,5"
        field_name = "day_of_week"

        self.assertTrue(
            self.job_schedule.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )
        )

    def test_validate_values_in_range_values_out_of_range(self):
        value_range = [1, 7]
        field_value = "1,2,8"
        field_name = "day_of_week"
        expected_message = (
            f"{field_name} value must be between {value_range[0]} and {value_range[1]}."
        )

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message=expected_message,
        ):
            self.job_schedule.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )
