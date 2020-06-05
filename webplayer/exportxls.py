import xlwt
from django.http import HttpResponse
from django.utils.translation import gettext as _
from xlwt.compat import xrange


def export_xls(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Radyo Dinleyiciler.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tümü')

    row_num = 0

    columns = [
        (u"İsim", 2000),
        (u"Grup", 2000),
        (u"IP Adresi", 6000),
        (u"Tarayıcı", 8000),
        (u"Zaman", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        row_num += 1
        row = [
            # obj.pk,
            obj.name,
            obj.organization,
            obj.ip,
            obj.browser,
            str(obj.updated),
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


export_xls.short_description = _('Export to Excel')
