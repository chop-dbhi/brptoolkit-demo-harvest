from django.db import models


class PortalSubject(models.Model):
    '''
    Base Model. The eHB Subject
    '''
    ehb_id = models.CharField(max_length=255, primary_key=True)
    research_id = models.CharField(max_length=255)

    class Meta:
        db_table = u'portal_subject'
        verbose_name = 'Portal Subject'
        verbose_name_plural = 'Portal Subjects'


class Subject(models.Model):
    '''
    Basic demographics regarding the Subject. Has 1-1 relationship to a REDCap
    entry.
    '''
    ehb = models.ForeignKey(PortalSubject)
    ethnicity = models.CharField(max_length=255)
    race = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    given_birth = models.CharField(max_length=255)
    num_children = models.CharField(max_length=255)
    study_id = models.CharField(max_length=255, primary_key=True)

    class Meta:
        db_table = u'subject'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
