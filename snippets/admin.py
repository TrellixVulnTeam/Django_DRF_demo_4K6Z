from django.contrib import admin

# Register your models here.
from .models import Snippet


@admin.display(description='created',
                ordering='created')
def upper_case_name(obj):
    return obj.code

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    # 修改页面的内容
    fields = ('title', 'code')
    # 修改页面只读内容
    readonly_fields  = ('code', )
    # 修改列表显示内容
    list_display = (upper_case_name,)
    # 搜索引擎搜索范围
    search_fields = ('code',)
    # 右侧过滤面板
    list_filter  = (('created',admin.DateFieldListFilter),'code')
    # 时间分类导航
    #date_hierarchy = 'created'

    empty_value_display = '-empty-'
    admin.site.empty_value_display = '???'
    actions_on_bottom = True




# admin.site.register(Snippet, SnippetAdmin)