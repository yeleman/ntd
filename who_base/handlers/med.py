#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.utils.translation import ugettext as _

from rapidsms.contrib.auth.decorators import registration_required

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.contrib.handlers.helpers import require_args

from ..utils import check_against_last_report

#todo: do a customRoleHandler that you can inherit from, that register the
# role you want

class MedHandler(KeywordHandler):
    u"""
        EXAMPLE SMS FORMAT: med 3 3 87 76
        3: number of drug dose received for drug 1 of the drug pack
        3: number of drug dose returned for drug 1 of the drug pack
        87: number of drug dose received for drug 2 of the drug pack
        76 : number of drug dose returned for drug 2 of the drug pack
    """

    keyword = "med"

    aliases = (('fr', ("med", )),
               ('en', ("med", "drug")),)


    def help(self, keyword, lang_code):
        return self.respond(_(u"To report, send 'MED', followed by an "\
                              u"even number of values."))


    @registration_required()
    def handle(self, text, keyword, lang_code):

        # todo: factorize this
        args = [self.flatten_string(arg) for arg in text.split()]

        #todo: rename the report model in report manager
        report_manager = check_against_last_report(self.msg.contact)

        # make update the manager date so
        report_manager.save()

        report_was_completed = report_manager.is_completed()

        results = report_manager.results

        drugs_args_count = results.drugs_pack.drugs.count() * 2

        require_args(args, min=drugs_args_count, max=drugs_args_count)

        try:
            args = [int(x) for x in args]
        except ValueError:
            return self.respond(_(u"All %(count)s values must be numbers") % {
                                  'count': drugs_args_count})

        for movement in results.stock_movements.all():
            movement.received = args.pop(0)
            movement.returned = args.pop(0)
            if movement.returned > movement.received:
                return self.respond(_(u'The number of doses returned (%(returned)s) '\
                                      u'for %(drug)s can not be greater than '\
                                      u'the number of doses received (%(received)s).' % {
                                      'returned': movement.returned,
                                      'received': movement.received,
                                      'drug': movement.drug.name
                                      }))

            movement.save()
        # todo : check if all the given pills match the one received and
        # the one returned ?

        results.report_manager.status.drug = True
        results.report_manager.save()
        results.save()

        # todo: prefix successeful messages by 'OK'
        msg = _(u"The stocks for the campaign %(campaign)s in "\
                   u"%(location)s are saved.") % {
                   'campaign': results.campaign, 'location': results.area}

        if not report_was_completed and report_manager.is_completed():
            msg += _(u" All reports for this location are completed!")
        else:
            progress = results.report_manager.progress
            msg += _(u" You have sent %(completed)s over %(to_complete)s "\
                     u"reports for this location.") % {'completed': progress[0],
                                                     'to_complete': progress[1]}

        return self.respond(msg)




