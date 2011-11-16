from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from AccessControl import getSecurityManager
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector
from Acquisition import aq_base, aq_inner
from zope.i18nmessageid import MessageFactory

class LogoViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()

        portal = self.portal_state.portal()
        logoName = portal.restrictedTraverse('base_properties').logoName
        self.logo_tag = portal.restrictedTraverse(logoName).tag()

        self.portal_title = self.portal_state.portal_title()

class NewPersonal_bar(ViewletBase):
    index = ViewPageTemplateFile('templates/personal_bar.pt')

    def update(self):
        super(NewPersonal_bar, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')

        sm = getSecurityManager()

        self.user_actions = context_state.actions().get('user', None)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

        self.anonymous = self.portal_state.anonymous()

        if not self.anonymous:

            member = self.portal_state.member()
            userid = member.getId()

            if sm.checkPermission('Portlets: Manage own portlets', self.context):
                self.homelink_url = self.navigation_root_url + '/dashboard'
            else:
                if userid.startswith('http:') or userid.startswith('https:'):
                    self.homelink_url = self.site_url + '/author/?author=' + userid
                else:
                    self.homelink_url = self.site_url + '/author/' + quote_plus(userid)

            member_info = tools.membership().getMemberInfo(member.getId())
            # member_info is None if there's no Plone user object, as when
            # using OpenID.
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid


class NewLanguageSelector(ViewletBase):
    render = ViewPageTemplateFile('templates/languageselector.pt')

    def __init__(self, context, request, view, manager):
        super(ViewletBase, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager

        self.tool = getToolByName(context, 'portal_languages', None)

    def portal_url(self):
        return self.site_url

    def available(self):
        if self.tool is not None:
            # Ask the language tool. Using getattr here for BBB with older
            # versions of the tool.
            showSelector = getattr(aq_base(self.tool), 'showSelector', None)
            if showSelector is not None:
                return self.tool.showSelector() # Call with aq context
            # BBB
            return bool(self.tool.use_cookie_negotiation)
        return False

    def showFlags(self):
        """Do we use flags?."""
        return False

    def languages(self):
        """Returns list of languages."""
        if self.tool is None:
            return []
        bound = self.tool.getLanguageBindings()
        current = bound[0]

        def merge(lang, info):
            info["code"]=lang
            if lang == current:
                info['selected'] = True
            else:
                info['selected'] = False

            return info
        return [merge(lang, info) for (lang,info) in
                    self.tool.getAvailableLanguageInformation().items()
                    if info["selected"]]

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.site_url = self.portal_state.portal_url()
        ls = LanguageSelector(self.context, self.request, self.view, self.manager)
        ls.update()
        results = ls.languages()
        translatable = ITranslatable(self.context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']
            else:
                state = getMultiAdapter((self.context, self.request), name='plone_context_state')
                try:
                    data['url'] = state.view_url() + '?set_language=' + data['code']
                except AttributeError:
                    data['url'] = self.context.absolute_url() + '?set_language=' + data['code']



class NewSearchbox(ViewletBase):
    index = ViewPageTemplateFile('templates/searchbox.pt')

    def update(self):
        super(NewSearchbox, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        props = getToolByName(self.context, 'portal_properties')
        livesearch = props.site_properties.getProperty('enable_livesearch', False)
        if livesearch:
            self.search_input_id = "searchGadget"
        else:
            self.search_input_id = ""

        folder = context_state.folder()
        self.folder_path = '/'.join(folder.getPhysicalPath())


class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/path_bar.pt')

    def update(self):
        super(PathBarViewlet, self).update()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()