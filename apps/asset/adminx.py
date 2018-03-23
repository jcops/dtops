from xadmin import views
import  xadmin
from  .models import Asset,System_User,ProductLine,Tag,Cloud_Platform

@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True




@xadmin.sites.register(Asset)
class assets(object):
    search_fields = ('pub_ip', 'inner_ip','hostname')  #义搜索# 定框以哪些字段可以搜索
    list_display = ('cloud_platform', 'inner_ip', 'pub_ip', 'product', 'system_user',)  # 每行的显示信息
    # list_display_links = ('model',)
    list_filter = ("product",)

@xadmin.sites.register(System_User)
class SUser(object):
    search_fields = ('name', 'username',)  #义搜索# 定框以哪些字段可以搜索
    list_display = ('name', 'username', 'create_time', 'detail',)  # 每行的显示信息
    # list_display_links = ('model',)
    list_filter = ('username','name',)

@xadmin.sites.register(ProductLine)
class Product(object):
    search_fields = ('name', 'detail',)  #义搜索# 定框以哪些字段可以搜索
    list_display = ('name', 'detail', 'create_time', 'detail',)  # 每行的显示信息
    # list_display_links = ('model',)
    list_filter = ('detail','name',)

@xadmin.sites.register(Tag)
class Tag(object):
    search_fields = ('name',)  #义搜索# 定框以哪些字段可以搜索
    list_display = ('name', 'create_time', 'update_time',)  # 每行的显示信息
    # list_display_links = ('model',)
    list_filter = ('name',)

@xadmin.sites.register(Cloud_Platform)
class Cloud_Pl(object):
    search_fields = ('name','cloud',)  #义搜索# 定框以哪些字段可以搜索
    list_display = ('name','cloud', 'detail','create_time', 'update_time',)  # 每行的显示信息
    # list_display_links = ('model',)
    list_filter = ('name','cloud','detail',)