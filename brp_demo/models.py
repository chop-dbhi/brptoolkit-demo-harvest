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


class Visit(models.Model):
    '''
    Visit Model
    '''
    ehb = models.ForeignKey(PortalSubject)
    visit_id = models.CharField(max_length=255, primary_key=True)
    visit_type = models.CharField(max_length=255)
    height = models.IntegerField()
    weight = models.IntegerField()
    prealbumin = models.FloatField()
    creatine = models.FloatField()
    total_chol = models.FloatField()
    transferrin = models.FloatField()
    ibd_flag = models.BooleanField()

    class Meta:
        db_table = u'visit'
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'

class Meal(models.Model):
    '''
    Meal Model
    '''
    id = models.IntegerField(primary_key=True)
    ehb = models.ForeignKey(PortalSubject)
    visit = models.ForeignKey(Visit)
    meal_type = models.CharField(max_length=255)
    meal_description = models.CharField(max_length=255)
    healthy = models.CharField(max_length=255)

    class Meta:
        db_table = u'meal'
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'


class Medication(models.Model):
    '''
    Medication model
    '''
    id = models.IntegerField(primary_key=True)
    ehb = models.ForeignKey(PortalSubject)
    visit = models.ForeignKey(Visit)
    visit_type = models.CharField(max_length=255)
    med_type = models.CharField(max_length=255)

    class Meta:
        db_table = u'visit_medications'
        verbose_name = 'Visit Medication'
        verbose_name_plural = 'Visit Medications'
