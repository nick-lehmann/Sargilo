## Assets

In your test data, you can link to assets very quickly. The asset data can of course be configured and will typically be something like `tests/assets/`. Assets can be anything you like, e.g.:

- Samples for more complex model fields like `TextField` and `JsonField`
- Images, videos or other documents 
- Input and Output for your API

Sargilo distinguishes between three types of assets, which are differently treated:

### Normal assets

Normal assets are files which are read from the disk and are automatically decoded. You use a normal asset if you expected to have the "normal" content in your test. Samples for this type of assets are txt files, whose contents should be stored in a `TextField`. Those assets are loaded via `open(file, 'r')`.

### Binary assets

Binary assets are, well, binary files which you want to load. Samples for this are pdf, doc or image files. You typically want to do this if you want to compare the content of this asset to the output of some function which will return binary data. Those assets are loaded via `open(file, 'rb')`.

### Data assets / Loaded assets

Data assets are files which contain structured data that can be easily converted to python data structures. The most important examples for this are `json`, `yaml` and `toml` files, but also other formats like `csv` are supported. If you request a data asset in your test, you will receive a Python data structure e.g. a `dict` or a `list`.