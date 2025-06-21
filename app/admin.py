from django.contrib import admin
from .models import Table, Category, Booking, Foods, Menu
# Register your models here.

admin.site.register(Table),
admin.site.register(Category),
admin.site.register(Booking),
admin.site.register(Foods),


class MenuAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "foods":
            category_id = (
                request.POST.get("category") or
                request.GET.get("category") or
                request.resolver_match.kwargs.get("object_id") and
                Menu.objects.filter(id=request.resolver_match.kwargs["object_id"]).values_list("category_id", flat=True).first()
            )

            if category_id:
                kwargs["queryset"] = Foods.objects.filter(category_id=category_id)
            else:
                kwargs["queryset"] = Foods.objects.all()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Menu, MenuAdmin)
