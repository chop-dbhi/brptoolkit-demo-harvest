from django.core.urlresolvers import reverse
from avocado.formatters import registry
from serrano.formatters import HTMLFormatter
from brp_demo.models import *
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import logging

log = logging.getLogger(__name__)

class cBioLinkFormatter(HTMLFormatter):
    def to_html(self, value, **context):
	# http://reslnbrp_demobio01.research.chop.edu:8080/cbioportal/case.do?cancer_study_id=cranio_resnicklab_2013&case_id=7316_100
	from .models import NautilusSubject, PortalSubject
	sub = PortalSubject.objects.get(pk=value)
	sdgs = sub.nautilussubject_set.all()
	html = '<ul>'
	for sdg in sdgs:
	    html += '<em>{0}</em>'.format(sdg.sample_subject_id)
	    if hasattr(sdg, 'cbiosample'):
		html += '<li><a href="{0}case.do?cancer_study_id={1}&case_id={2}" target="_blank">View in cBio</a></li>'.format(settings.CBIO_HOST, sdg.cbiosample.cancer_study_identifier, sdg.cbiosample.stable_id)
	    else:
		html += '<li>Not Available</li>'
	return html

class SpecimenLocationFormatter(HTMLFormatter):
    def to_html(self, values, **context):
        from avocado.models import DataField
        plate_locations = ['plate_order', 'plate_column', 'plate_row']

        html_str = ""
        for name in plate_locations:
            if values[name] is not None:
                data_field = DataField.objects.get_by_natural_key('brp_demo', 'specimen', name)
                html_str += "<tr><td>{0}</td><td>{1}</td></tr>".format(data_field, values[name])
        if html_str != "":
            return "<table class='table table-striped table-condensed'>{0}</table>".format(html_str)
        return ""

    to_html.process_multiple = True


class PatientSummaryFormatter(HTMLFormatter):
    def to_html(self, value, **context):
        url = reverse('patient-detail', kwargs={'pk': value})
        return '<a href="{0}">View Summary</a>'.format(url)

    def to_csv(self, value, **context):
        return ''


class PathologyReportFormatter(HTMLFormatter):
    def to_html(self, value, **context):
        from .models import NautilusSubject, PortalSubject

        try:
            sub = PortalSubject.objects.get(ehb_id=value)
            sdgs = sub.nautilussubject_set.all()
        except:
            return '<em>Not Available</em>'


        html = '<ul>'

        for sdg in sdgs:
            html += '<em>{0}</em>'.format(sdg.sample_subject_id)
            if not sdg.pathreport_set.all():
                html+= '<li><em>Not Available</em></li>'

            for each in sdg.pathreport_set.all():
                html += '<li><a href="{0}">Pathology Report</a></li>'.format(each.path_url)

        html += '</ul>'

        return html

    def to_csv(self, value, **context):
        from .models import NautilusSubject
        try:
            sub = NautilusSubject.objects.get(sample_subject_id=value)
        except:
            return ''

        if not sub.pathreport_set.all():
            return ''

        csv_ = ''

        for each in sub.pathreport_set.all():
            csv_ += '{0},'.format(each.path_url)
        csv_.rstrip(',')

        return csv_


class OperativeReportFormatter(HTMLFormatter):
    def to_html(self, value, **context):
	from .models import NautilusSubject, PortalSubject

	try:
	    sub = PortalSubject.objects.get(ehb_id=value)
	    sdgs = sub.nautilussubject_set.all()
	except:
	    return '<em>Not Available</em>'


	html = '<ul>'

	for sdg in sdgs:
	    html += '<em>{0}</em>'.format(sdg.sample_subject_id)
	    if not sdg.operativereport_set.all():
		html+= '<li><em>Not Available</em></li>'

	    for each in sdg.operativereport_set.all():
		html += '<li><a href="{0}">Operative Report</a></li>'.format(each.op_url)

	html += '</ul>'

	return html

    def to_csv(self, value, **context):
	from .models import NautilusSubject
	try:
	    sub = NautilusSubject.objects.get(sample_subject_id=value)
	except:
	    return ''

	if not sub.operativereport_set.all():
	    return ''

	csv_ = ''

	for each in sub.operativereport_set.all():
	    csv_ += '{0},'.format(each.op_url)
	csv_.rstrip(',')

	return csv_


class EnrollmentTypeFormatter(HTMLFormatter):
    def to_html(self, value, **context):
        from .models import PortalSubject

        try:
            sub = PortalSubject.objects.get(ehb_id=value)
            diags = sub.diagnosis_set.all()
        except:
            return '<em>Not Available</em>'

        count = 1

        for diag in diags:
            html = '<ul>'
            if diag.diagnosis_type:
                html += '<em>{0}</em>'.format(diag.diagnosis_type)
            else:
                html += '<em>Diagnosis {0}</em>'.format(count)

            if not diag.enrollment_type:
                html += '<li><em>Unknown</em></li>'
            else:
                html += '<li>{0}</li>'.format(diag.enrollment_type)

            html += '</ul>'

            count += 1

        return html

    def to_csv(self, value, **context):
        try:
            sub = PortalSubject.objects.get(ehb_id=value)
            diags = sub.diagnosis_set.all()
        except:
            return ''

        for diag in diags:
            csv = ''
            if diag.diagnosis_type:
                csv += '{0} - '.format(diag.diagnosis_type)

            if not diag.enrollment_type:
                csv += 'Unknown,'
            else:
                csv += '{0},'.format(diag.enrollment_type)

        return csv.rstrip(',')

class AltEnrollmentTypeFormatter(HTMLFormatter):
    def to_html(self, value, **context):
        from .models import PortalSubject

        try:
            sub = PortalSubject.objects.get(ehb_id=value)
            diags = sub.diagnosis_set.all()
        except:
            return '<em>Not Available</em>'

        for diag in diags:
            html = '<ul>'
            if diag.diagnosis_type:
                html += '<em>{0}</em>'.format(diag.diagnosis_type)

            if not diag.enrollment_type:
                html += '<li><em>Unknown</em></li>'
            else:
                html += '<li>{0}</li>'.format(diag.enrollment_type)

            html += '</ul>'

        return html

    def to_csv(self, value, **context):
        try:
            sub = PortalSubject.objects.get(ehb_id=value)
            diags = sub.diagnosis_set.all()
        except:
            return ''

        for diag in diags:
            csv = ''
            if diag.diagnosis_type:
                csv += '{0} - '.format(diag.diagnosis_type)

            if not diag.enrollment_type:
                csv += 'Unknown,'
            else:
                csv += '{0},'.format(diag.enrollment_type)

        return csv.rstrip(',')


class LinkAggFormatter(HTMLFormatter):
    def to_html(self, values, **kwargs):
        from .models import PathFolders, PortalSubject
        sub = PortalSubject.objects.get(ehb_id=values['ehb_id'])
        sdgs = sub.nautilussubject_set.all()

        html = '<i class="icon-info-sign"></i>'
        content = "Pathology slide images and scans are provided in .svs format which is viewable using Aperio ImageScope software. <br><br>Aperio ImageScope software can be downloaded <a target=\'_blank\' href=\'http://www.aperio.com/appcenter\'>here</a>"
        popover = '<script>$(".icon-info-sign").popover({"html":true,"title":"File format info","content":"' + content + '"})</script>'
        urls = ['<ul>']
        for sdg in sdgs:
            urls.append('<ul><em>{0}</em>'.format(sdg.sample_subject_id))
            folders = PathFolders.objects.filter(sample_subject_id=sdg.sample_subject_id)
            links = folders.values('description', 'folder_link')

            for link in links:
                urls.append('<li><a href="{folder_link}">{description}</a></li>'.format(**link))
            urls.append('</ul>')
        if sdgs and links:
            return html + ''.join(urls) + '</ul>' + popover
        else:
            return ''
    to_html.process_multiple = True

    def to_csv(self, values, **kwargs):
        folders = PathFolders.objects.filter(sample_subject_id=values['sample_subject_id'])
        links = folders.values('description', 'folder_link')
        _str = ''
        for link in links:
            _str += '{folder_link},'.format(**link)

        return _str

    to_csv.process_multiple = True


class AliquotAggFormatter(HTMLFormatter):

    field = 'aliquots'

    def _object_to_string(self, aliquot):
        xstr = lambda s: '' if s is None else str(s)
        fmt = '%s %s\n' % (
            xstr(aliquot.aliquot_name),
            xstr(aliquot.secondary_sample_type))

        if aliquot.volume_remaining:
            fmt += '<br>\tVolume Remaining: %s %s' % (
                xstr(aliquot.volume_remaining),
                xstr(aliquot.vol_units))
        if aliquot.concentration:
            fmt += '<br>\tConcentration: %s %s' % (
                xstr(aliquot.concentration),
                xstr(aliquot.conc_units))
        if aliquot.concentration is None and aliquot.volume_remaining is None:
            fmt += '<br>\tVolume and Concentration Unknown'

        return fmt

    def _object_detail(self, aliquot):
        fmt = 'Name: %s' % aliquot.aliquot_name
        fmt += '<br>Type: %s' % aliquot.tissue_type
        fmt += '<br>Received On: %s' % aliquot.received_on
        fmt += '<br>Event: %s' % aliquot.collection_event_name
        fmt += '<br>Note: <br> %s' % aliquot.draw_note
        try:
            if aliquot.sample_type == 'Tissue':
                if aliquot.diagnosis_id.diagnosis_type:
                    fmt += '<br>Associated Diagnosis: <br> %s' % aliquot.diagnosis_id.diagnosis_type
        except:
            pass
        if aliquot.volume_remaining is None or aliquot.volume_received is None:
            fmt += '<br>Availability: <i>Unknown</i> <br>'

        try:
            avail = float(aliquot.volume_received) / float(aliquot.volume_remaining) * 100
        except:
            avail = 0.00
        fmt += '<br>Availability: %s <br>' % ('''<div class=\\\"progress progress-striped\\\"><div class=\\\"bar\\\" style=\\\"width: {}%;\\\"></div></div>'''.format(avail))
        return fmt

    def _build_html(self, pk):
        sdgs = NautilusSubject.objects.filter(ehb_id=pk).all()
        visit_aliquot_set = {}
        for subject in sdgs:
            visits = subject.nautilusvisit_set.all()
            visit_aliquot_set[subject.sample_subject_id] = {}
            for visit in visits:
                visit_aliquot_set[subject.sample_subject_id][visit.visit_name] = {}
                for sample_type in visit.nautilusaliquot_set.filter(parent_aliquot_id__isnull=True).distinct('sample_type').all():
                    visit_aliquot_set[subject.sample_subject_id][visit.visit_name][sample_type.sample_type] = []
                    for aliq in visit.nautilusaliquot_set.filter(sample_type=sample_type.sample_type).filter(parent_aliquot_id__isnull=True).all():
                        aliquot = {
                            'aliquot': self._object_to_string(aliq),
                            'id': aliq.aliquot_id,
                            'content': self._object_detail(aliq),
                            'children': []
                        }
                        for child in visit.nautilusaliquot_set.filter(parent_aliquot_id=aliq.aliquot_id).all():
                            aliquot['children'].append({
                                'id': child.aliquot_id,
                                'aliquot': self._object_to_string(child),
                                'content': self._object_detail(child)
                            })
                        visit_aliquot_set[subject.sample_subject_id][visit.visit_name][sample_type.sample_type].append(aliquot)
        return visit_aliquot_set

    def _build_csv(self, pk, **context):
        sdgs = NautilusSubject.objects.filter(ehb_id=pk).all()
        aliquots = ''
        for sdg in sdgs:
            visits = sdg.nautilusvisit_set.all()
            for visit in visits:
                for aliq in visit.nautilusaliquot_set.all():
                    if aliq.secondary_sample_code:
                        aliquots += "{0} - {1},".format(aliq.aliquot_name, aliq.secondary_sample_code)
                    else:
                        aliquots += "{0},".format(aliq.aliquot_name)
        return aliquots.rstrip(',')

    def to_csv(self, value, **context):
        return self._build_csv(value)

    def to_html(self, value, **context):
        return '<button class="btn btn-primary aliquot_button" data-toggle="modal" data-target="#aliquotList" data-id="{0}">Aliquots</button>'.format(value)

    def __call__(self, values, preferred_formats=None, **context):
        # Create a copy of the preferred formats since each set values may
        # be processed slightly differently (e.g. mixed data type in column)
        # which could cause exceptions that would not be present during
        # processing of other values
        if preferred_formats is None:
            preferred_formats = self.default_formats
        preferred_formats = list(preferred_formats) + ['raw']

        # Create a OrderedDict of the values relative to the
        # concept fields objects the values represent. This
        # enables key-based access to the values rather than
        # relying on position.
        if not isinstance(values, OrderedDict):
            # Wrap single values
            if not isinstance(values, (list, tuple)):
                values = [values]
            values = OrderedDict(zip(self.keys, values))

        # Iterate over all preferred formats and attempt to process the values.
        # For formatter methods that process all values must be tracked and
        # attempted only once. They are removed from the list once attempted.
        # If no preferred multi-value methods succeed, each value is processed
        # independently with the remaining formats
        for f in iter(preferred_formats):
            method = getattr(self, u'to_{0}'.format(f), None)
            # This formatter does not support this format, remove it
            # from the available list
            if not method:
                preferred_formats.pop(0)
                continue

            # The implicit behavior when handling multiple values is to process
            # them independently since, in most cases, they are not dependent
            # on one another, but rather should be represented together since
            # the data is related. A formatter method can be flagged to process
            # all values together by setting the attribute
            # `process_multiple=True`. we must # check to if that flag has been
            # set and simply pass through the values and context to the method
            # as is. if ``process_multiple`` is not set, each value is handled
            # independently
            if getattr(method, 'process_multiple', False):
                try:
                    output = method(values, fields=self.fields,
                                    concept=self.concept,
                                    process_multiple=True, **context)
                    if not isinstance(output, dict):
                        return OrderedDict([(self.concept.name, output)])
                    return output
                # Remove from the preferred formats list since it failed
                except Exception:
                    if self.concept and self.concept not in self._errors:
                        self._errors[self.concept] = None
                        log.warning(u'Multi-value formatter error',
                                    exc_info=True)
                    preferred_formats.pop(0)

        # The output is independent of the input. Formatters may output more
        # or less values than what was entered.
        output = OrderedDict()

        # Attempt to process each
        for i, (key, value) in enumerate(values.iteritems()):
            for f in preferred_formats:
                method = getattr(self, u'to_{0}'.format(f))
                field = self.fields[key] if self.fields else None
                try:
                    fvalue = method(value, field=field, concept=self.concept,
                                    process_multiple=False, **context)
                    if isinstance(fvalue, dict):
                        output.update(fvalue)
                    else:
                        output[self.field] = fvalue
                    break
                except Exception:
                    if field and field not in self._errors:
                        self._errors[field] = None
                        log.warning(u'Single-value formatter error',
                                    exc_info=True)
        return output


class AggregationFormatter(HTMLFormatter):
    '''
        Formatter that aggregates 1-N relationships where the base model
        is related to a PortalSubject
    '''

    model = None
    order_by = None
    field = None

    def _aggregate(self):
        pass

    def _aggregates_to_html(self):
        aggregates = self._aggregate()
        if aggregates:
            return '<ul><li>{0}</li></ul>'.format(
                '</li><li>'.join(str(v) for v in aggregates))
        else:
            return '<em> None Listed </em>'

    def _aggregates_to_csv(self):
        aggregates = self._aggregate()
        if aggregates:
            return'{0}'.format(','.join(str(v) for v in aggregates))

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        return self._aggregates_to_csv()

    def to_html(self, pk, **context):
        self.pk = pk
        self.context = context
        return self._aggregates_to_html()

    def __call__(self, values, preferred_formats=None, **context):
        # Create a copy of the preferred formats since each set values may
        # be processed slightly differently (e.g. mixed data type in column)
        # which could cause exceptions that would not be present during
        # processing of other values
        if preferred_formats is None:
            preferred_formats = self.default_formats
        preferred_formats = list(preferred_formats) + ['raw']

        # Create a OrderedDict of the values relative to the
        # concept fields objects the values represent. This
        # enables key-based access to the values rather than
        # relying on position.
        if not isinstance(values, OrderedDict):
            # Wrap single values
            if not isinstance(values, (list, tuple)):
                values = [values]
            values = OrderedDict(zip(self.keys, values))

        # Iterate over all preferred formats and attempt to process the values.
        # For formatter methods that process all values must be tracked and
        # attempted only once. They are removed from the list once attempted.
        # If no preferred multi-value methods succeed, each value is processed
        # independently with the remaining formats
        for f in iter(preferred_formats):
            method = getattr(self, u'to_{0}'.format(f), None)
            # This formatter does not support this format, remove it
            # from the available list
            if not method:
                preferred_formats.pop(0)
                continue

            # The implicit behavior when handling multiple values is to process
            # them independently since, in most cases, they are not dependent
            # on one another, but rather should be represented together since
            # the data is related. A formatter method can be flagged to process
            # all values together by setting the attribute
            # `process_multiple=True`. we must # check to if that flag has been
            # set and simply pass through the values and context to the method
            # as is. if ``process_multiple`` is not set, each value is handled
            # independently
            if getattr(method, 'process_multiple', False):
                try:
                    output = method(values, fields=self.fields, concept=self.concept, process_multiple=True, **context)
                    if not isinstance(output, dict):
                        return OrderedDict([(self.concept.name, output)])
                    return output
                # Remove from the preferred formats list since it failed
                except Exception:
                    if self.concept and self.concept not in self._errors:
                        self._errors[self.concept] = None
                        log.warning(u'Multi-value formatter error', exc_info=True)
                    preferred_formats.pop(0)

        # The output is independent of the input. Formatters may output more
        # or less values than what was entered.
        output = OrderedDict()

        # Attempt to process each
        for i, (key, value) in enumerate(values.iteritems()):
            for f in preferred_formats:
                method = getattr(self, u'to_{0}'.format(f))
                field = self.fields[key] if self.fields else None
                try:
                    fvalue = method(value, field=field, concept=self.concept, process_multiple=False, **context)
                    if isinstance(fvalue, dict):
                        output.update(fvalue)
                    else:
                        # Override the key value so that CSV exports have the correct header name
                        output[self.field] = fvalue
                    break
                except Exception:
                    raise
                    if field and field not in self._errors:
                        self._errors[field] = None
                        # log.warning(u'Single-value formatter error', exc_info=True)
        return output


# Model Specific Base Aggregators
class SubjectAggregationFormatter(AggregationFormatter):

    def _aggregate(self):
        if self.distinct:
            if self.order_by:
                aggregates = self.model.objects.filter(ehb_id=self.pk).order_by(self.order_by).distinct().values_list(self.field, flat=True)
            else:
                aggregates = self.model.objects.filter(ehb_id=self.pk).distinct().values_list(self.field, flat=True)
        else:
            if self.order_by:
                aggregates = self.model.objects.filter(ehb_id=self.pk).order_by(self.order_by).values_list(self.value, flat=True)
            else:
                aggregates = self.model.objects.filter(ehb_id=self.pk).values_list(self.value, flat=True)

        if None in aggregates:
            return None
        else:
            return aggregates


class AgeAtDiagAggregationFormatter(AggregationFormatter):

    def _aggregate(self):
        aggregates = PortalSubject.objects.get(ehb_id=self.pk).diagnosis_set.order_by('age').all()
        return aggregates

    def _aggregates_to_html(self):
        html = '<ul>'
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                label = diagnosis.diagnosis_type
            else:
                label = 'Diagnosis {0}'.format(diag_count)
                diag_count += 1
            html += '<li>{0}</li><ul>'.format(label)
            if diagnosis.age:
                html += '<li>{0} Months</li>'.format(diagnosis.age)
            else:
                html += '<li><em>None Listed</em></li>'
            html += '</ul>'
        html += '</ul>'
        return html

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        _str = ''
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                _str += '{0},'.format(diagnosis.diagnosis_type)
            else:
                _str += 'Diagnosis {0};'.format(diag_count)
                diag_count += 1
            if diagnosis.age:
                _str += '{0}'.format(diagnosis.age)
            else:
                _str += ','
        return _str


class AgeDescAggregationFormatter(AggregationFormatter):

    def _aggregate(self):
        aggregates = PortalSubject.objects.get(ehb_id=self.pk).diagnosis_set.order_by('age').all()
        return aggregates

    def _aggregates_to_html(self):
        html = '<ul>'
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                label = diagnosis.diagnosis_type
            else:
                label = 'Diagnosis {0}'.format(diag_count)
                diag_count += 1
            html += '<li>{0}</li><ul>'.format(label)
            if diagnosis.age:
                html += '<li>{0}</li>'.format(diagnosis.age_description)
            else:
                html += '<li><em>None Listed</em></li>'
            html += '</ul>'
        html += '</ul>'
        return html

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        _str = ''
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                _str += '{0},'.format(diagnosis.diagnosis_type)
            else:
                _str += 'Diagnosis {0};'.format(diag_count)
                diag_count += 1
            if diagnosis.age:
                _str += '{0}'.format(diagnosis.age)
            else:
                _str += ','
        return _str

class AgeYmdAggregationFormatter(AggregationFormatter):

    def _aggregate(self):
        aggregates = PortalSubject.objects.get(ehb_id=self.pk).diagnosis_set.order_by('age').all()
        return aggregates

    def _aggregates_to_html(self):
        html = '<ul>'
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                label = diagnosis.diagnosis_type
            else:
                label = 'Diagnosis {0}'.format(diag_count)
                diag_count += 1
            html += '<li>{0}</li><ul>'.format(label)
            if diagnosis.age:
                html += '<li>{0}</li>'.format(diagnosis.age_ymd)
            else:
                html += '<li><em>None Listed</em></li>'
            html += '</ul>'
        html += '</ul>'
        return html

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        _str = ''
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                _str += '{0},'.format(diagnosis.diagnosis_type)
            else:
                _str += 'Diagnosis {0};'.format(diag_count)
                diag_count += 1
            if diagnosis.age:
                _str += '{0}'.format(diagnosis.age)
            else:
                _str += ','
        return _str

class DiagnosisAggregationFormatter(AggregationFormatter):

    def _aggregate(self):
        aggregates = PortalSubject.objects.get(ehb_id=self.pk).diagnosis_set.order_by('age').all()
        return aggregates

    def _aggregates_to_html(self):
        html = '<ul>'
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                label = diagnosis.diagnosis_type
            else:
                label = 'Diagnosis {0}'.format(diag_count)
                diag_count += 1
            html += '<li>{0}</li><ul>'.format(label)
            model_name = self.model._meta.object_name.lower()
            aggregates = getattr(diagnosis, '{0}_set'.format(model_name)).all()
            if aggregates:
                for each in aggregates:
                    html += '<li>{0}</li>'.format(getattr(each, self.field))
            else:
                html += '<li><em>None Listed</em></li>'
            html += '</ul>'
        html += '</ul>'
        return html

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        _str = ''
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                _str += '{0},'.format(diagnosis.diagnosis_type)
            else:
                _str += 'Diagnosis {0};'.format(diag_count)
                diag_count += 1
            model_name = self.model._meta.object_name.lower()
            aggregates = getattr(diagnosis, '{0}_set'.format(model_name)).all()
            if aggregates:
                for each in aggregates:
                    _str += '{0}'.format(getattr(each, self.field))
            else:
                _str += ','
        return _str

class DiagnosisTypeAggregationFormatter(AggregationFormatter):

    def _aggregate(self):
        aggregates = PortalSubject.objects.get(ehb_id=self.pk).diagnosis_set.order_by('age').all()
        return aggregates

    def _aggregates_to_html(self):
        html = '<ul>'
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                label = diagnosis.diagnosis_type
            else:
                label = 'Diagnosis {0}'.format(diag_count)
                diag_count += 1
            try:
                last_dx = diagnosis.monthsbetweendx.months_last_diag
            except:
                last_dx = None
            if last_dx:
                label = label + " ({0} months since last Dx)".format(diagnosis.monthsbetweendx.months_last_diag)
            html += '<li>{0}</li><ul>'.format(label)
            html += '<li>{0}</li>'.format(diagnosis.pathhistology_aggr)
            html += '</ul>'
        html += '</ul>'
        return html

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        _str = ''
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                _str += '{0};{1},'.format(diagnosis.diagnosis_type, diagnosis.pathhistology_aggr)
            else:
                _str += 'Diagnosis {0};{1}'.format(diag_count, diagnosis.pathhistology_aggr)
                diag_count += 1

        return _str


class UpdateAggregationFormatter(AggregationFormatter):
    def _aggregate(self):
        aggregates = PortalSubject.objects.get(ehb_id=self.pk).diagnosis_set.order_by('date_of_diagnosis').all()
        return aggregates

    def _aggregates_to_html(self):
        html = '<ul>'
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                label = diagnosis.diagnosis_type
            else:
                label = 'Diagnosis {0}'.format(diag_count)
                diag_count += 1
            html += '<li>{0}</li><ul>'.format(label)
            model_name = self.model._meta.object_name.lower()
            aggregates = getattr(diagnosis, '{0}_set'.format(model_name)).all()
            if aggregates:

                for update in aggregates:
                    html += '<li>{0}</li>'.format(update.update_type)
                    field = getattr(update, self.field)
                    if field:
                        html += '<ul><li>{0}</li></ul>'.format(field)
                    else:
                        html += '<ul><li>{0}</li></ul>'.format('<em>Unknown</em>')

            else:
                html += '<li><em>None Listed</em></li>'
            html += '</ul>'
        html += '</ul>'
        return html

    def to_csv(self, pk, **context):
        self.pk = pk
        self.context = context
        _str = ''
        for diagnosis in self._aggregate():
            diag_count = 1
            if diagnosis.diagnosis_type:
                _str += '{0},'.format(diagnosis.diagnosis_type)
            else:
                _str += 'Diagnosis {0};'.format(diag_count)
                diag_count += 1
            model_name = self.model._meta.object_name.lower()
            aggregates = getattr(diagnosis, '{0}_set'.format(model_name)).all()
            if aggregates:
                for update in aggregates:
                    _str += '{0} Month Update,'.format(update.update_month)
                    field = getattr(update, self.field)
                    if field:
                        _str += '{0},'.format(field)
                    else:
                        _str += ','
            else:
                _str += ','
        return _str


# Diagnosis Based Aggregations
class PathDiagFormatter(DiagnosisAggregationFormatter):
    model = PathHistology
    field = 'path_histology'
    distinct = True

class MolecularTestsDoneFormatter(DiagnosisAggregationFormatter):
    model = TumorOrMolecularTestsD
    field = 'tumor_or_molecular_tests_d'
    distinct = True


class MetasAtSubmitSiteFormatter(DiagnosisAggregationFormatter):
    model = MetasAtSubmitSite
    field = 'metas_at_submit_site'
    distinct = True


class SubjectClinStatusFormatter(UpdateAggregationFormatter):
    model = Update
    field = 'clin_status'
    distinct = True


# Portal Subject Based Aggregations
class FamilyHistoryFormatter(SubjectAggregationFormatter):
    model = MedicalHistoryMain
    field = 'family_history'
    distinct = True


class TumorLocFormatter(SubjectAggregationFormatter):
    model = TumorLocationIn
    field = 'tumor_location_in'
    distinct = True


class RaceFormatter(SubjectAggregationFormatter):
    model = Race
    field = 'race'
    distinct = True


class RelapseNumberFormatter(SubjectAggregationFormatter):
    model = Diagnosis
    field = 'relapse_number2_7d6'
    distinct = True
    order_by = 'date_of_diagnosis'


class SiteOfProgressionFormatter(SubjectAggregationFormatter):
    model = Diagnosis
    field = 'site_prog'
    distinct = True
    order_by = 'date_of_diagnosis'


class DiagnosisTypeListFormatter(SubjectAggregationFormatter):
    model = Diagnosis
    field = 'diagnosis_type'
    distinct = True
    order_by = 'date_of_diagnosis'


class CancerPredispositionFormatter(SubjectAggregationFormatter):
    model = CancPredispCondition
    field = 'canc_predisp_condition'
    distinct = True


class OtherMedConditionFormatter(SubjectAggregationFormatter):
    model = OtherMedCondition
    field = 'other_med_condition'
    distinct = True


class LimsIDFormatter(SubjectAggregationFormatter):
    model = NautilusSubject
    field = 'sample_subject_id'
    distinct = True


registry.register(PathologyReportFormatter, 'PathologyReportFormatter')
registry.register(OperativeReportFormatter, 'OperativeReportFormatter')
registry.register(AgeDescAggregationFormatter, 'AgeDescAggregationFormatter')
registry.register(AgeAtDiagAggregationFormatter, 'AgeAtDiagAggregationFormatter')
registry.register(AgeYmdAggregationFormatter, 'AgeYmdAggregationFormatter')
registry.register(PatientSummaryFormatter, 'PatientSummaryFormatter')
registry.register(LinkAggFormatter, 'LinkAggFormatter')
registry.register(AliquotAggFormatter, 'AliqAggFormatter')
registry.register(TumorLocFormatter, 'TumorLocFormatter')
registry.register(OtherMedConditionFormatter, 'OtherMedConditionFormatter')
registry.register(PathDiagFormatter, 'PathDiagFormatter')
registry.register(RaceFormatter, 'RaceFormatter')
registry.register(MolecularTestsDoneFormatter, 'MolecularTestsDoneFormatter')
registry.register(DiagnosisTypeListFormatter, 'DiagnosisTypeListFormatter')
registry.register(CancerPredispositionFormatter, 'CancerPredispositionFormatter')
registry.register(RelapseNumberFormatter, 'RelapseNumberFormatter')
registry.register(SiteOfProgressionFormatter, 'SiteOfProgressionFormatter')
registry.register(MetasAtSubmitSiteFormatter, 'MetasAtSubmitSiteFormatter')
registry.register(FamilyHistoryFormatter, 'FamilyHistoryFormatter')
registry.register(SubjectClinStatusFormatter, 'SubjectClinStatusFormatter')
registry.register(LimsIDFormatter, 'LimsIDFormatter')
registry.register(EnrollmentTypeFormatter, 'EnrollmentTypeFormatter')
registry.register(AltEnrollmentTypeFormatter, 'AltEnrollmentTypeFormatter')
registry.register(DiagnosisTypeAggregationFormatter, 'DiagnosisTypeAggregationFormatter')
registry.register(cBioLinkFormatter, 'cBioLinkFormatter')
