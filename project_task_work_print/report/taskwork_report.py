# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
from openerp.report import report_sxw


class TaskWorkReport(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(TaskWorkReport, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
        })
        self.context = context

    def _get_tot_hours(self, ts_lines):
        tot = 0.0
        deduced = 0.0
        for line in ts_lines:
            if line.product_uom_id:
                factor = line.product_uom_id.factor
                if factor == 0.0:
                    factor = 1.0
            else:
                factor = 1.0
            factor_invoicing = 1.0
            if line.to_invoice and line.to_invoice.factor != 0.0:
                factor_invoicing = 1.0 - line.to_invoice.factor / 100
            if factor_invoicing > 1.0:
                deduced += ((line.unit_amount / factor) * factor_invoicing)
                tot += ((line.unit_amount / factor) * factor_invoicing)
            elif factor_invoicing <= 1.0:
                tot += (line.unit_amount / factor)
                deduced += ((line.unit_amount / factor) * factor_invoicing)
        return {'total': tot, 'deduced': deduced}


report_sxw.report_sxw(
    'report.project.task.work', 'project.project',
    'addons/project_task_work_print/report/taskwork_report.rml',
    parser=TaskWorkReport)
