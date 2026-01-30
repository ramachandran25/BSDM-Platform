from django.contrib import admin

from django.contrib import admin
from .models import ProjectRequest, RequestAttachment


class RequestAttachmentInline(admin.TabularInline):
    model = RequestAttachment
    extra = 1
    can_delete = True
    readonly_fields = ('uploaded_by', 'uploaded_at')
    fields = ('file', 'uploaded_by', 'uploaded_at')

    def has_delete_permission(self, request, obj=None):
        """
        Allow delete ONLY for ADMIN-uploaded attachments.
        Block delete for USER-uploaded attachments.
        """
        if obj is None:
            return True

        if hasattr(obj, 'uploaded_by') and obj.uploaded_by == 'USER':
            return False

        return True


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'user', 'title', 'estimated_cost', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('request_id', 'title', 'user__email')
    readonly_fields = ('request_id', 'created_at')

    inlines = [RequestAttachmentInline]

    def save_formset(self, request, form, formset, change):
        """
        REQUIRED when using inlines.

        - Sets uploaded_by = ADMIN for new admin uploads
        - Explicitly deletes admin attachments when selected
        - Protects user attachments from deletion
        """
        instances = formset.save(commit=False)

        # Save new / updated attachments
        for obj in instances:
            if not obj.pk:
                obj.uploaded_by = 'ADMIN'
            obj.save()

        # Handle deletions explicitly
        for obj in formset.deleted_objects:
            if obj.uploaded_by == 'ADMIN':
                obj.delete()

        formset.save_m2m()
    def save_model(self, request, obj, form, change):
    	if obj.estimated_cost and obj.status == 'NEW':
        	obj.status = 'ESTIMATED'
    	super().save_model(request, obj, form, change)


@admin.register(RequestAttachment)
class RequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ('project_request', 'uploaded_by', 'uploaded_at', 'file')
    list_filter = ('uploaded_by', 'uploaded_at')
    search_fields = ('project_request__request_id',)
