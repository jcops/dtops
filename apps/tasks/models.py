from django.db import models

# Create your models here.
class KeyList(models.Model):
    STATUS_CHOICES = (
        ('1','认证'),
        ('2','未认证')
    )
    name = models.CharField(max_length=50,verbose_name='key名',unique=True)
    status = models.BooleanField(choices=STATUS_CHOICES,verbose_name='状态')

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name = 'key列表'
        verbose_name_plural = verbose_name

