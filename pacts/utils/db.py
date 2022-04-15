from tortoise import fields
from tortoise.models import Model


class Tag(Model):
    id = fields.BigIntField(pk=True)
    guild_id = fields.TextField()
    author_id = fields.TextField()
    tag_name = fields.TextField()
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tags"
        unique_together = ("tag_name", "guild_id")

    def __str__(self):
        return self.tag_name
