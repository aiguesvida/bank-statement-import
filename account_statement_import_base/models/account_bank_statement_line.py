# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    # Ensure transactions can be imported only once
    # if the import format provides unique transaction IDs
    unique_import_id = fields.Char(string="Import ID", copy=False)
    raw_data = fields.Text(copy=False)

    @api.constrains("unique_import_id")
    def _check_unique_import_id(self):
        for rec in self:
            if not rec.unique_import_id:
                continue
            domain = [
                ("unique_import_id", "=", rec.unique_import_id),
                ("id", "!=", rec.id),
            ]
            if self.search_count(domain):
                raise ValidationError(
                    "A bank account transaction can be imported only once!"
                )
