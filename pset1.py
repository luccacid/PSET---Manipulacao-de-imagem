# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: LUCCA CID DOS SANTOS
#    Matrícula: 202200268
#    Turma: CC6N
#    Email: luccacids@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels


    def get_pixel(self, x, y):
            '''self.pixels é uma lista, não uma matriz, por isso a notação de tupla teve que ser substituida por uma notação de lista. 
        y * self.largura + x' calcula o indice na posição do pixel nessa lista. Alem disso, foi implementado um tratamento para as bordas, para métodos que necessitam.'''
            # Trata bordas para não acessar índices inválidos
            if x < 0:
                x = 0  # Limita o valor de x ao mínimo (0)
            elif x >= self.largura:
                x = self.largura - 1  # Limita o valor de x ao máximo (largura - 1)

            if y < 0:
                y = 0  # Limita o valor de y ao mínimo (0)
            elif y >= self.altura:
                y = self.altura - 1  # Limita o valor de y ao máximo (altura - 1)

            return self.pixels[y * self.largura + x]  # Retorna o valor do pixel na posição (x, y)


    def set_pixel(self, x, y, c):
        self.pixels[y * self.largura + x] = c

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(self.largura):  # Correção: troca do Y pelo X
            for y in range(self.altura):  # Correção: troca do X pelo Y
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)  # Y e X trocados de lugar
        return resultado

    def invertida(self):
        # 256 substituido por 255
        return self.aplicar_por_pixel(lambda c: 255 - c)


    def kernel_borrado(self, n):
        '''Cria um kernel n x n.'''
        valor_kernel = 1 / (n * n)  # Calcula o valor de cada elemento do kernel
        return [[valor_kernel for _ in range(n)] for _ in range(n)]  # Cria um kernel n x n com valores iguais


    def borrada(self, n):
        '''Aplica um desfoque à imagem usando um kernel de tamanho n.'''
        kernel = self.kernel_borrado(n)  # Obtém o kernel
        nova_imagem = Imagem.nova(self.largura, self.altura)  # Cria uma nova imagem em branco

        compensacao_kernel_borda = n // 2  # Calcula o deslocamento do kernel
        for x in range(self.largura):  # Loop sobre a largura da imagem
            for y in range(self.altura):  # Loop sobre a altura da imagem
                soma = 0  # Inicializa a soma dos pixels
                for kx in range(-compensacao_kernel_borda, compensacao_kernel_borda + 1):  # Loop sobre a largura do kernel
                    for ky in range(-compensacao_kernel_borda, compensacao_kernel_borda + 1):  # Loop sobre a altura do kernel
                        pixel_x = x + kx  # Calcula a coordenada x do pixel atual
                        pixel_y = y + ky  # Calcula a coordenada y do pixel atual
                        valor_pixel = self.get_pixel(pixel_x, pixel_y)  # Obtém o valor do pixel
                        soma += valor_pixel * kernel[kx + compensacao_kernel_borda][ky + compensacao_kernel_borda]  # Aplica o kernel na soma

                nova_cor = int(max(0, min(255, round(soma))))  # Arredonda e limita o valor para [0, 255]
                nova_imagem.set_pixel(x, y, nova_cor)  # Define o novo valor do pixel na imagem borrada

        return nova_imagem


    def focada(self, n):
        '''Aplica um efeito de foco à imagem com base no desfoque de um kernel de tamanho n.'''
        borrada = self.borrada(n)  # Aplica o desfoque
        nova_imagem = Imagem.nova(self.largura, self.altura)  # Cria uma nova imagem em branco

        for x in range(self.largura):  # Loop sobre a largura da imagem
            for y in range(self.altura):  # Loop sobre a altura da imagem
                original = self.get_pixel(x, y)  # Obtém o valor do pixel original
                borrado = borrada.get_pixel(x, y)  # Obtém o valor do pixel borrado
                valor_focado = round(2 * original - borrado)  # Calcula o valor focado
                valor_focado = max(0, min(255, valor_focado))  # Limita o valor focado para [0, 255]
                nova_imagem.set_pixel(x, y, valor_focado)  # Define o valor focado na nova imagem

        return nova_imagem


    def bordas(self):
        '''Detecta bordas na imagem usando o operador de Sobel.'''
        Kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]  # Kernel de Sobel para detectar bordas na direção x
        Ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]  # Kernel de Sobel para detectar bordas na direção y

        nova_imagem = Imagem.nova(self.largura, self.altura)  # Cria uma nova imagem em branco

        for x in range(self.largura):  # Loop sobre a largura da imagem
            for y in range(self.altura):  # Loop sobre a altura da imagem
                soma_x = 0  # Inicializa a soma dos gradientes na direção x
                soma_y = 0  # Inicializa a soma dos gradientes na direção y
                for i in range(-1, 2):  # Loop sobre o kernel na direção x
                    for j in range(-1, 2):  # Loop sobre o kernel na direção y
                        pixel_x = x + i  # Calcula a coordenada x do pixel atual
                        pixel_y = y + j  # Calcula a coordenada y do pixel atual
                        valor_pixel = self.get_pixel(pixel_x, pixel_y)  # Obtém o valor do pixel
                        soma_x += valor_pixel * Kx[i + 1][j + 1]  # Aplica o kernel na soma x
                        soma_y += valor_pixel * Ky[i + 1][j + 1]  # Aplica o kernel na soma y

                valor_borda = round(math.sqrt(soma_x ** 2 + soma_y ** 2))  # Calcula a magnitude do gradiente
                valor_borda = max(0, min(255, valor_borda))  # Limita o valor de borda para [0, 255]
                nova_imagem.set_pixel(x, y, valor_borda)  # Define o valor de borda na nova imagem

        return nova_imagem

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(
            getattr(self, i) == getattr(other, i)
            for i in ("altura", "largura", "pixels")
        )

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, "rb") as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith("RGB"):
                pixels = [
                    round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
                ]
            elif img.mode == "LA":
                pixels = [p[0] for p in img_data]
            elif img.mode == "L":
                pixels = list(img_data)
            else:
                raise ValueError("Modo de imagem não suportado: %r" % img.mode)
            l, a = img.size  # noqa: E741
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo="PNG"):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode="L", size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo="GIF")
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(
            toplevel, height=self.altura, width=self.largura, highlightthickness=0
        )
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode="L", size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize(
                (event.width, event.height), PILImage.NEAREST
            )
            buffer = BytesIO()
            nova_imagem.save(buffer, "GIF")
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind("<Configure>", ao_redimensionar)
        toplevel.bind(
            "<Configure>", lambda e: tela.configure(height=e.height, width=e.width)
        )

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol("WM_DELETE_WINDOW", tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def refaz_apos():
        tcl.after(500, refaz_apos)

    tcl.after(500, refaz_apos)
except:  # noqa: E722
    tk_root = None

WINDOWS_OPENED = False

if __name__ == "__main__":
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()

