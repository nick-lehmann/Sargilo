Resolvers
=========

The task of a resolver is to read in the plain data of an item given in the dataset file and determine the type of data that it describes. Examples for this are:

- Data primitives: Text, Integer, etc.
- Structured data e.g. json
- Files
- Relations (One-to-One, One-to-Many, Many-to-Many)

Because of the last point, it is also the task of a resolver to calculate that data dependencies that the collection has. Take the dataset file of the sample project as an example:

```eval_rst
.. literalinclude:: /../tests/test_project/blog/tests/dataset.yaml
```

Compare the last collection called `posts` to the model `Post`.

```eval_rst
.. literalinclude:: /../tests/test_project/blog/models/post.py
   :language: python
   :linenos:
```
