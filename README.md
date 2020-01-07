Sargilo 
=======

Data loader for Humans

Sargilo lets you declare your data in a visually pleasing and non-frustrating way and loads it into your environment of choice. YAML usage, validation and auto-completion help you get boring jobs done.

💡 Motivation
-------------

The idea for this project came from the testing I had to do at work. Surely, you will need sample data to test the project you currently work on. After some time, two ways how to approach this have been emerged:

- Create a minimal and abstract data sample for each test or group of tests and test against those
- Find a more comphrehensive data set that satisfies most of edge cases and only add to it in rare cases

There are of course advantages and disadvantages to both approaches. However, I prefer the second approach and think of it as telling a little story. I prefer this way since the dataset can be used as a fixture when running your application and after working on it for quite some time, you will get a feeling for the result a function should produce, making it easier to spot errors.

📦 Install
----------

```bash
pip install sargilo
```

Or if you prefer an alternative installation method

```bash
poetry add sargilo
pipenv install sargilo
```

🔗 Integrations
---------------

To know how to load your data, `sargilo` has to know how to deal with your framework or ORM of choice. While `sargilo` provides the interface and basic functionaly, the specifics on how to load the data are up to the integration. Currently, the following integrations are supported:

- Django (ORM)

📒 Examples
-----------

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
