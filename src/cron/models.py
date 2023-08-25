from django.db import models
from django.forms import ValidationError


class Job(models.Model):
    """Model that describes a Job or RPA"""

    id = models.UUIDField()
    name = models.CharField(max_length=255, verbose_name="Nombre")
    owner = models.CharField(max_length=255, verbose_name="Responsable")
    script = models.CharField(max_length=200, verbose_name="Fichero")

    def __str__(self):
        return self.name


class JobSchedule(models.Model):
    """Model taht describes the schedules on which the job will be executed"""

    id = models.UUIDField()
    description = models.CharField(max_length=255, verbose_name="Nombre")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="schedules")
    minute = models.CharField(
        max_length=255,
        default="*",
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
        return f"{self.name} - {self.job.name}"

    def validate_allowed_chars(self, field_value, field_name):
        allowed_chars = set("*,0123456789")
        if not all(char in allowed_chars for char in field_value):
            raise ValidationError(f"Invalid characters in {field_name} field")

    def validate_all_char(self, field_value, field_name):
        if "*" in field_value:
            if field_value.count("*") > 1:
                raise ValidationError(f"Only one * is allowed in {field_name}")

            if any(value.isdigit() for value in field_value.split(",")):
                raise ValidationError(
                    f"Cannot use * with other numbers in {field_name}"
                )

            return True

        return False

    def validate_values_in_range(self, value_range, field_values, field_name):
        min_value, max_value = value_range

        for value in field_values:
            if value != "*" and not (min_value <= int(value) <= max_value):
                raise ValidationError(
                    f"{field_name} value must be between {min_value} and {max_value}."
                )

    def validate_minute(self):
        self.validate_allowed_chars(self.minute)

        minutes = self.minute.split(",")

    def validate_hour(self):
        self.validate_allowed_chars(self.hour)

    def validate_day_of_month(self):
        self.validate_allowed_chars(self.day_of_month)

    def validate_month(self):
        self.validate_allowed_chars(self.month)

    def validate_day_of_week(self):
        self.validate_allowed_chars(self.day_of_week)

        if not self.validate_all_char(self.day_of_week):
            self.validate_values_in_range(
                value_range=[1, 7],
                field_values=self.day_of_week.split(","),
                field_name="day_of_week",
            )

    def validate_year(self):
        self.validate_allowed_chars(self.year)

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
