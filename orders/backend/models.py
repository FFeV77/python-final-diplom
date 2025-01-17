from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),

)


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class User(AbstractUser):
    email = models.EmailField(
        'email',
        unique=True,
        db_index=True
        )
    type = models.CharField(
        'тип пользователя',
        choices=USER_TYPE_CHOICES,
        default='buyer',
        max_length=5
        )
    is_active = models.BooleanField(
        ("active"),
        default=False,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    father_name = models.CharField(
        'отчество',
        max_length=150,
        blank=True
        )
    company = models.CharField('Компания', max_length=150, blank=True)
    position = models.CharField('должность', max_length=150, blank=True)
    username = models.CharField('username', max_length=150,
                                help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[UnicodeUsernameValidator()],
                                error_messages={
                                                'unique': ("A user with that username already exists."),
                                                },
                                )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Shop(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=50,
                            )
    url = models.URLField(verbose_name='Ссылка',
                          null=True,
                          blank=True
                          )
    filename = models.FileField(verbose_name='Файл',
                                upload_to='uploads/',
                                null=True,
                                blank=True
                                )
    user = models.OneToOneField(User, verbose_name='Пользователь',
                                blank=True, null=True,
                                on_delete=models.CASCADE
                                )
    state = models.BooleanField(verbose_name='статус получения заказов',
                                default=True
                                )

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(verbose_name='Название',
                            max_length=40
                            )
    shops = models.ManyToManyField(Shop, verbose_name='Магазины',
                                   related_name='categories',
                                   blank=True
                                   )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Название',
                            max_length=80
                            )
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 related_name='products',
                                 blank=True,
                                 on_delete=models.CASCADE
                                 )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Список продуктов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    model = models.CharField(verbose_name='Модель',
                             max_length=80,
                             blank=True
                             )
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
    product = models.ForeignKey(Product, verbose_name='Продукт',
                                related_name='product_infos',
                                blank=True,
                                on_delete=models.CASCADE
                                )
    shop = models.ForeignKey(Shop, verbose_name='Магазин',
                             related_name='product_infos',
                             blank=True,
                             on_delete=models.CASCADE
                             )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информационный список о продуктах"
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'shop', 'model', 'external_id'],
                name='unique_product_info'
            ),
        ]


class Parameter(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название'
        )

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список имен параметров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='product_parameters',
                                     blank=True,
                                     on_delete=models.CASCADE
                                     )
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр',
                                  related_name='product_parameters',
                                  blank=True,
                                  on_delete=models.CASCADE
                                  )
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров"
        constraints = [
            models.UniqueConstraint(
                fields=['product_info', 'parameter'],
                name='unique_product_parameter'
            ),
        ]


class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='contacts', blank=True,
                             on_delete=models.CASCADE
                             )
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE
                             )
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус',
                             default='basket',
                             choices=STATE_CHOICES,
                             max_length=15
                             )
    contact = models.ForeignKey(Contact, verbose_name='Контакт',
                                blank=True, null=True,
                                on_delete=models.CASCADE
                                )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)

    @property
    def total(self):
        return sum(item.sum for item in self.ordered_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ',
                              related_name='ordered_items',
                              blank=True,
                              on_delete=models.CASCADE
                              )
    product_info = models.ForeignKey(ProductInfo,
                                     verbose_name='Информация о продукте',
                                     related_name='ordered_items',
                                     blank=True,
                                     on_delete=models.CASCADE
                                     )
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"
        constraints = [
            models.UniqueConstraint(
                fields=['order_id', 'product_info'],
                name='unique_order_item'
            ),
        ]

    @property
    def sum(self):
        return self.product_info.price * self.quantity
