from plonetheme.classic.browser.interfaces import IThemeSpecific as IClassicTheme
from zope.viewlet.interfaces import IViewletManager


class IThemeSpecific(IClassicTheme):
    """Marker interface that defines a Zope 3 browser layer.
    """

class IPortalLogo(IViewletManager):
    """A viewlet manager that manage the logo in two languages
    """

class IPortalNewPersonal_bar(IViewletManager):
    """ A viewlet manager for the new personal_bar
    """

class IPortalNewFooter(IViewletManager):
    """ A viewlet manager for the new footer
    """

class IPortalNewLanguageSelector(IViewletManager):
    """ A viewlet manager for the new language selector
    """

class IPortalNewSearchbox(IViewletManager):
    """ A viewlet manager for the new searchbox
    """

class IPortalNewBreadcrumb(IViewletManager):
    """A viewlet manager that contains the new breadcrumb
    """