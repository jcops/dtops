from django.conf.urls import url


from  .views import AssetListView,SystemUserListAllView,ProductLineListAllView,AddAssetView,DelAssetView,AssetDetailView,AssetUpdateView

app_name = 'asset'
urlpatterns = [
    #资产列表
    url(r'asset_list/$', AssetListView.as_view(), name='asset_list'),
    # 添加资产
    url(r'add/$', AddAssetView.as_view(), name='asset_add'),
    # 资产详情
    url(r'asset_detail/(?P<pk>\d+)/$', AssetDetailView.as_view(), name='asset_detail'),
    # 资产更新
    url(r'asset_update/(?P<pk>\d+)/$', AssetUpdateView.as_view(), name='asset_update'),
    # 资产删除
    url(r'asset_del/$', DelAssetView.as_view(), name='del_asset'),
    #系统用户列表
    url(r'system_user/$', SystemUserListAllView.as_view(), name='system_user'),
    #产品线列表
    url(r'product_list/$', ProductLineListAllView.as_view(), name='product_list'),

]