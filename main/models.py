from django.db import models, connection

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='students/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='учится')
    info = models.TextField(verbose_name='Информация о студенте', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ('last_name',)
