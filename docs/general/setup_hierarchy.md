# Setup hierarchy

Another important feature is the setup hierarchy. Because some collections can grow quite big and therefore creating all records of your dataset is not wise, especially if the actual test does not need all entries. To avoid completely recreating the dataset before every test run, Sargilo can determine the hierarchy of your dataset, meaning it knows "which collection needs another collection to be created first". Let's have a look at the following example with Django.

```python
# models.py
from django import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    tag = models.ForeignKey(
        Tag,
        verbose_name='Tag',
        related_name='posts',
        on_delete=models.PROTECT
    )

    author = models.ForeignKey(
        User,
        verbose_name='Author',
        related_name='posts',
        on_delete=models.PROTECT
    )
```

```yaml
# dataset.yaml
auth:
  users:
    - &Admin
      username:     "Admin"
      first_name:   "Christoph"
      last_name:    "Smaul"
      email:        "christoph@mail.de"
      password:     "very_secret"
      is_staff:      True
      is_superuser:  True
    - &Editor
      username:     "Editor"
      first_name:   "Wendy"
      last_name:    "Lator"
      email:        "wendy@mail.de"
      password:     "very_secret"
      is_staff:      True
      is_superuser:  False


blog:
  tags:
    - &TestTag
      name: "Test"
    - &BlueTag
      name: "Blue"
  posts:
    - title: "Hello world"
      text: "Lorem ipsum dolor amet sunt"
      tag: *TestTag
      author: *Admin

    - title: "Just a test"
      text: "This is just a test. This is just a test. This is just a test."
      tag: *TestTag
      author: *Editor
```