from django import forms

from  .models import Asset
class AddAssetModelForm(forms.ModelForm):

    class Meta:
        model = Asset
        exclude = ['create_time','update_time','mac_addr','virtual','kernelrelease','dns','osrelease','cpu_model']
        help_texts ={
            'inner_ip': '*必填',
        }
        labels = {
            'inner_ip':'内网IP',
            'pub_ip':'公网IP',
            'hostname':'主机名',
            'port':'端口号',
        }
        widgets = {
            'inner_ip':forms.TextInput(attrs={'class':'form-control','placeholder':'请输入内网IP','cols': 80, 'rows': 20}),
            'pub_ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入外网IP','cols': 80, 'rows': 20}),
            'hostname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入主机名',}),
            'port': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入端口号', 'cols': 80, 'rows': 20}),
            'mem_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入内存值', 'cols': 80, 'rows': 20}),
        }