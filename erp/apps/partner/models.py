from django.db import models


class PartnerType(models.Model):
    Type = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % (self.Type)


class PartnerSector(models.Model):
    Sector = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.Sector


class PartnerSegment(models.Model):
    Segment = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.Segment


class BankName(models.Model):
    Name = models.CharField(max_length=100)
    Code = models.CharField(max_length=10)

    def __unicode__(self):
        return u'%s' % self.Name


class Partner(models.Model):
    PartnerName = models.CharField(max_length=200)
    Type = models.ForeignKey(PartnerType, blank=True, null=True)
    Sector = models.ForeignKey(PartnerSector, blank=True, null=True)
    Segment = models.ForeignKey(PartnerSegment, blank=True, null=True)
    CompanyId = models.CharField(max_length=100, blank=True, null=True)
    BankAccount = models.CharField(max_length=50, blank=True, null=True)
    BankName = models.ForeignKey(BankName, blank=True, null=True)
    TaxId = models.CharField(max_length=100, blank=True, null=True)
    VatId = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.PartnerName


class PartnerContact(models.Model):
    Note = models.TextField(null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    State = models.CharField(max_length=100, null=True, blank=True)
    Phone = models.CharField(max_length=50, null=True, blank=True)
    Address = models.CharField(max_length=100, null=True, blank=True)
    ZipCode = models.CharField(max_length=100, null=True, blank=True)
    Partner = models.ForeignKey(Partner, null=True, blank=True)