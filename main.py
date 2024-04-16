# -*- coding: utf-8 -*-

import arquivoClasse as module

# Função principal
def main():
    questionario = module.Questionario()
    
    while True:
        opcao = input("\nOperações:\n\n1) Fazer pesquisa\n2) Mostrar tabela\n3) Remover resposta\n0) Encerrar\n\nEscolha uma opção: ")
        if opcao == '1':
            questionario.coletar_informacoes()
            questionario.escrever_csv()
            questionario.exibir_resultados()
        elif opcao == '2':
            questionario.exibir_resultados()
        elif opcao == '3':
            questionario.remove_linha()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Por favor, escolha '1', '2', '3' ou '0'.")

main()