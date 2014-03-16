muto-client
===========

**muto** is a client/server system for cloud-based image manipulation in
[Django] projects. It uses [easy-thumbnails] for the manipulation part and
[boto] for accessing and storing images on [S3].

This is the client part. The server package is called [muto-server].


Installation
------------

You can install the package from PyPI using pip or easy_install:

```bash
$ pip install muto-client
```

Or you can install from the latest source version:

```bash
$ git clone git://github.com/philippbosch/muto-client.git
$ cd muto-client/
$ python setup.py install
```

Add `muto` to your `INSTALLED_APPS` in **settings.py**:

```python
INSTALLED_APPS = (
    # ...
    'muto',
)
```

Create the database tables:

If you use [South]:

```bash
$ python manage.py migrate muto
```

Otherwise:

```bash
$ python manage.py syncdb
```



Configuration
-------------

There are a few configuration settings you can set in your **settings.py**:

* `MUTO_REDIS_URL` – The URL to your [muto-server]'s Redis instance (defaults to `redis://:6379`)
* `MUTO_AWS_STORAGE_BUCKET_NAME` - The S3 bucket used to store and retrieve images (falls back to `AWS_STORAGE_BUCKET_NAME` if not defined)
* `MUTO_AWS_ACCESS_KEY_ID` and `MUTO_AWS_SECRET_ACCESS_KEY` – Your S3 credentials used to upload to S3 (fall back to `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` respectively if not defined)


Usage
-----

Use `MutoField` in your models (in **models.py**):

```python
from django.db import models
from muto.fields import MutoField

class MyModel(models.Model):
    image = MutoField()
```

Register your model with the *muto transformer* (also in **models.py**):

```python
transformer.register(MyModel, 'image')
```

You should see a new section called **Muto** in your *Django Admin*. There you
can create *image version definitions*. The options value should be a
JSON-serialized kwargs dict that will be handed over to [easy-thumbnails]. An
example:

```json
{
    "size": [640,480],
    "quality": 65,
    "bw": true
}
```

Now every time you create a new `MyModel` instance or change one, the muto
server will create image versions of the corresponding image and upload them to
[S3].


License
-------

[MIT]



[Django]: http://www.djangoproject.com/
[easy-thumbnails]: https://github.com/SmileyChris/easy_thumbnails
[boto]: https://github.com/boto/boto
[S3]: https://aws.amazon.com/s3/
[muto-server]: https://github.com/philippbosch/muto-server
[South]: http://south.aeracode.org/
[MIT]: http://philippbosch.mit-license.org/
