CHANGES
=======

0.2.3 (2019-07-15)
------------------

- Blog views with pagination will now calculate appropriate `rel=prev`
  and `rel=next` links.
- Added Django 1.10 support.


0.2.2 (2016-02-08)
------------------

- Fix subclassing view name bug


0.2.1 (2016-01-14)
------------------

- Fix PyPI bug


0.2.0 (2016-01-14)
------------------

- Support for Django 1.8
- Blog archives are now shown in reverse chronological order.
- Blogs now have date and time rather than just date published.
- Tags are now supported
- Various small bugfixes.
- Blog views with a page querystring equal to 1 will now have a canonical_url
  in the template context pointing to the same page without that querystring.

0.1.0 (release 2014-12-03)
--------------------------

- Add model attributes to AbstractBlogLayout and BlogAdmin
  that make them easier to subclass. Update AbstractBlogLayout
  published queryset function to use fewer queries [Scott Clark, #18]
- **Backwards Incompatible:** Registered the ``BlogLayout`` model with widgy.
  If you weren't using this as your Blog layout, you will need to unregister
  it::

      import widgy
      from widgy_blog.models import BlogLayout

      widgy.unregister(BlogLayout)

  If you were already registering the ``BlogLayout`` yourself, you can just
  remove that code.
