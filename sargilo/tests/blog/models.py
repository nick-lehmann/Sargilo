from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name


class Critique(models.Model):
    """
    Serves as a One-To-One relation to the post, with a foreign key to User to make
    it more complex.
    """
    content = models.TextField()
    author = models.ForeignKey(
        User,
        verbose_name='author',
        related_name='critiques'
    )


class Post(models.Model):
    """
    Main testing model for Sargilo. It has five different types of relations.
    - One-to-One relation to Critique
    - Incoming foreign key relation with slugs
    - Outgoing foreign key relation with user
    - Normal many-to-many relation with tags
    - Many-to-many relation with Comment as intermediary model with user
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateField()

    author = models.ForeignKey(
        User,
        verbose_name='Author',
        related_name='posts',
        on_delete=models.PROTECT
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='posts',
    )

    comments = models.ManyToManyField(
        User,
        related_name='commented_posts',
        through='Comment'
    )

    critique = models.OneToOneField(
        Critique,
        verbose_name='Critique',
        related_name='post',
        blank=True, null=True
    )

    def __str__(self):
        tag_string = '#' + '#'.join(self.tags.all())
        return "{} {} ({} slugs, {} comments)".format(
            self.title,
            tag_string,
            self.slugs.all().count(),
            self.comments.all().count()
        )


class Slug(models.Model):
    title = models.CharField(max_length=255)
    post = models.ForeignKey(
        Post,
        related_name='slugs'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=500)
    upvotes = models.IntegerField()

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return '"{}" by {}'.format(self.text[:15], self.author)
