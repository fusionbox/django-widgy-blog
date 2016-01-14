Django Widgy Blog
=================

This is reusable blog app designed for use with django-widgy_. It can
be utilized as a drop-in addition to a widgy project for creating a
quick, run-of-the-mill blog or as an abstract guide to building your
own custom app that takes advantage of all the wonderful features that
widgy offers.

Quickstart
----------

(This guide assumes that your project is already using widgy. Please see
this tutorial_ if this is not the case.)

1.  Install the package

        $ pip install django-widgy-blog

2.  Add ``widgy_blog`` to your ``INSTALLED_APPS``.

3.  Run ``python manage.py migrate`` in
    order to generate the relevant models in the database.

4.  Configure the urls:

    a.  If you're using widgy's ``contrib.urlconf_include`` package, you can
        opt to use widgy_blog as a plugin. This allows admin users of the site
        to take advantage of plugin-specific features, such as editing the url
        route of the blog and customizing its addition to menus. See
        urlconf_include_ for more information.

    b.  Alternatively, you can include the widgy_blog urls within your urls.py
        file as you normally would. Just remember to add them before the
        included Mezzanine urls if you're editing the root conf!

5.  That's it. Log in to the admin center and start adding blog posts!

.. _django-widgy: https://github.com/fusionbox/django-widgy
.. _tutorial: http://docs.wid.gy/en/latest/tutorials/widgy-mezzanine-tutorial.html
.. _urlconf_include: http://docs.wid.gy/en/latest/tutorials/widgy-mezzanine-tutorial.html#urlconf-include
