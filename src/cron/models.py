import uuid

from django.db import models
from django.forms import ValidationError


class Job(models.Model):
    """Model that describes a Job or RPA"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nombre", unique=True)
    owner = models.CharField(max_length=255, verbose_name="Responsable")
    script = models.CharField(max_length=200, verbose_name="Fichero", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ["name"]


class JobSchedule(models.Model):
    """Model taht describes the schedules on which the job will be executed"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(
        max_length=255, verbose_name="Descripción", blank=True, null=True
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="schedules")
    minute = models.CharField(
        max_length=255,
        default="0",
        verbose_name="Minutos",
        help_text="Minutos donde se iniciará la ejecución. Deben ser números entre el 0 y el 59 separados por comas.",
    )
    hour = models.CharField(
        max_length=255,
        default="*",
        verbose_name="Horas",
        help_text="Horas donde se iniciará la ejecución. Deben ser números entre el 0 y el 23 separados por comas.",
    )
    day_of_month = models.CharField(
        max_length=255,
        default="*",
        verbose_name="Día del mes",
        help_text="Días del mes donde se iniciará la ejecución. Deben ser números entre el 1 y el 31 (O la cantidad de día del mes) separados por comas.",
    )
    month = models.CharField(
        max_length=255,
        default="*",
        verbose_name="Meses",
        help_text="Meses donde se iniciará la ejecución. Deben ser números entre el 1 (Enero) y el 12 (Diciembre) separados por comas.",
    )
    day_of_week = models.CharField(
        max_length=255,
        default="*",
        verbose_name="Día de la semana",
        help_text="Días de la semana donde se iniciará la ejecución. Deben ser números entre el 1 (Lunes) y el 7 (Domingo) separados por comas.",
    )
    year = models.CharField(
        max_length=255,
        default="*",
        verbose_name="Años",
        help_text="Años donde se iniciará la ejecución. Deben ser un número de 4 dígitos.",
    )

    def __str__(self):
        return (
            f"{self.job.name} | {self.description}"
            if self.description
            else self.job.name
        )

    class Meta:
        verbose_name = "Horario de Job"
        verbose_name_plural = "Horarios de Jobs"
        ordering = ["job", "description"]

    def validate_allowed_chars(self, field_value, field_name) -> bool:
        """Validates whether the provided field value contains only allowed characters.

        Args:
            field_value (str): The value to be validated.
            field_name (str): The name of the field being validated.

        Raises:
            ValidationError: If the field value contains invalid characters.

        Returns:
            bool: True if validation passes.
        """

        allowed_chars = set("*,0123456789")
        if not all(char in allowed_chars for char in field_value):
            raise ValidationError(f"Invalid characters in {field_name} field")

        return True

    def validate_asterisk_use(self, field_value, field_name) -> bool:
        """Validates the usage of asterisk (*) in the field value.

        The asterisk means 'all' the possible values of the field. If there is an asterisk on the
        field, there must not be any number.

        Args:
            field_value (str): The value to be validated.
            field_name (str): The name of the field being validated.

        Raises:
            ValidationError: If asterisk (*) is used incorrectly in the field value.

        Returns:
            bool: True if validation passes.
        """

        if "*" in field_value:
            if field_value.count("*") > 1:
                raise ValidationError(f"Only one * is allowed in {field_name}")

            if any(value.isdigit() for value in field_value.split(",")):
                raise ValidationError(
                    f"Cannot use * with other numbers in {field_name}"
                )

            return True

        return False

    def validate_values_in_range(self, value_range, field_value, field_name) -> bool:
        """Validates whether the values in the field value are within the specified range.

        Args:
            value_range (list[int]): A list containing the minimum and maximum allowed values.
            field_value (str): The value to be validated.
            field_name (str): The name of the field being validated.

        Raises:
            ValidationError: If values are outside the allowed range.

        Returns:
            bool: True if validation passes.
        """

        min_value, max_value = value_range
        field_values = field_value.split(",")

        if "*" in field_values:
            raise ValidationError(f"Cannot use * with other numbers in {field_name}")

        for value in field_values:
            if value == "":
                pass
            elif not (min_value <= int(value) <= max_value):
                raise ValidationError(
                    f"{field_name} value must be between {min_value} and {max_value}."
                )

        return True

    def validate_minute(self):
        """Validates the 'minute' field based on allowed characters, asterisk usage, and value range."""

        value_range = [0, 59]
        field_value = self.minute
        field_name = "minute"

        self.validate_allowed_chars(field_value, field_name)

        if not self.validate_asterisk_use(field_value, field_name):
            self.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )

    def validate_hour(self):
        """Validates the 'hour' field based on allowed characters, asterisk usage, and value range."""

        value_range = [0, 23]
        field_value = self.hour
        field_name = "hour"

        self.validate_allowed_chars(field_value, field_name)

        if not self.validate_asterisk_use(field_value, field_name):
            self.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )

    def validate_day_of_month(self):
        """Validates the 'day_of_month' field based on allowed characters, asterisk usage, and value range."""

        value_range = [1, 31]
        field_value = self.day_of_month
        field_name = "day_of_month"

        self.validate_allowed_chars(field_value, field_name)

        if not self.validate_asterisk_use(field_value, field_name):
            self.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )

    def validate_month(self):
        """Validates the 'month' field based on allowed characters, asterisk usage, and value range."""

        value_range = [1, 12]
        field_value = self.month
        field_name = "month"

        self.validate_allowed_chars(field_value, field_name)

        if not self.validate_asterisk_use(field_value, field_name):
            self.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )

    def validate_day_of_week(self):
        """Validates the 'day_of_week' field based on allowed characters, asterisk usage, and value range."""

        value_range = [1, 7]
        field_value = self.day_of_week
        field_name = "day_of_week"

        self.validate_allowed_chars(field_value, field_name)

        if not self.validate_asterisk_use(field_value, field_name):
            self.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )

    def validate_year(self):
        """Validates the 'year' field based on allowed characters, asterisk usage, and value range."""

        value_range = [0, 9999]
        field_value = self.year
        field_name = "year"

        self.validate_allowed_chars(field_value, field_name)

        if not self.validate_asterisk_use(field_value, field_name):
            self.validate_values_in_range(
                value_range=value_range,
                field_value=field_value,
                field_name=field_name,
            )

    def clean(self):
        self.validate_minute()
        self.validate_hour()
        self.validate_day_of_month()
        self.validate_month()
        self.validate_day_of_week()
        self.validate_year()

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
