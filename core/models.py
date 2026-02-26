from django.db import models

class Autor(models.Model):
    autor = models.CharField(max_length=100,verbose_name="Autor")
    pais = models.CharField(max_length=100,verbose_name="País")

    class Meta:
        verbose_name = 'autor'
        verbose_name_plural = 'autores'
        ordering = ['autor']

    def __str__(self):
        return f"{self.autor} | {self.pais}"
    

class Libro(models.Model):

    IDIOMAS = [
        ('EN','Inglés'),
        ('ES','Español'),
        ('DE','Alemán'),
        ('FR','Francés'),
        ('PT','Portugués'),
        ('IT','Italiano'),
    ]

    titulo = models.CharField(max_length=250)
    fecha_publicacion = models.DateField()
    idioma = models.CharField(max_length=2,choices=IDIOMAS)
    paginas = models.PositiveIntegerField(verbose_name='páginas',default=0)
    autores = models.ManyToManyField(Autor,related_name='libros')

    class Meta:
        verbose_name = 'libro'
        verbose_name_plural = 'libros'
        ordering = ['idioma','titulo']

    def __str__(self):
        return self.titulo