from django.contrib import admin
from .models import Complaint, Remark


class RemarkInline(admin.TabularInline):
    model = Remark
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'room_number', 'category', 'priority', 'status', 'upvotes', 'satisfaction', 'date_filed', 'is_overdue')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('student_name', 'room_number', 'description')
    list_editable = ('status', 'priority')
    readonly_fields = ('date_filed', 'resolved_date')
    inlines = [RemarkInline]


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'complaint', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('student_name', 'content')
