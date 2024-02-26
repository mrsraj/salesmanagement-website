from django.db import models

# Create your models here.


class user(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    mobile = models.CharField(max_length=255, unique=True)
    pswd = models.CharField(max_length=255)


class customer(models.Model):
    Name = models.CharField(max_length=250)
    Mob_No = models.CharField(max_length=40)
    Addr = models.CharField(max_length=255)
    fk_User_Id = models.ForeignKey(user, on_delete=models.CASCADE)
    Type = models.CharField(max_length=255)


class service(models.Model):
    fk_User_Id = models.ForeignKey(user, on_delete=models.CASCADE)
    fk_customer_Id = models.ForeignKey(customer, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Type = models.CharField(max_length=100)
    Qantity=models.FloatField()
    Date=models.DateField()
    Rate=models.FloatField()

class Payment(models.Model):
    fk_User_Id = models.ForeignKey(user, on_delete=models.CASCADE)
    fk_customer_Id = models.ForeignKey(customer, on_delete=models.CASCADE)
    PayRs= models.FloatField()
    Date=models.DateField()
    