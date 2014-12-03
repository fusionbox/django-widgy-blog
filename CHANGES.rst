CHANGES
=======

0.2.0 (not yet released)
------------------------

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
