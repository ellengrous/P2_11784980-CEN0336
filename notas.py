'''
Explicação do pseudocódigo

1 - Inicializa a variável TOTAL com zero.
2 - Inicializa a variável CONTADOR NOTAS com zero.
3 - Entra em um loop enquanto CONTADOR NOTAS for menor ou igual a dez.
4 - Solicita ao usuário que insira uma nota.
5 - Adiciona a nota à variável TOTAL.
6 - Incrementa o CONTADOR NOTAS.
7 - Após o loop, calcula a média da disciplina dividindo o TOTAL por dez.
8 - Imprime a média da disciplina na tela.

OBS: Há um problema no código ao iterar sobre o loop, o mesmo não tem uma condição de parada, causando loop infinito no script
Adicionei na linha 22 a condição para que o contador seja incrimentado
Dessa forma o loop irá parar após a inserção de 10 notas
'''

TOTAL = 0
CONTADOR_NOTAS = 0

while CONTADOR_NOTAS <= 10:
   nota = float(input("Insira a nota: "))
   TOTAL += nota
   CONTADOR_NOTAS += 1

media = TOTAL / 10
print("A média da disciplina é:", media)
