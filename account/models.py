from django.db import models
from django.contrib.auth.models import User
from common.models import BaseModel
from common.choices import citys


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profiles", verbose_name="کاربر"
    )
    avatar = models.ImageField(
        upload_to="image/", null=True, blank=True, verbose_name="تصویر صورت"
    )
    city = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        choices=citys,
        verbose_name="شهر محل سکونت",
    )
    full_address = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="ادرس محل سکونت"
    )
    special_user = models.BooleanField(default=False, verbose_name="کاربر ویژه")

    class Meta:
        verbose_name_plural = "کاربر ها"

    def __str__(self):
        return self.user
