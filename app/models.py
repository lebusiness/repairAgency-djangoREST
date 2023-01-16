from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
# Категория
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    summary = models.TextField(blank=True, verbose_name="Краткое описание")
    descr = models.TextField(blank=True, verbose_name="Описание")
    img = models.ImageField(upload_to="photos/categories", verbose_name="Фото")

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

# Отзыв
class Feedback(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Имя")
    text = models.TextField(blank=True, verbose_name="Отзыв")
    valuation = models.IntegerField(verbose_name="Оценка")

    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория", related_name="feedbacks")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['id']

# Услуга
class Service(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    summary = models.TextField(blank=True, verbose_name="Краткое описание")
    descr = models.TextField(blank=True, verbose_name="Описание")
    img = models.ImageField(upload_to="photos/services/", verbose_name="Фото")
    price = models.IntegerField(verbose_name="Цена")

    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория", related_name="services")

    # def get_absolute_url(self):
    #     return reverse('cat_slug', kwargs={'serv_slug': self.slug})

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['id']

# Корзина
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")

    def __str__(self):
        return 'Корзина ' + str(self.user)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['id']

# Корзина-Услуга связь
class RelationCartService(models.Model):
    service = models.ForeignKey('Service', on_delete=models.PROTECT, verbose_name="Услуга")
    cart = models.ForeignKey('Cart', on_delete=models.PROTECT, verbose_name="Корзина владелец", related_name="rel_services")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина-Услуга'
        verbose_name_plural = 'Корзина-Услуга'
        ordering = ['id']

# Заказ
class Order(models.Model):
    services = models.TextField(blank=True, verbose_name="Услуги")
    number = models.CharField(max_length=100, db_index=True, verbose_name="Номер")
    price = models.IntegerField(verbose_name="Цена")
    address = models.CharField(max_length=100, db_index=True, verbose_name="Адрес", default="")

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь", default="")
    
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']