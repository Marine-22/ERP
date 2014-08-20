from django.db import models

class FinanceType(models.Model):
    FinanceType = models.CharField(max_length=100)

class Vehicle(models.Model):
    PlateNumber = models.CharField(max_length=20)
    Model = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    YearOfPurchase = models.DateField()
    FinanceType = models.ForeignKey(FinanceType)

class Phone(models.Model):
    PhoneNumber = models.CharField(max_length=20)
    Imei = models.CharField(max_length=100)
    Model = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)

class VehicleContract(models.Model):
    Vehicle = models.ForeignKey(Vehicle)

class PhoneContract(models.Model):
    Phone = models.ForeignKey(Phone)