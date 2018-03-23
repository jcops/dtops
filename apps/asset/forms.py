from django import forms

from  .models import Asset
class AddAssetModelForm(forms.ModelForm):

    class Meta:
        model = Asset
        # fields = ['hostname','inner_ip','pub_ip']
        exclude = ['create_time','update_time','mac_addr','virtual','kernelrelease','dns','osrelease','cpu_model','serialnumber',]
        #
        help_texts ={
            'inner_ip': '*必填',
        }
        labels = {
            'inner_ip':'内网IP:',
            'pub_ip':'公网IP:',
            'hostname':'主机名:',
            'system_user': '系统用户:',
            'port':'端口号:',
            'status':'状态:',
            'osfinger': '系统版本:',
            'detail': '备注:',
            'product': '产品线:',
            'cloud_platform':'云平台:',
            'tag': '标签:',



        }
        widgets = {
            'inner_ip':forms.TextInput(
                attrs={'class':'form-control','placeholder':'请输入内网IP','cols': 80, 'rows': 20}),
            'pub_ip': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '请输入外网IP','cols': 80, 'rows': 20}),
            'hostname': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '请输入主机名',}),
            'port': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '请输入端口号', 'cols': 80, 'rows': 20}),
            'mem_total': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '请输入内存大小', 'cols': 80, 'rows': 20}),
            'status': forms.Select(
                attrs={'class': 'form-control',}),
            'system_user': forms.Select(
                attrs={'class': 'select2','data-placeholder': '-------请选择系统用户---------',}),
            'disk_total': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '请输入磁盘大小', 'cols': 80, 'rows': 20}),
            'num_cpus': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '请输入CPU核数', 'cols': 80, 'rows': 20}),
            'osfinger': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '请输入系统版本', 'cols': 80, 'rows': 20}),
            'detail': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': '备注信息', 'cols': 20, 'rows': 3}),
            'product': forms.Select(
                attrs={'class': 'select2', 'data-placeholder': '-------请选择产品线------------',}),
            'cloud_platform': forms.Select(
                attrs={'class': 'select2','data-placeholder': '-------请选择云平台---------' }),    ##select是bootstrap的高级功能
            'tag': forms.SelectMultiple(
                attrs={'class': 'select2', }),


        }
