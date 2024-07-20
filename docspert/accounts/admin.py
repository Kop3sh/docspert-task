from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.formats import base_formats

from .models import Account, Transaction

class AccountResource(resources.ModelResource):
    # id = fields.Field(attribute='ID', column_name='id')
    # name = fields.Field(attribute='Name', column_name='name')
    # balance = fields.Field(attribute='Balance', column_name='balance')

    class Meta:
        model = Account
        import_id_fields = ['id',]

    def before_import(self, dataset, **kwargs):
        # Lowercase all column names if they are a string
        dataset.headers = [header.lower() if isinstance(header, str) else header for header in dataset.headers]

class AccountAdmin(ImportExportModelAdmin):
    resource_classes = [AccountResource]
    readonly_fields = ('id',)

    def get_import_formats(self):
        return [base_formats.CSV]


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction)

