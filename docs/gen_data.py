#!/usr/bin/env python
# encoding=utf-8

import random
from datetime import datetime

def gen_data():

    ''' Generates a valid set of data for the NTD2010 Field Test Forms '''

    # set some good faith limits
    POPULATION_LIMITS = (3500, 20000)
    TARGET_PERCENTAGE = (40, 65)
    UNDER6_PERCENTAGE = (3, 9)
    MALE_PERCENTAGE = (45, 52)
    # percentage of 5-15 in target population
    FIVE15_PERCENTAGE = (75, 92)

    # pregnent women
    PREG5_PERCENTAGE = (0, 2)
    PREG15_PERCENTAGE = (2, 8)

    # absence
    ABS5_PERCENTAGE = (1, 5)
    ABS15_PERCENTAGE = (10, 20)

    # refus
    REF5_PERCENTAGE = (0, 2)
    REF15_PERCENTAGE = (1, 10)

    # effets secondaires
    EFF5_PERCENTAGE = (0, 20)
    EFF15_PERCENTAGE = (0, 20)

    # percentages 
    MECT1_U5_PERCENTAGE = (30, 36)
    MECT2_U5_PERCENTAGE = (30, 36)
    MECT3_U5_PERCENTAGE = (30, 36)
    MECT4_U5_PERCENTAGE = (30, 36)

    MECT1_15_PERCENTAGE = (0,2)
    MECT2_15_PERCENTAGE = (0,10)
    MECT3_15_PERCENTAGE = (10, 20)
    MECT4_15_PERCENTAGE = (70, 90)

    MED_OVERHEAD_PERCENTAGE = (10, 30)
    MED_LOST_PERCENTAGE = (1, 30)


    # generate population
    # get a random number inside limits
    total_population = random.randint(*POPULATION_LIMITS)

    # target population is part of total
    # get random percentage inside percentage limts
    target_population = (total_population * random.randint(*TARGET_PERCENTAGE)) / 100

    # under 6 treated
    # this one is not related and should be faily small
    under6_treated = (total_population * random.randint(*UNDER6_PERCENTAGE)) / 100

    # gender break down
    men = (target_population * random.randint(*MALE_PERCENTAGE)) / 100
    women = target_population - men

    # age break downs
    men_5 = (men * random.randint(*FIVE15_PERCENTAGE)) / 100
    men_15 = men - men_5

    women_5 = (women * random.randint(*FIVE15_PERCENTAGE)) / 100
    women_15 = women - women_5

    # setup some containers to help pop people out
    men5_remain = men_5
    men15_remain = men_15
    women5_remain = women_5
    women15_remain = women_15

    # special cases
    # all part of target_population
    # only secondary effects have been treated.

    # pregnant women
    cpf_enc5 = (women5_remain * random.randint(*PREG5_PERCENTAGE)) /100
    cpf_enc15 = (women5_remain * random.randint(*PREG15_PERCENTAGE)) /100
    women5_remain -= cpf_enc5
    women5_remain -= cpf_enc15

    # person not present
    cph_abs5 = (men5_remain * random.randint(*ABS5_PERCENTAGE)) /100
    cph_abs15 = (men5_remain * random.randint(*ABS15_PERCENTAGE)) /100
    men5_remain -= cph_abs5
    men5_remain -= cph_abs15

    cpf_abs5 = (women5_remain * random.randint(*ABS5_PERCENTAGE)) /100
    cpf_abs15 = (women5_remain * random.randint(*ABS15_PERCENTAGE)) /100
    women5_remain -= cpf_abs5
    women5_remain -= cpf_abs15

    # person refusing medecine
    cph_ref5 = (men5_remain * random.randint(*REF5_PERCENTAGE)) /100
    cph_ref15 = (men5_remain * random.randint(*REF15_PERCENTAGE)) /100
    men5_remain -= cph_ref5
    men5_remain -= cph_ref15

    cpf_ref5 = (women5_remain * random.randint(*REF5_PERCENTAGE)) /100
    cpf_ref15 = (women5_remain * random.randint(*REF15_PERCENTAGE)) /100
    women5_remain -= cpf_ref5
    women5_remain -= cpf_ref15

    # EFFETS SECONDAIRES BELOW

    # 1 mectizan - kids under 119cm
    # should target mostly 5-7yo.
    # assuming loosely that women have same age/height as men.
    h1_5 = (men5_remain * random.randint(*MECT1_U5_PERCENTAGE)) /100
    men5_remain -= h1_5
    h1_15 = (men5_remain * random.randint(*MECT1_15_PERCENTAGE)) /100
    men15_remain -= h1_15

    f1_5 = (women5_remain * random.randint(*MECT1_U5_PERCENTAGE)) /100
    women5_remain -= f1_5
    f1_15 = (women5_remain * random.randint(*MECT1_15_PERCENTAGE)) /100
    women15_remain -= f1_15

    # 2 mectizan - kids between 120 - 140cm
    # should target mostly 5-7yo.
    # assuming loosely that women have same age/height as men.
    h2_5 = (men5_remain * random.randint(*MECT2_U5_PERCENTAGE)) /100
    men5_remain -= h2_5
    h2_15 = (men5_remain * random.randint(*MECT2_15_PERCENTAGE)) /100
    men15_remain -= h2_15

    f2_5 = (women5_remain * random.randint(*MECT2_U5_PERCENTAGE)) /100
    women5_remain -= f2_5
    f2_15 = (women5_remain * random.randint(*MECT2_15_PERCENTAGE)) /100
    women15_remain -= f2_15

    # 3 mectizan - kids between 141 - 158cm
    # should target mostly 5-7yo.
    # assuming loosely that women have same age/height as men.
    h3_5 = (men5_remain * random.randint(*MECT3_U5_PERCENTAGE)) /100
    men5_remain -= h3_5
    h3_15 = (men5_remain * random.randint(*MECT3_15_PERCENTAGE)) /100
    men15_remain -= h3_15

    f3_5 = (women5_remain * random.randint(*MECT3_U5_PERCENTAGE)) /100
    women5_remain -= f3_5
    f3_15 = (women5_remain * random.randint(*MECT3_15_PERCENTAGE)) /100
    women15_remain -= f3_15

    # 4 mectizan - kids over 159cm
    # should target mostly 5-7yo.
    # assuming loosely that women have same age/height as men.
    h4_5 = (men5_remain * random.randint(*MECT4_U5_PERCENTAGE)) /100
    men5_remain -= h4_5
    h4_15 = (men5_remain * random.randint(*MECT4_15_PERCENTAGE)) /100
    men15_remain -= h4_15

    f4_5 = (women5_remain * random.randint(*MECT4_U5_PERCENTAGE)) /100
    women5_remain -= f4_5
    f4_15 = (women5_remain * random.randint(*MECT4_15_PERCENTAGE)) /100
    women15_remain -= f4_15

    # equaly share remaining people.
    def equalize(remain, v1, v2, v3, v4, default):

        #print "equalizing: %d - %d %d %d %d" % (remain, v1, v2, v3, v4)
        split = remain / 4
        extra = remain % 4
        if remain < 0:
            split = -split
        #print "split: %d, extra: %d" % (split, extra)
        v1 += split
        v2 += split
        v3 += split
        v4 += split
        remain = 0
        #print "equalized: %d - %d %d %d %d" % (remain, v1, v2, v3, v4)

    equalize(men5_remain, h1_5, h2_5, h3_5, h4_5, h1_5)
    equalize(men15_remain, h1_15, h2_15, h3_15, h4_15, h4_15)
    equalize(women5_remain, f1_5, f2_5, f3_5, f4_5, f1_5)
    equalize(women15_remain, f1_15, f2_15, f3_15, f4_15, f4_15)

    extra = None

    # effets secondaires
    men5_treated = h1_5 + h2_5 + h3_5 + h4_5
    men15_treated = h1_15 + h2_15 + h3_15 + h4_15
    cph_eff5 = (men5_treated * random.randint(*EFF5_PERCENTAGE)) /100
    cph_eff15 = (men15_treated * random.randint(*EFF15_PERCENTAGE)) /100

    women5_treated = f1_5 + f2_5 + f3_5 + f4_5
    women15_treated = f1_15 + f2_15 + f3_15 + f4_15
    cpf_eff5 = (women5_treated * random.randint(*EFF5_PERCENTAGE)) /100
    cpf_eff15 = (women15_treated * random.randint(*EFF15_PERCENTAGE)) /100

    # stocks
    # pick a received number higher than used and generate some returned
    alben_used = men5_treated + men15_treated + women5_treated + women15_treated
    st_alb_rec = int(round(alben_used + (alben_used * random.randint(*MED_OVERHEAD_PERCENTAGE)) / 100, -2))
    alben_remain = st_alb_rec - alben_used
    alben_lost = (alben_remain * random.randint(*MED_LOST_PERCENTAGE)) / 100
    st_alb_rend = alben_remain - alben_lost

    mec_used = h1_5 + h1_15 + f1_5 + f1_5 + 2 * (h2_5 + h2_15 + f2_5 + f2_15) + 3 * (h3_5 + h3_15 + f3_5 +f3_15) + 4 * (h4_5 + h4_15 + f4_5 + f4_15)
    st_mec_rec = int(round(mec_used + (mec_used * random.randint(*MED_OVERHEAD_PERCENTAGE)) / 100, -2))
    mec_remain = st_mec_rec - mec_used
    mec_lost = (mec_remain * random.randint(*MED_LOST_PERCENTAGE)) / 100
    st_mec_rend = mec_remain - mec_lost

    return locals()

def genpdf(name, code, sample, parent=u""):

    from datetime import datetime, timedelta
    from subprocess import Popen, PIPE
    from cStringIO import StringIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from reportlab.lib.pagesizes import landscape,A4,letter,portrait


    # Static source pdf to be overlayed
    PDF_SOURCE = 'tally_empty.pdf'

    DATE_FORMAT = u"%d/%m/%Y"

    DEFAULT_FONT_SIZE = 11
    FONT = 'Courier-Bold'

    # A simple function to return a leading 0 on any single digit int.
    def double_zero(value):
        try:
            return '%02d' % value
        except TypeError:
            return value

    # temporary file-like object in which to build the pdf containing
    # only the data numbers
    buffer = StringIO()

    # setup the empty canvas
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    c.setFont(FONT, DEFAULT_FONT_SIZE)


    # REPORT HEADER AND FOOTER
    def report_header_footer():

        # The y coordinates for each line of fields on the form
        header_line_y = 15.65 * cm
        footer_line_y = 1.65 * cm

        # A list containing dictionaries of each field in the header and footer
        # Each item in the list is a dictionary with the x and y coords and
        # the value of the data
        data = [
                # Village
                {"x": 19.5 * cm, "y": header_line_y,
                 "value": name},
                # Commune
                {"x": 5.4 * cm, "y": header_line_y,
                 "value": parent},
                # Distributor
                {"x": 9.8 * cm, "y": footer_line_y,
                 "value": u""},
                ]
        '''# Dates
            {"x": 23.8 * cm, "y": footer_line_y,
             "value": datetime.today().strftime(DATE_FORMAT)},'''

        # draw the data onto the pdf overlay
        for field in data:
            if 'size' in field:
                c.setFont(FONT, field['size'])
            c.drawString(field['x'], field['y'],
                         unicode(double_zero(field['value'])))
            if 'size' in field:
                c.setFont(FONT, DEFAULT_FONT_SIZE)


    # REPORT HEADER AND FOOTER
    def report_data(line, values):

        # The y coordinates for each line of fields on the form
        lines_y = {
            1: 12.90 * cm,
            2: 12.35 * cm,
            3: 11.7 * cm,
            4: 11.0 * cm,
            5: 6.05 * cm,
            6: 5.05 * cm,
            7: 4.05 * cm,
            8: 3.05 * cm,
            9: 9.7 * cm,
            10: 8.6 * cm,
            }
        columns_x = {
            1: 8.0 * cm,
            2: 12.2 * cm,
            3: 16.9 * cm,
            4: 21.1 * cm,
            5: 24.66 * cm,
            6: 26.87 * cm,
        }

        columns2_x = {
            1: 6.5 * cm,
            2: 12.6 * cm,
            3: 18.7 * cm,
            4: 25.0 * cm,
        }

        col = columns_x if line < 9 else columns2_x

        # draw the data onto the pdf overlay
        for index in range(0, 6):
            try:
                c.drawString(col[index + 1], lines_y[line],
                             unicode(double_zero(values[index])))
            except (IndexError, KeyError):
                continue

    # display header/footer
    report_header_footer()
    
    report_data(1, [sample['h1_5'], sample['h1_15'], sample['f1_5'], sample['f1_15']])
    report_data(2, [sample['h2_5'], sample['h2_15'], sample['f2_5'], sample['f2_15']])
    report_data(3, [sample['h3_5'], sample['h3_15'], sample['f3_5'], sample['f3_15']])
    report_data(4, [sample['h4_5'], sample['h4_15'], sample['f4_5'], sample['f4_15']])

    report_data(5, ['', '', sample['cpf_enc5'], sample['cpf_enc15']])
    report_data(6, [sample['cph_abs5'], sample['cph_abs15'], sample['cpf_abs5'], sample['cpf_abs15']])
    report_data(7, [sample['cph_ref5'], sample['cph_ref15'], sample['cpf_ref5'], sample['cpf_ref15']])
    report_data(8, [sample['cph_eff5'], sample['cph_eff15'], sample['cpf_eff5'], sample['cpf_eff15']])

    report_data(9, [sample['total_population'], sample['target_population'], sample['under6_treated']])
    report_data(10, [sample['st_alb_rec'], sample['st_alb_rend'], sample['st_mec_rec'], sample['st_mec_rend']])

    # render and save the pdf overlay to the buffer
    c.showPage()
    c.save()

    # use pdftk to 'stamp' the canvas data containing the data
    # onto the pdf_source.
    cmd = '/usr/bin/pdftk %s stamp - output -' % PDF_SOURCE
    proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    pdf, cmderr = proc.communicate(buffer.getvalue())

    # We don't need the buffer anymore because the two pdfs have been
    # combined in the string variable pdf
    buffer.close()

    # name the pdf the receipt code, but get rid of the / as those
    # shouldn't be in filenames.
    filename = "gen_%s.pdf" % code

    fp = open(filename, "w")
    fp.write(pdf)
    fp.close

    return filename

def gen_sms(code, sample, ds, dd):

    vil = u"VIL %(code)s %(ds)s %(de)s %(pop)d %(target)d %(u6)d" % { \
        'code': code,
        'ds': ds.strftime(u"%d%m"), \
        'de': ds.strftime(u"%d%m"), \
        'pop': sample['total_population'], \
        'target': sample['target_population'], \
        'u6': sample['under6_treated'],
        }

    hom = u"HOM %(h1_5)d %(h1_15)d %(h2_5)d %(h2_15)d %(h3_5)d %(h3_15)d %(h4_5)d %(h4_15)d" % { \
            'h1_5': sample['h1_5'], \
            'h1_15': sample['h1_15'], \
            'h2_5': sample['h2_5'], \
            'h2_15': sample['h2_15'], \
            'h3_5': sample['h3_5'], \
            'h3_15': sample['h3_15'], \
            'h4_5': sample['h4_5'], \
            'h4_15': sample['h4_15'], \
        }

    fem = u"FEM %(f1_5)d %(f1_15)d %(f2_5)d %(f2_15)d %(f3_5)d %(f3_15)d %(f4_5)d %(f4_15)d" % { \
            'f1_5': sample['f1_5'], \
            'f1_15': sample['f1_15'], \
            'f2_5': sample['f2_5'], \
            'f2_15': sample['f2_15'], \
            'f3_5': sample['f3_5'], \
            'f3_15': sample['f3_15'], \
            'f4_5': sample['f4_5'], \
            'f4_15': sample['f4_15'], \
        }

    cph = u"CPH %(cph_abs5)d %(cph_abs15)d %(cph_ref5)d %(cph_ref15)d %(cph_eff5)d %(cph_eff15)d" % { \
            'cph_abs5': sample['cph_abs5'], \
            'cph_abs15': sample['cph_abs15'], \
            'cph_ref5': sample['cph_ref5'], \
            'cph_ref15': sample['cph_ref15'], \
            'cph_eff5': sample['cph_eff5'], \
            'cph_eff15': sample['cph_eff15'], \
        }

    cpf = u"CPH %(cpf_abs5)d %(cpf_abs15)d %(cpf_ref5)d %(cpf_ref15)d %(cpf_eff5)d %(cpf_eff15)d %(cpf_enc5)d %(cpf_enc15)d" % { \
            'cpf_abs5': sample['cpf_abs5'], \
            'cpf_abs15': sample['cpf_abs15'], \
            'cpf_ref5': sample['cpf_ref5'], \
            'cpf_ref15': sample['cpf_ref15'], \
            'cpf_eff5': sample['cpf_eff5'], \
            'cpf_eff15': sample['cpf_eff15'], \
            'cpf_enc5': sample['cpf_enc5'], \
            'cpf_enc15': sample['cpf_enc15'], \
        }

    med = u"MED %(alb_rec)d %(alb_rend)d %(mec_rec)d %(mec_rend)d" % { \
        'alb_rec': sample['st_alb_rec'], \
        'alb_rend': sample['st_alb_rend'], \
        'mec_rec': sample['st_mec_rec'], \
        'mec_rend': sample['st_mec_rend'], \
        }

    return (vil, hom, fem, cph, cpf, med)

def gen_demo_set(campaign_id):

    import os
    import commands
    from who_base.models import Results, Campaign

    campaign=Campaign.objects.get(id=campaign_id)
    results = Results\
             .objects\
             .filter(campaign=campaign)\
             .select_related('area__as_data_source__data_collection__parent')\
             .order_by('area__as_data_source__data_collection__parent',
                       'area__as_data_source__data_collection',
                       'area')
    
    files = []
    for result in results:
        print "Generating %s, %s" % (result.area, result.area.parent)
        data = gen_data()
        files.append(genpdf(result.area.name, result.area.code, data, result.area.parent.name))

    output_file = 'all_sheets.pdf'
    cmd = '/usr/bin/pdftk %s output %s' % (" ".join(files), output_file)
    status, output = commands.getstatusoutput(cmd)

    for f in files:
        os.remove(f)

    return output_file

def main():

    # generate a set of data
    sample = gen_data()

    # display sample data
    import pprint
    #pprint.pprint(sample)

    # Generate an SMS report from the sample data
    smses = gen_sms("A1560", sample, datetime.now(), datetime.now())
    for sms in smses:
        print sms

    # generate a PDF from the sample data
    genpdf("New York City", "nyc", sample, parent="NY")

if __name__ == '__main__':
    main()
