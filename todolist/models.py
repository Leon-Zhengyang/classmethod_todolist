from django.db import models

# todo table
class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("タイトル", max_length=50)
    content = models.TextField(
        "内容",
        blank=True,
        null=True,
        max_length=255,
    )
    deleted = models.IntegerField(
        choices=(
            (0, "ACTIVE"),
            (1, "INACTIVE"),
        ),
        default=0,
    )