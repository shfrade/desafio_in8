from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Gerando o Token de forma automatica para cada usuário novo.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Autor(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    edicao = models.PositiveIntegerField(default=1)
    autor = models.ManyToManyField('Autor', related_name='autores_dos_livros')

    def __str__(self):
        return f"{self.titulo} - Edição: {self.edicao}"


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.nome}"


class Emprestimo(models.Model):
    aluno = models.ForeignKey(Aluno, models.CASCADE)
    livro = models.ForeignKey(Livro, models.PROTECT)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True)

    def __str__(self):
        return f"{self.livro} para o aluno(a) {self.aluno.nome} foi emprestado em {self.data_emprestimo}"

    @property
    def emprestado(self):
        if self.data_devolucao is None:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.data_devolucao < self.data_emprestimo:
            raise Exception("A data de devolução deve ser maior ou igual a data de emprestimo.")
        super().save(*args, **kwargs)  # Call the "real" save() method.
