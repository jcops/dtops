from django.conf.urls import url


from  .views import AssetListView,SystemUserListAllView,ProductLineListAllView,AddAssetView,DelAssetView,\
    AssetDetailView,AssetUpdateView,auto_update_assets,AssetWebView,AddSysUserView,Del_SysUserView,SysUserDetailView,SysUserUpdateView,ExAssetView,ImAssetView

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

    # 刷新全部资产
    url(r'auto_update_assets/$', auto_update_assets.as_view(), name='assets_update'),
    # 资产终端
    url(r'assetweb/$', AssetWebView.as_view(), name='asset_web'),
    # 添加系统用户
    url(r'sysuser_create/$', AddSysUserView.as_view(), name='sysuser_create'),
    # 删除系统用户
    url(r'del_sysuser/$', Del_SysUserView.as_view(), name='del_sysuser'),
    # 系统用户详情
    url(r'system_user_detail/(?P<pk>\d+)/$', SysUserDetailView.as_view(), name='system_user_detail'),
    # 系统用户更新
    url(r'sysuser_update/(?P<pk>\d+)/$', SysUserUpdateView.as_view(), name='sysuser_update'),
    # 资产导出
    url(r'ex_asset/$', ExAssetView.as_view(), name='ex_asset'),
    # 资产导入
    url(r'im_asset/$', ImAssetView.as_view(), name='im_asset'),
]