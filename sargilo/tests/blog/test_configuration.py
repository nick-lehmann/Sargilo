import os

from django.contrib.auth.models import User

from sargilo.collection import CollectionConfig
from .models import Post, Comment, Tag, Slug


# default creation method
def dcm(model):
    return model.objects.create


def user_create_function(model):
    def create_new_user(**kwargs):
        user = model.objects.create_user(  # type: User
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            password=kwargs.get('password')
        )
        user.first_name = kwargs.get('first_name', '')
        user.last_name = kwargs.get('last_name', '')

        if kwargs.get('is_staff'):
            user.is_staff = True

        if kwargs.get('is_superuser'):
            user.is_staff = True
            user.is_superuser = True

        user.is_active = kwargs.get('is_active', True)

        user.save()
        return user
    return create_new_user


test_configuration = {
    'Posts': CollectionConfig(
        model=Post,
        creation_function=dcm
    ),
    'Comments': CollectionConfig(
        model=Comment,
        creation_function=dcm
    ),
    'Tags': CollectionConfig(
        model=Tag,
        creation_function=dcm
    ),
    'Users': CollectionConfig(
        model=User,
        creation_function=user_create_function
    ),
    'Slugs': CollectionConfig(
        model=Slug,
        creation_function=dcm
    ),
    'Comments': CollectionConfig(
        model=Comment,
        creation_function=dcm
    )
}

current_dir = os.path.dirname(__file__)
dataset_path = os.path.join(current_dir, 'dataset.yaml')
