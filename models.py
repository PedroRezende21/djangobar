from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome_do_produto = models.CharField(max_length=100, unique=True)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

class Historico(models.Model):
    nome_do_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_do_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    debito = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        produto = Produto.objects.get(pk=self.nome_do_produto.pk)
        self.valor = produto.preco * self.quantidade
        super().save(*args, **kwargs)
