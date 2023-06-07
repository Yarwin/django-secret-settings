from django.contrib import admin

from models import Secret


class SecretManager(admin.ModelAdmin):
    readonly_fields = ('created_at', )


admin.site.register(Secret, SecretManager)
