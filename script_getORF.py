#!/usr/bin/env python3  # Especifica o interpretador Python a ser usado para execução do script

import sys  # Importa o módulo sys para lidar com argumentos da linha de comando
import re   # Importa o módulo re para expressões regulares

class Sequencia:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.sequencias = self.pegar_sequencias()

    def pegar_sequencias(self):
        sequencias = {}  # Dicionário para armazenar as sequências do arquivo FASTA
        try:
            with open(self.arquivo, "r") as fasta:  # Abre o arquivo FASTA para leitura
                id_atual = ""
                for linha in fasta:  # Itera sobre as linhas do arquivo
                    linha = linha.rstrip()  # Remove espaços em branco no final da linha
                    if linha.startswith(">"):  # Se a linha começar com ">", é um cabeçalho de sequência
                        id_atual = linha[1:].split()[0]  # Obtém o identificador da sequência
                        sequencias[id_atual] = ""  # Inicializa a sequência para o identificador atual
                    else:
                        sequencias[id_atual] += linha.upper()  # Concatena a linha à sequência atual em letras maiúsculas
        except FileNotFoundError:
            print("Arquivo não encontrado")
            exit()
        return sequencias  # Retorna o dicionário de sequências

class ORF:
    def __init__(self, sequencia):
        self.sequencia = sequencia
        self.stop_codons = ['TAA', 'TAG', 'TGA']

    def reverso_complementar(self):
        reverseSeq = self.sequencia[::-1]  # Inverte a sequência
        reverseSeq = reverseSeq.replace("A", "t").replace("T", "a").replace("C", "g").replace("G", "c")  # Obtém o complemento reverso trocando as bases
        return reverseSeq.upper()  # Retorna o reverso complementar em letras maiúsculas

    def maior_ORF(self):
        if len(self.sequencia) == 0:
            print(" A sequência está vazia")
        big_frame = 0
        big_start = 0
        big_end = 0
        big_sequence = ""

        reverseSeq = self.reverso_complementar()

        for frame in range(6):  # Loop sobre as 6 molduras possíveis (3 na sequência original e 3 no reverso complementar)
            if frame >= 3:
                dna = reverseSeq[frame-3:]
            else:
                dna = self.sequencia[frame:]
            codons = re.findall(r".{3}", dna)  # Divide a sequência em codons de três em três
            frameId = frame + 1

            seq = ""
            i = 0
            for codon in codons:
                i += 1
                if codon == "ATG" and seq == "":
                    seq += codon
                elif codon in self.stop_codons and len(seq) > 0:
                    seq += codon
                    if len(seq) > len(big_sequence):
                        big_sequence = seq
                        big_frame = frameId
                        big_start = (i*3) - len(seq) + 1 + frame%3
                        big_end = (i*3) + frame%3
                    seq = ""
                elif len(seq) > 0:
                    seq += codon
        return big_sequence, big_frame, big_start, big_end  # Retorna a maior ORF encontrada

class Traducao:
    def __init__(self, sequencia):
        self.sequencia = sequencia
        self.translation_table = {...}  # Tabela de tradução de códons para aminoácidos

    def traduzir(self):
        protein = ""
        for i in range(0, len(self.sequencia), 3):  # Loop sobre a sequência em incrementos de 3
            codon = self.sequencia[i: i+3]  # Obtém o próximo codon de 3 bases
            if codon in self.translation_table:
                protein += self.translation_table[codon]  # Traduz o codon para um aminoácido
            else:
                print("Códon não encontrado")
        return protein  # Retorna a sequência de aminoácidos traduzida

def main():
    try:
        arquivo = sys.argv[1]  # Obtém o nome do arquivo a partir dos argumentos da linha de comando
    except IndexError:
        print("Forneça um arquivo de entrada")
        exit()

    sequencias = Sequencia(arquivo).sequencias  # Obtém as sequências do arquivo FASTA
    with open("ORF.fna", "w") as fna, open("ORF.faa", "w") as faa:  # Abre arquivos de saída para escrita
        for identificador in sequencias:
            orf = ORF(sequencias[identificador])  # Cria um objeto ORF para a sequência atual
            sequencia, frame, start, end = orf.maior_ORF()  # Encontra a maior ORF na sequência
            peptideo = Traducao(sequencia).traduzir()  # Traduz a ORF para um peptídeo
            fna.write(f">{identificador}_frame{frame}_{start}_{end}\n{sequencia}\n")  # Escreve a sequência de DNA no arquivo de saída
            faa.write(f">{identificador}_frame{frame}_{start}_{end}\n{peptideo}\n")  # Escreve o peptídeo no arquivo de saída

if __name__ == "__main__":
    main()  # Chama a função principal se o script for executado como um programa independente
