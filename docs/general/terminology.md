General concepts & Terminology
==============================

Because this documentation and the comments in the source code often refer to different types of data, it is necessary to come up with a terminology that lets you easily distinguish between created data on the application side and the data and data containers that Sargilo uses. Please note that the terminologoy of the application side is taken from Django, but can be applied to many other frameworks or ORMs.

```
     Application                            Dataset
     ===========                            =======
     |                                      |
     +> App                                 +> Section
     |  |                                   |  |
     |  +> Model        ---> Object (id)    |  +> Collection   ---> Item (anchor)
     |  |  -> Field     \--> Object (id)    |  |  -> Field     \--> Item (anchor)
     |  |  -> Field                         |  |  -> Field
     |  -> Model        ---> Object (id)    |  -> Collection   ---> Item (anchor)
     |     -> Field     \--> Object (id)    |     -> Field     \--> Item (anchor)
     -> App                                 -> Section
        |                                      |
        -> Model        ---> Object (id)       -> Model        ---> Item (anchor)
           -> Field     \--> Object (id)          -> Field     \--> Item (anchor)
           -> Field                               -> Field
```

## Application side (e.g. Django)

A Django project is composed of several apps, including the ones shipped with the Django installation.
- App
Each app contains a set of Django models. A app is identified by its app label.
- Model
Represents a real world object.
- Model Field
Describes by its name and type. The type is a Django model field (e.g. CharField)
- Object
Created based on models by populating them with data. Identified by their id.

## Sargilo


### Dataset

The term `dataset` describes, well, the entirety of data that makes up your test setup.

```eval_rst
.. autoclass:: sargilo.dataset.Dataset
    :show-inheritance:
```


### Section

Analogous to an app.

Contains a collection for each model in corresponding app.


### Collection

Analogous to a model.

Container for several test items. A collection also saves the mapping between the item anchors
and the object ids.


### Collection field

Analogous to a model field. 


### Item

Analogous to a model instance or any other object.

Analog to this, a test data set is composed of several section, each representing one app. Inside a section,
the user can a collection for each model. A collection is, like a collection, defined by its fields, each with a name
and a value. However, in contrast to the model fields, the type of a collection field is a Python object. How this value
is processed before passed to the model constructor depends on the value of the corresponding model field.




