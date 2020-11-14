import codecs
import csv
from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path
from .models import Client, Package, SpreadSheet, SheetItem



class SheetItemInline(admin.TabularInline):
    """
    Los siguientes son InLines de SheetItem, en este caso para mostrarlo en Packages y SpreadSheet
    """
    readonly_fields = ['pos']
    list_display = ['package', 'date','pos']
    model = SheetItem
    extra = 1

class InfoSheetItemInline(admin.TabularInline):
    """
    En este caso se llama InfoSheetItemInLine pues la mostramos en Package y ahi solo se muestra, no se podrá editar
    """
    readonly_fields = ['spreadsheet', 'package', 'pos', 'status']
    model = SheetItem

    def has_add_permission(self, request, obj):
        return False


# ----------------------------------------------------------------------------------------------

class CsvImportForm(forms.Form):
    """
    # Clase de tipo form con el que vamos a poder hacer el import de packages desde un csv
    """
    csv_file = forms.FileField()

###########################
# ModelAdmin de Packages:
###########################

class PackageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('client', 'weigth', 'heigth')
                }),
        ('Destination', {
            'fields': ('destination_address', 'destination_phone', 'destination_name')}))

    search_fields = ['tracking_id', 'client__name']

    list_filter = ['client','size']

    list_display = ['tracking_id', 'client', 'destination_address', 'destination_phone', 'destination_name', 'size']

    # Gracias al inline podemos ver en que planilla/s está cada paquete
    inlines = [InfoSheetItemInline]

    # Sobreescribimos el template de change_list para package y editar como se ve la págiina en el admin y agregar
    change_list_template = 'admin/package_system/package_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [

            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """
        Función que hace el import del csv a nuestro sistema, acá se lee el archivo csv, se comparan los valores y:
        -Se crea la planilla donde se agregarán todos los paquetes del archivo
        -Se leen las filas de Packages y se crean(si es que no existen) los paquetes en el sistema
        -Se agregan todos a la planilla creada
        -Por último se crea y agrega la relacion Package-SpreadSheet en SheetItem
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            try:
                headers = next(reader)
                s = SpreadSheet.objects.create()
                for row in reader:
                    tracking_id = row[0]
                    destination_address = row[1]
                    destination_phone = row[2]
                    destination_name = row[3]
                    weigth = row[4]
                    heigth = row[5]
                    cliente = row[6]
                    c, created = Client.objects.get_or_create(name=cliente)
                    try:
                        p = Package.objects.get(tracking_id=tracking_id)
                    except Package.DoesNotExist:
                        p = Package(
                            destination_address=destination_address,
                            destination_phone=destination_phone,
                            destination_name=destination_name,
                            weigth=weigth,
                            heigth=heigth,
                            client=c
                        )
                        p.save()
                    si = SheetItem(package=p, spreadsheet=s)
                    si.save()
                self.message_user(request, "El csv fue cargado con exito'")
                headers = 0
            except (ValueError, IndexError):
                s = SpreadSheet.objects.last()
                s.delete()
                self.message_user(request, "El archivo Csv ingresado no es válido", level=messages.ERROR)
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


class SheetItemAdmin(admin.ModelAdmin):
    fields = ('spreadsheet', 'package', 'status')
    readonly_fields = ['date_created', 'pos']
    search_fields = ['spreadsheet', 'package']
    list_editable = ['status']
    list_filter = ['spreadsheet', 'status']
    list_display = ('pos', 'spreadsheet', 'package', 'date_created', 'status')


class SpreadSheetAdmin(admin.ModelAdmin):
    fields = []
    search_fields = ['sheet_id']
    list_filter = []
    list_display = ['sheet_id', 'date']
    readonly_fields = ['sheet_id', 'date']

    # Gracias a este inline podemos agregar uno o más paquetes al crear/editar
    # planilla
    inlines = [
        SheetItemInline
    ]


class ClientAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'phone', 'mail']
    list_display = ['name', 'address', 'phone', 'mail']


#################### Registers en el admin ####################################
admin.site.register(Package, PackageAdmin)
admin.site.register(SpreadSheet, SpreadSheetAdmin)
admin.site.register(SheetItem, SheetItemAdmin)
admin.site.register(Client, ClientAdmin)
