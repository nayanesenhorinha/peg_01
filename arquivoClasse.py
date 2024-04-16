# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import os

class Questionario:
    def __init__(self, nome_arquivo='questionario.csv', nome_arquivo_backup = 'backup.csv'):
        # Atributos da classe Questionário
        self.nome_arquivo = nome_arquivo
        self.nome_arquivo_backup = nome_arquivo_backup
        self.backup = []
        self.linha_backup = []
        self.perguntas = [
            "\nVocê utiliza IA para pesquisas? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nVocê acredita que a IA pode substituir alguma tarefa que você realiza no dia a dia? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nA IA já te ajudou em alguma situação importante? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nVocê se sentiria seguro com a IA atuando na área da saúde ou de segurança? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nVocê acredita que num futuro próximo a IA substituirá os humanos em alguns postos de trabalho? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: "
        ]
        # Verifica se o aquivo questionario.csv existe
        if os.path.exists(nome_arquivo):
            # Se existe ele lê o arquivo
            self.respostas = pd.read_csv(nome_arquivo)
            self.num_linhas = len(self.respostas)
        else:
            # Se não existe ele cria
            self.respostas = pd.DataFrame(columns=['ID', 'Idade', 'Gênero', 'Resposta 1', 'Resposta 2', 'Resposta 3', 'Resposta 4', 'Resposta 5', 'Data/Hora'])
            self.num_linhas = 0
    # Função que salva a linha no arquivo backup
    def salva_backup(self):
        if os.path.exists(self.nome_arquivo_backup):
            self.backup = pd.read_csv(self.nome_arquivo_backup)
            new_df_backup = pd.DataFrame(self.linha_backup)
            self.backup = pd.concat([self.backup, new_df_backup], ignore_index=True).drop_duplicates()
        else:
            self.backup = pd.DataFrame(self.linha_backup)
        self.backup.to_csv(self.nome_arquivo_backup, index=False) 
    def maior_id(self):
        # Verifica no arquivo csv, na coluna ID, qual é o maior valor e atribui à variável maior_id + 1
        # Se o arquivo csv não existir, atribui a variável maior_id o valor 1
        if os.path.exists(self.nome_arquivo):
            maior_id = max(self.respostas['ID'].tolist())+1
        else:
            maior_id=1
        return maior_id
    def coletar_informacoes(self):
        # Função que coleta os dados do usuário no prompt, e atribui as variáveis
        while True:
            try:
                idade = int(input("\nDigite sua idade (00 para não inserir dados):\n"))
                if idade == 0:
                    return False
                elif idade < 0 or idade > 150:
                    raise ValueError("Idade inválida. Por favor, insira uma idade válida.")
                break
            except ValueError as e:
                print(e)
        while True:
            genero = input("\nDigite seu gênero (M/F):\n ").upper()
            if genero in ['M', 'F']:
                break
            else:
                print("Gênero inválido. Por favor, insira 'M' para masculino ou 'F' para feminino.")
        # Atribui o maior_id, a idade, e o gênero ao dicionário respostas
        respostas = {'ID': self.maior_id(),'Idade': idade, 'Gênero': genero}
        for i, pergunta in enumerate(self.perguntas, start=1):
            # Percorre a string de perguntas
            while True:
                resposta = input(pergunta)
                if resposta in ['1', '2', '3']:
                    break
                else:
                    print("Resposta inválida. Por favor, insira '1', '2' ou '3'.")
            # Substitui os números por 1,2,3 por "Sim","Não","Não sabe" respectivamente
            # Atribui as repostas ao dicionário respostas
            if resposta == '1':
                respostas[f'Resposta {i}'] = 'sim'
            elif resposta == '2':
                respostas[f'Resposta {i}'] = 'não'
            else:
                respostas[f'Resposta {i}'] = 'não sabe'
        respostas['Data/Hora'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Concatena o dicionário respostas ao csv
        self.respostas = pd.concat([self.respostas, pd.DataFrame([respostas])], ignore_index=True)
        self.num_linhas +=1
        return True
    # Função chamada para remover resposta do formulário
    def remove_linha(self):
        id = int(input('Digite o ID a ser deletado: '))
        if id in self.respostas['ID'].tolist():
            self.linha_backup = self.respostas[self.respostas['ID'] == id]
            self.respostas = self.respostas[self.respostas['ID'] != id]
            self.respostas.to_csv(self.nome_arquivo, index=False)
            self.num_linhas -= 1
            print(f'Linha com ID {id} removida do arquivo CSV.')
            self.salva_backup()
            return True
        else:
            print("ID não encontrado.")
            return False
    # Função chamada para adicionar uma linha ao csv
    def escrever_csv(self):
        if os.path.exists(self.nome_arquivo):
            df = pd.read_csv(self.nome_arquivo)
            new_df = pd.DataFrame(self.respostas)
            # Verifica se há respostas duplicadas antes de adicionar
            df = pd.concat([df, new_df], ignore_index=True).drop_duplicates()
        else:
            df = pd.DataFrame(self.respostas)
        df.to_csv(self.nome_arquivo, index=False)
    # Função chamada pelo exibir o arquivo csv no console
    def exibir_resultados(self):
        df = pd.DataFrame(self.respostas)
        print("\nResultados do Questionário: \n")
        print(df)
        print(f'Numero de linhas: {self.num_linhas}')