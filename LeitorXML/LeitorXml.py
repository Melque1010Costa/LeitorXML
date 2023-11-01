# Importa a biblioteca ElementTree do XML
import xml.etree.ElementTree as ET

# Faz o parse do arquivo XML
tree = ET.parse('verbetesWikipedia.xml')

# Classe para realizar operações de busca nas páginas do arquivo XML
class Search:
    # Inicialização da classe
    def __init__(self):
        # Obtém o elemento raiz da árvore XML
        self.root = tree.getroot()
        # Constrói um índice invertido para os títulos das páginas
        self.inverted_index = self.build_inverted_index()

    # Método para construir um Hash invertido dos títulos das páginas
    def build_inverted_index(self):
        inverted_index = {}
        for page in self.root.findall('.//page'):
            page_id = page.find('id').text
            title = page.find('title').text.lower()
            words = title.split()
            for word in words:
                if word not in inverted_index:
                    inverted_index[word] = []
                inverted_index[word].append(page_id)
        return inverted_index

    # Método para buscar páginas por uma única palavra
    def searchBySingleWord(self, word: str) -> None:
        word = word.lower()
        if word in self.inverted_index:
            pages = self.inverted_index[word]
            ListaDeOcorrencia = {}

            for page_id in pages:
                relevancia = self.Calculo_Relevancia(page_id, word)
                ListaDeOcorrencia[page_id] = relevancia

            sorted_pages = sorted(ListaDeOcorrencia.items(), key=lambda x: x[1], reverse=True)
            for page_id, occurrences in sorted_pages:
                title = self.root.find(f'.//page[id="{page_id}"]/title').text
                print(f"ID: {page_id}, Title: {title} - Relevância: {occurrences}")
        else:
            print(f"Nenhuma página encontrada para a palavra: {word}")

    # Método para buscar páginas por duas palavras
    def searchByTwoWords(self, global1: str, global2: str) -> None:
        global1 = global1.lower()
        global2 = global2.lower()
        ListaDeOcorrencia = {}

        for page in self.root.findall('.//page'):
            page_id = page.find('id').text
            title = page.find('title').text.lower()

            if global1 in title and global2 in title:
                RelevanciaGeral1 = self.Calculo_Relevancia(page_id, global1)
                RelevanciaGeral2 = self.Calculo_Relevancia(page_id, global2)
                total_relevance = RelevanciaGeral1 + RelevanciaGeral2
                ListaDeOcorrencia[page_id] = total_relevance

        sorted_pages = sorted(ListaDeOcorrencia.items(), key=lambda x: x[1], reverse=True)
        for page_id, occurrences in sorted_pages:
            title = self.root.find(f'.//page[id="{page_id}"]/title').text
            print(f"ID: {page_id}, Title: {title} - Relevância: {occurrences}")

    # Método para calcular a relevância de uma palavra em uma página específica
    def Calculo_Relevancia(self, page_id, word):
        title = self.root.find(f'.//page[id="{page_id}"]/title').text.lower()
        text = self.root.find(f'.//page[id="{page_id}"]/text').text.lower()

        title_occurrences = title.count(word.lower()) * 10
        text_occurrences = text.count(word.lower())

        return title_occurrences + text_occurrences

    # Método para executar o programa
    def execute(self) -> None:
        while True:
            print("\x1b[2J\x1b[1;1H")
            print("1. Tarefa 01 <page>")
            print("2. Tarefa 02 <title><text>")
            print("3. Tarefa 03 e Tarefa 04")
            print("4. Tarefa 06")
            print("5. Sair\n")
            choice = input("Escolha uma opção (1/2/3/4/5): \n")

            if choice == "1":
                print(f"Quantidade de <page>: {len(self.root.findall('.//page'))}")
            elif choice == "2":
                self.printPageIdsAndTitles()
            elif choice == "3":
                word = input("Digite a palavra de busca: ")
                self.searchBySingleWord(word)
            elif choice == "4":
                words = input("Digite duas palavras de busca separadas por espaço: ").split()
                if len(words) == 2:
                    self.searchByTwoWords(words[0], words[1])
                else:
                    print("Por favor, insira exatamente duas palavras.")
            elif choice == "5":
                break
            else:
                print("Opção inválida. Tente novamente.")

            input("Pressione ENTER para continuar...")
            continue

    # Método para imprimir os IDs e títulos de todas as páginas
    def printPageIdsAndTitles(self):
        for page in self.root.findall('.//page'):
            id = page.find('id').text
            title = page.find('title').text
            print(f"ID: {id}, Title: {title}")

# Cria uma instância da classe Search e executa o programa
search = Search()
search.execute()
