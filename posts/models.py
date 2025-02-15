from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

"""
все объекты таблицы -- Post.objects.all()

один объект по условию -- Post.objects.get(id = 1)

объект по условию не уникальному(несколько) -- Post.objects.filter(title = "title")
"""


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'Категория: {self.name}'
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return f"Тэг: {self.name}"



class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=1100)    
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)],default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ManyToManyField(Tag, related_name='posts', blank=True, null=True)


    def __str__(self):
        return f"{self.title} - {self.content}"
