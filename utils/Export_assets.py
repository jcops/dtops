import xlwt
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtops.settings")# project_name 项目名称
django.setup()
from io import StringIO
from django.http import HttpResponse
from asset.models import Asset
def write_excel():
    row = 1
    style_heading  = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour ocean_blue;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    style_body = xlwt.easyxf("""
            font:
                name Arial,
                bold off,
                height 0XA0;
            align:
                wrap on,
                vert center,
                horiz left;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """)
    fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
    ]

    style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
    style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    style_body.num_format_str = fmts[0]
    ass_all =Asset.objects.all()
    f = xlwt.Workbook()  # 创建工作簿
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    #sheet1.write(0, 1, label='内网ip', style_heading)
    sheet1.write(0, 0, '主机名', style_heading)
    sheet1.write(0, 1, '内网ip', style_heading)
    sheet1.write(0, 2, '外网ip', style_heading)
    sheet1.write(0, 3, '端口', style_heading)
    sheet1.write(0, 4, '总内存', style_heading)
    sheet1.write(0, 5, '总磁盘', style_heading)
    sheet1.write(0, 6, 'CPU型号', style_heading)
    sheet1.write(0, 7, 'CPU核数', style_heading)
    sheet1.write(0, 8, '系统版本', style_heading)
    sheet1.write(0, 9, '系统发行版本', style_heading)
    sheet1.write(0, 10, 'DNS', style_heading)
    sheet1.write(0, 11, 'MAC地址', style_heading)
    sheet1.write(0, 12, '内核版本', style_heading)
    sheet1.write(0, 13, '序列号', style_heading)
    sheet1.write(0, 14, '虚拟化', style_heading)
    sheet1.write(0, 15, '状态', style_heading)
    sheet1.write(0, 16, '系统用户', style_heading)
    sheet1.write(0, 17, '产品线', style_heading)
    sheet1.write(0, 18, '标签', style_heading)
    sheet1.write(0, 19, '云平台', style_heading)
    sheet1.write(0, 20, '创建用户', style_heading)
    sheet1.write(0, 21, '备注', style_heading)
    sheet1.write(0, 22, '创建时间', style_heading)
    sheet1.write(0, 23, '更新时间', style_heading)
    for ass in ass_all:
        sheet1.write(row, 0, ass.hostname)
        sheet1.write(row, 1, ass.inner_ip)
        sheet1.write(row, 2, ass.pub_ip)
        sheet1.write(row, 3, ass.port)
        sheet1.write(row, 4, ass.mem_total)
        sheet1.write(row, 5, ass.disk_total)
        sheet1.write(row, 6, ass.cpu_model)
        sheet1.write(row, 7, ass.num_cpus)
        sheet1.write(row, 8, ass.osfinger)
        sheet1.write(row, 9, ass.osrelease)
        sheet1.write(row, 10, ass.dns)
        sheet1.write(row, 11, ass.mac_addr)
        sheet1.write(row, 12, ass.kernelrelease)
        sheet1.write(row, 13, ass.serialnumber)
        sheet1.write(row, 14, ass.virtual)
        sheet1.write(row, 15, ass.status)
        sheet1.write(row, 16, ass.system_user.name +'--'+ ass.system_user.username)
        sheet1.write(row, 17, ass.product.name)
        for tags in ass.tag.all():
            sheet1.write(row, 18, tags.name)
        sheet1.write(row, 19, ass.cloud_platform.cloud)
        sheet1.write(row, 20, ass.create_user)
        sheet1.write(row, 21, ass.detail)
        sheet1.write(row, 22, str(ass.create_time),style_body)
        sheet1.write(row, 23, str(ass.update_time),style_body)

        row += 1




    # sio = StringIO()
    #
    # f.save(sio)
    # sio.seek(0)
    # response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment;filename=demo1.xls'
    # response.write(sio.getvalue())
    # return response

    # response = f.save('demo1.xls')  # 保存文件
    # return  response

# a = write_excel()

import  xlrd
#打开表格
def exmysql():
    data = xlrd.open_workbook('asset.xls')
    #获取工作表sheet1
    table = data.sheet_by_name('sheet1')
    #获取行数和列数
    nrows,ncols = table.nrows,table.ncols
    #
    colnames = table.row_values(0)
    w = []
    # print(nrows,ncols)
    # lists = []
    # for i in range(1,nrows):
    #     print(i)
    #     row = table.row_values(i)
    #     if row:
    #         app = {}
    #         for ii in range(len(n)):
    #             app[n[ii]] = row[ii]
    #         lists.append(app)
    # print(lists)
    for i in range(1,nrows):
        #获取每行的值
        row = table.row_values(i)
        print()
        for j in range(0,ncols):#
            if type(row[j]) == float:
                row[j] = int(row[j])
        if row:
            if Asset.objects.filter(hostname = row[0],inner_ip=row[1],pub_ip=row[2]).exists():
                pass
            else:
                w.append(Asset(hostname=row[0],inner_ip=row[1],pub_ip=row[2],port=row[3],mem_total=row[4],disk_total=row[5],cpu_model=row[6],num_cpus=row[7],osfinger=row[8],osrelease=row[9],
                               dns=row[10],mac_addr=row[11],kernelrelease=row[12],serialnumber=row[13],virtual=row[14],status=row[15],detail=row[16]))

    Asset.objects.bulk_create(w)


#system_user=row[17],product=row[18],tag=row[19],cloud_platform=row[20],create_user=row[21]