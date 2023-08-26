from django.contrib import admin

from cron.models import Job, JobSchedule


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "script")
    list_filter = ("owner",)
    search_fields = ("name", "owner", "script")


@admin.register(JobSchedule)
class JobScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "get_job_name",
        "get_job_owner",
        "description",
        "minute",
        "hour",
        "day_of_month",
        "month",
        "day_of_week",
    )

    def get_job_name(self, obj):
        return obj.job.name

    def get_job_owner(self, obj):
        return obj.job.owner

    get_job_name.short_description = "Nombre del Job"
    get_job_owner.short_description = "Dueño del Job"

    search_fields = ("description", "get_job_name", "get_job_owner")
