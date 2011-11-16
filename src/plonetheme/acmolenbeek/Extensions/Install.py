from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple

def install(self, reinstall=False):
    tool=getToolByName(self, "portal_setup")

    if getFSVersionTuple()[0]>=3:
        tool.runAllImportStepsFromProfile(
                "profile-plonetheme.acmolenbeek:default",
                purge_old=False)
    else:
        plone_base_profileid = "profile-CMFPlone:plone"
        tool.setImportContext(plone_base_profileid)
        tool.setImportContext("profile-plonetheme.acmolenbeek:default")
        tool.runAllImportSteps(purge_old=False)
        tool.setImportContext(plone_base_profileid)

    return "Ran all import steps for profile-plonetheme.acmolenbeek:default."

def uninstall(self):
    tool=getToolByName(self, "portal_setup")

    if getFSVersionTuple()[0]>=3:
        tool.runAllImportStepsFromProfile(
                "profile-plonetheme.acmolenbeek:uninstall",
                purge_old=False)
    else:
        plone_base_profileid = "profile-CMFPlone:plone"
        tool.setImportContext(plone_base_profileid)
        tool.setImportContext("profile-plonetheme.acmolenbeek:uninstall")
        tool.runAllImportSteps(purge_old=False)
        tool.setImportContext(plone_base_profileid)

    # Set Plone Default as default skin
    portal_skins = getToolByName(self, 'portal_skins')
    portal_skins.default_skin = "Sunburst Theme"


    return "Ran all import steps for profile-plonetheme.acmolenbeek:uninstall."

