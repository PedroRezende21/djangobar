from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Produto, Historico
from django.contrib.auth import get_user_model

User = get_user_model()


def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    return render(request, 'registro.html')

def logout_usuario(request):
    logout(request)
    messages.success(request, 'Logout realizado')
    return redirect('home')

@login_required(login_url='login')
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})


@login_required(login_url='login')
def comprar(request):
    produtos = Produto.objects.all()

    if request.method == 'POST':
        nome_do_produto = request.POST['produto']
        quantidade = int(request.POST['quantidade'])
        produto = Produto.objects.get(nome_do_produto=nome_do_produto)
        
        # Verificar se a quantidade desejada está disponível no estoque
        if quantidade > produto.quantidade:
            # Quantidade insuficiente no estoque
            messages.error(request, 'Quantidade insuficiente no estoque.')
            return redirect('comprar')

        # Subtrair a quantidade comprada do estoque
        produto.quantidade -= quantidade
        produto.save()

        # Criar um registro no histórico de compras
        usuario = request.user
        print(usuario)
        historico = Historico(nome_do_usuario=usuario, nome_do_produto=produto, quantidade=quantidade, debito=produto.preco * quantidade)
        historico.save()

        messages.success(request, 'Compra realizada com sucesso!')
        return redirect('home')

    return render(request, 'comprar.html', {'produtos': produtos})


@staff_member_required
@login_required(login_url='login')
def adicionar_produto(request):
    if request.method == 'POST':
        nome_do_produto = request.POST['nome']
        quantidade = int(request.POST['quantidade'])
        preco = float(request.POST['preco'])
        Produto.objects.create(nome_do_produto=nome_do_produto, quantidade=quantidade, preco=preco)
        messages.success(request, 'Produto adicionado com sucesso!')
        return redirect('home')
    return render(request, 'adicionar_produto.html')

@staff_member_required
@login_required(login_url='login')
def excluir_produto(request, produto_id):
    produto = Produto.objects.get(pk=produto_id)
    produto.delete()
    messages.success(request, 'Produto excluído com sucesso!')
    return redirect('home')

@staff_member_required
@login_required(login_url='login')
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, pk=int(produto_id))
    if request.method == 'POST':
        produto.nome_do_produto = request.POST['nome']
        produto.quantidade = int(request.POST['quantidade'])
        produto.preco = float(request.POST['preco'])
        produto.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('home')
    return render(request, 'editar_produto.html', {'produto': produto})

@staff_member_required
@login_required(login_url='login')
def reposicao_produto(request, produto_id):
    produto = Produto.objects.get(pk=produto_id)
    if request.method == 'POST':
        quantidade = int(request.POST['quantidade'])
        produto.quantidade += quantidade
        produto.save()
        messages.success(request, 'Produto reposto com sucesso!')
        return redirect('home')
    return render(request, 'reposicao_produto.html', {'produto': produto})


@login_required(login_url='login')
def historico(request):
    historicos = Historico.objects.filter(usuario=request.user)
    saldo_total = sum(historico.produto.preco * historico.quantidade for historico in historicos)
    return render(request, 'historico.html', {'historicos': historicos, 'saldo_total': saldo_total})

@staff_member_required(login_url='login')
@login_required(login_url='login')
def deletar_historico(request):
    if request.method == 'POST':
        usuario_id = request.POST['usuario']
        try:
            usuario = User.objects.get(id=usuario_id)
            Historico.objects.filter(nome_do_usuario=usuario).delete()
            messages.success(request, 'Histórico excluído com sucesso para o usuário selecionado.')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        return redirect('home')

    usuarios = User.objects.all()
    return render(request, 'deletar_historico.html', {'usuarios': usuarios})

@login_required(login_url='login')
def historico_consumo(request):
    # Obtém o usuário logado
    usuario = request.user

    # Filtra o histórico de consumo do usuário logado
    historicos = Historico.objects.filter(nome_do_usuario=usuario)

    # Calcula o saldo total
    saldo_total = sum(historico.nome_do_produto.preco * historico.quantidade for historico in historicos)

    # Renderiza o template 'historico_consumo.html' com os dados do histórico e saldo total
    return render(request, 'historico_consumo.html', {'historicos': historicos, 'saldo_total': saldo_total})