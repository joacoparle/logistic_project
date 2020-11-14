from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver



class Client(models.Model):
    """
    Modelo de cliente, name va para el nombre de la empresa que presenta el paquete para enviar
    además va con el mail, teléfono y direccion de la empresa
    """
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mail = models.EmailField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

############################################################################################################

class Package(models.Model):
    """
    Modelo para Paquete, con un tracking id (que se caluclua en el presave)
    destination adress, phone y name refieren a dónde se envie el paquete, a quién, y un teléfono
    size es un lavor S, M o L que se calcula según el peso del paquete.
    """
    tracking_id = models.IntegerField(unique=True)
    destination_address = models.CharField(max_length=200)
    destination_phone = models.CharField(max_length=50, blank=True)
    destination_name = models.CharField(max_length=200, blank=True)
    weigth = models.FloatField(default=1)
    heigth = models.FloatField(null=True, blank=True)
    size = models.CharField(max_length=2, default='S')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.tracking_id)


@receiver(pre_save, sender=Package)
def pack_callback(sender, instance, *args, **kwargs):
    """
    Esta función corre antes de guardar un package, lo que hace es calcular el tracking_id según el último valor
    que existe, si no hay otro paquete creado antes, se agrega por defecto el 1ro.
    Luego se hace un if para calcula el size, tomando weight, vemos si es menor que 1000, entre 1000 y 3000, o mayor
    (S,M,L
    """
    if not instance.pk:
        if Package.objects.first() != None:
            instance.tracking_id = Package.objects.last().id + 1100001
        else:
            instance.tracking_id = 1100001
        size = instance.weigth
        if int(size) < 1000:
            instance.size = 'S'
        elif int(size) < 3000:
            instance.size = 'M'
        else:
            instance.size = 'L'

###################################################################################################################
class SpreadSheet(models.Model):
    """
    Modelo para Planilla, tiene una sheet id que guardará el numero de la planilla (lo calcula automatiocamente
    el pre-save)
    Date es la fecha donde se crea tal planilla.

    Datos de desarrollo:
    En vés de agregar a los paquetes de cada planilla directamente, se crea el modelo SheetItem,
    por el cual vamos a poder conectar cada package a una Spreadsheet (osea cada paquete a la planilla).
    Otra forma de resolverlo puede ser agregar una key ManyToMany para un valor packages dentro de este modelo,
    y que esta contuviese todos los paquetes de cada instancia de planilla
    """
    sheet_id = models.IntegerField(unique=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.sheet_id)


@receiver(pre_save, sender=SpreadSheet)
def sheet_callback(sender, instance, *args, **kwargs):
    """
    Pre-save que genera el valor de sheet id siguiendo el valor de la anterior planilla
    """
    if not instance.pk:
        if SpreadSheet.objects.first() != None:
            instance.sheet_id = SpreadSheet.objects.last().id + 9900001
        else:
            instance.sheet_id = 9900001

#############################################################################################

class SheetItem(models.Model):
    """
    Item de Planilla
    ----------------
    Tiene dos ForeignKey, una para packages y otra para spreadsheet, relacionando así los dos modelos.
    Date created es la frecha de creación
    Pos es la posición en la que se agrega este tiem de planilla (se calcula luego en el pre-save antes de guardarse
    Status hace referencia a el estado del packete de una planilla. EL valos es un Integer porque se toma STATUS_TYPES
    como referencia y con un valor numérico de 1 a 4 tenemos el estado representado (Complete, lost, damaged, incomplete)
    Se incluye de esta forma así en un futuro para conseguir la estadística del estado de los paquetes, será solo cuestión
    de consulta el "status" de cada uno
    """
    COMPLETE = 1
    LOST = 2
    DAMAGED = 3
    INCOMPLETE = 4

    STATUS_TYPES = (
        (COMPLETE, 'Complete'),
        (LOST, 'Lost'),
        (DAMAGED, 'Damaged'),
        (INCOMPLETE, 'Incomplete'),
    )

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    spreadsheet = models.ForeignKey(SpreadSheet, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    pos = models.IntegerField(blank=True)
    status = models.IntegerField(choices=STATUS_TYPES, default=1)



    def __str__(self):
        return str(self.id)


@receiver(pre_save, sender=SheetItem)
def sheet_item_callback(sender, instance, *args, **kwargs):
    if not instance.pk:
        if SheetItem.objects.first() != None:
            instance.pos = SheetItem.objects.last().pos + 1
        else:
            instance.pos = 1
