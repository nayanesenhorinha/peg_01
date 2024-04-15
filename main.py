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
            "\nPergunta 1? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nPergunta 2? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nPergunta 3? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: ",
            "\nPergunta 4? \n(1) Sim \n(2) Não \n(3) Não sei \nEscolha uma opção: "
        ]

        # Verifica se o aquivo questionario.csv existe
        if os.path.exists(nome_arquivo):
            # Se existe ele lê o arquivo
            self.respostas = pd.read_csv(nome_arquivo)
            self.num_linhas = len(self.respostas)
        else:
            # Se não existe ele cria
            self.respostas = pd.DataFrame(columns=['ID', 'Idade', 'Gênero', 'Resposta 1', 'Resposta 2', 'Resposta 3', 'Resposta 4', 'Data/Hora'])
            self.num_linhas = 0

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
    
