from django.db import models

# Create your models here.
class Directory (models.Model):
    path = models.CharField(max_length=4096)
    name =models.CharField(max_length=255)
    parent  = models.ForeignKey('self',on_delete= models.CASCADE())
    permission = models.ForeignKey(Permission,on_delete= models.CASCADE())

    def test(self):
        return self.name



