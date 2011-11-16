from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class PlonethemeAcmolenbeek(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import plonetheme.acmolenbeek
        xmlconfig.file('configure.zcml',
                       plonetheme.acmolenbeek,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetheme.acmolenbeek:default')

PLONETHEME_ACMOLENBEEK_FIXTURE = PlonethemeAcmolenbeek()
PLONETHEME_ACMOLENBEEK_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(PLONETHEME_ACMOLENBEEK_FIXTURE, ),
                       name="PlonethemeAcmolenbeek:Integration")