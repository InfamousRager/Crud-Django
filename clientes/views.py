from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm
from .entidades import cliente
from .services import cliente_service



# Create your views here.

def listar_clientes(request):
    clientes = cliente_service.listar_clientes()
    return render(request, 'clientes/lista_clientes.html',{'clientes':clientes})

def inserir_cliente(request):
    if request.method =="POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["nome"]
            sexo = form.cleaned_data["sexo"]
            email = form.cleaned_data["email"]
            data_nascimento = form.cleaned_data["data_nascimento"]
            profissao = form.cleaned_data["profissao"]

            cliente_novo = cliente.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email,profissao=profissao) # salvando e criando objeto do tipo cliente com dados vindo do formulário
            cliente_service.cadastrar_cliente(cliente_novo)
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request,'clientes/form_cliente.html',{'form':form})

def listar_cliente_id(request,id):
    cliente = cliente_service.listar_cliente_id(id)
    return render(request,'clientes/lista_cliente.html',{'cliente':cliente})

def editar_cliente(request,id):
    cliente_antigo= cliente_service.listar_cliente_id(id)
    form = ClienteForm(request.POST or None,instance=cliente_antigo) #busca o cliente e envia os dados da requisição sendo feita , instance serve pra quando tu clickar em editar os dados do cliente já estejam preenchidos
    if form.is_valid():
        nome = form.cleaned_data["nome"]
        sexo = form.cleaned_data["sexo"]
        email = form.cleaned_data["email"]
        data_nascimento = form.cleaned_data["data_nascimento"]
        profissao = form.cleaned_data["profissao"]
        cliente_novo = cliente.Cliente(nome=nome, sexo=sexo, data_nascimento=data_nascimento, email=email,profissao=profissao)
        cliente_service.editar_cliente(cliente_antigo,cliente_novo)
        return redirect('listar_clientes')
    return render(request,'clientes/form_cliente.html',{'form':form})

def remover_cliente(request,id):
    cliente = cliente_service.listar_cliente_id(id)
    if request.method == "POST":
        cliente_service.remover_cliente(cliente)
        return redirect('listar_clientes')

    return render(request,'clientes/confirma_exclusao.html',{'cliente':cliente})
