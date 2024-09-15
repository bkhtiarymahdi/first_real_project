from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment
import time
from taggit.managers import TaggableManager
from converter import changes
from .choices import view, type_course, status_transaction
from django.contrib.auth import get_user_model
from converter.changes import price_amount
from account.models import Profile


class BaseModel(models.Model):
    create = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    update = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    @property
    def publish(self):
        return changes.converter_date_time(self.create)

    # def elapsed_time(self):
    #     time_now = time.time
    #     return

    class Meta:
        abstract = True


class Title(BaseModel):
    header_title = models.CharField(max_length=50, verbose_name="عنوان سایت")
    descriptions = models.CharField(max_length=300, verbose_name="توضیحات")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")

    class Meta:
        verbose_name_plural = "عناوین"
        ordering = ["-id"]

    def __str__(self):
        return self.header_title

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class Category(BaseModel):
    title = models.CharField(max_length=255, unique=True, verbose_name="عنوان")
    url = models.CharField(max_length=255, verbose_name="یو ار ال")
    slug = models.SlugField(max_length=255, blank=True, verbose_name="اسلاگ")
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name="زیر مجموعه",
    )

    class Meta:
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_children(self):
        return self.children.all()


class GetIpAddress(BaseModel):
    save_ip = models.GenericIPAddressField(verbose_name="آدرس آی پی")

    class Meta:
        verbose_name_plural = "آی پی کاربر"

    def __str__(self):
        return self.save_ip


class Article(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    description = models.TextField(verbose_name="متن")
    status = models.CharField(max_length=50, choices=view, verbose_name="وضعیت")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    special = models.BooleanField(default=False, verbose_name="آیا این مقاله ویژه هست؟")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="articles"
    )
    word = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل وورد"
    )
    pdf = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل پی دی اف"
    )
    comments = GenericRelation(Comment)
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "مقالات"

    def price(self):
        return price_amount(self.amount)

    price.short_description = "قیمت"

    def __str__(self):
        return self.title

    def img_tag(self):
        return format_html("<img width=80 src='{}'>".format(self.img.url))


class Book(BaseModel):
    title = models.CharField(max_length=100, verbose_name="اسم")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="books"
    )
    description = models.TextField(null=True, blank=True, verbose_name="متن کتاب")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    special = models.BooleanField(default=False, verbose_name="آیا این کتاب ویژه هست؟")
    writer_book = models.CharField(max_length=100, verbose_name="نویسنده کتاب")
    generic = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    word = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل وورد"
    )
    pdf = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل پی دی اف"
    )
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "کتاب ها"

    def __str__(self):
        return self.name

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class Biography(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="biographes"
    )
    description = models.TextField(null=True, blank=True, verbose_name="متن")
    special = models.BooleanField(default=False, verbose_name="آیا این پست ویژه هست؟")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "زندگینامه"

    def __str__(self):
        return self.title

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class QuoteImage(BaseModel):
    title = models.CharField(max_length=20, verbose_name="عنوان")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="quote_images"
    )
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "تصویر نوشته"

    def __str__(self):
        return f"{self.img}"

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class Movie(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="movies"
    )
    special = models.BooleanField(default=False, verbose_name="آیا این فیلم ویژه هست؟")
    description = models.TextField(null=True, blank=True, verbose_name="متن سخنرانی")
    film = models.FileField(
        upload_to="movie", storage=None, max_length=100, verbose_name="بارگزاری فیلم"
    )
    duration = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="زمان فیلم"
    )
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "فیلم ها"

    def __str__(self):
        return self.title

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class Voice(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="voices"
    )
    description = models.TextField(null=True, blank=True, verbose_name="متن سخنرانی")
    special = models.BooleanField(default=False, verbose_name="آیا این صوت ویژه هست؟")
    voice = models.FileField(
        upload_to="videos", storage=None, max_length=100, verbose_name="صوت"
    )
    word = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل وورد"
    )
    pdf = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل پی دی اف"
    )
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "سخنرانی"

    def __str__(self):
        return self.title

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class ShortSound(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="shortsounds"
    )
    description = models.TextField(null=True, blank=True, verbose_name="متن سخنرانی")
    special = models.BooleanField(default=False, verbose_name="آیا این صوت ویژه هست؟")
    voice = models.FileField(
        upload_to="videos", storage=None, max_length=100, verbose_name="صوت"
    )
    word = models.FileField(
        upload_to="text",
        storage=None,
        null=True,
        blank=True,
        max_length=100,
        verbose_name="فایل وورد",
    )
    pdf = models.FileField(
        upload_to="text",
        storage=None,
        null=True,
        blank=True,
        max_length=100,
        verbose_name="فایل پی دی اف",
    )
    tag = TaggableManager()

    class Meta:
        verbose_name_plural = "صوت های کوتاه"

    def __str__(self):
        return self.title

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class OnlineCourse(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="onlines"
    )
    description = models.TextField(verbose_name="توضیحات")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    special = models.BooleanField(default=False, verbose_name="آیا این دوره ویژه هست؟")
    amount = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="مبلغ")
    word = models.FileField(
        upload_to="text",
        storage=None,
        blank=True,
        null=True,
        max_length=100,
        verbose_name="فایل وورد",
    )
    pdf = models.FileField(
        upload_to="text",
        storage=None,
        blank=True,
        null=True,
        max_length=100,
        verbose_name="فایل پی دی اف",
    )
    video = models.FileField(
        upload_to="videos",
        storage=None,
        blank=True,
        null=True,
        max_length=100,
        verbose_name="فیلم",
    )
    tag = TaggableManager()

    def activate_for_user(self, user):
        User_Access.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        )

    def price(self):
        return price_amount(self.amount)

    price.short_description = "قیمت"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "دوره غیر حضوری"

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class InPersonCourse(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="in_persons"
    )
    description = models.TextField(verbose_name="توضیحات")
    special = models.BooleanField(default=False, verbose_name="آیا این دوره ویژه هست؟")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    capacity = models.PositiveIntegerField(
        blank=True, null=True, default=1, verbose_name="ظرفیت"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="مبلغ")
    list_of_registered_people = models.TextField(
        blank=True, null=True, verbose_name="اسامی افراد ثبت نام شده"
    )
    # Registrants = models.PositiveIntegerField(default=0, verbose_name="تعداد شرکت کننده ها")
    tag = TaggableManager()

    # def activate_for_user(self, user):
    #     User_Access.objects.create(user=user, in_person_course=self)

    # def is_pay(self):
    #     print(self.user_accesses.all())
    #     return self.user_accesses.all()
    # print(InPersonCourse.)

    def activate_for_user(self, user):
        User_Access.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        )

    def price(self):
        return price_amount(self.amount)

    price.short_description = "قیمت"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "دوره حضوری"

    def img_tag(self):
        return format_html("<img src='{}'>".format(self.img.url))


class Pamphlets(BaseModel):
    title = models.CharField(max_length=100, verbose_name="عنوان")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی ", related_name="pamphlets"
    )
    description = models.TextField(verbose_name="توضیحات")
    special = models.BooleanField(default=False, verbose_name="آیا این دوره ویژه هست؟")
    img = models.ImageField(upload_to="image", verbose_name="تصویر")
    word = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل وورد"
    )
    pdf = models.FileField(
        upload_to="text", storage=None, max_length=100, verbose_name="فایل پی دی اف"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="مبلغ")
    tag = TaggableManager()

    def activate_for_user(self, user):
        User_Access.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
        )

    def price(self):
        return price_amount(self.amount)

    price.short_description = "قیمت"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "جزوات"

    def img_tag(self):
        return format_html("<img src='{}'/>".format(self.img.url))


class Order(BaseModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="کاربر"
    )
    is_paid = models.BooleanField(default=False, verbose_name="آیا پرداخت شده است؟")
    total_amount = models.DecimalField(
        max_digits=10,
        null=True,
        default=0,
        blank=True,
        decimal_places=3,
        verbose_name="جمع مبالغ",
    )

    def __str__(self):
        return self.user.get_username()

    class Meta:
        verbose_name_plural = "سفارشات"


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE, verbose_name="سفارش"
    )
    in_person_course = models.ForeignKey(
        InPersonCourse,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="دوره حضوری",
    )
    online_course = models.ForeignKey(
        OnlineCourse,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="دوره آنلاین",
    )
    pamphlets = models.ForeignKey(
        Pamphlets, null=True, blank=True, on_delete=models.CASCADE, verbose_name="جزوات"
    )
    quantity = models.PositiveIntegerField(
        default=1, blank=True, null=True, verbose_name="تعداد"
    )
    price = models.DecimalField(
        max_digits=10,
        default=1,
        blank=True,
        null=True,
        decimal_places=3,
        verbose_name="قیمت",
    )

    def save(self, *args, **kwargs):
        if self.in_person_course:
            self.price = self.in_person_course.amount
        elif self.online_course:
            self.price = self.online_course.amount
        elif self.online_course:
            self.price = self.pamphlets.amount

        super(OrderItem, self).save(*args, **kwargs)

    # def __str__(self):
    #     return Order.__str__()

    class Meta:
        verbose_name_plural = "موارد سفارش شده"


class Transaction(BaseModel):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="transactions"
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(max_length=20, choices=status_transaction)

    def __str__(self):
        self.order_number

    class Meta:
        verbose_name_plural = "پرداخت ها"


class User_Access(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    purchased_item = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.user.username} - {self.purchased_item}"

    class Meta:
        verbose_name_plural = "دسترسی های کاربر به دوره ها"
