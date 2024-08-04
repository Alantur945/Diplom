from django.db import models

# Create your models here.
class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    
    title = models.CharField(max_length=255, verbose_name='Название')
    arcticule = models.CharField(max_length=255, verbose_name='Артикул', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    photo = models.ImageField(verbose_name='Превью', blank=True, upload_to='media/images')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    price = models.IntegerField(verbose_name="Цента")
    

    def __str__(self):
        return self.title