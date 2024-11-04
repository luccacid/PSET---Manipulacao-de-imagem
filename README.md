# Projeto de Processamento de Imagens

## Descrição

Este projeto implementa uma classe `Imagem` para manipulação básica de imagens em tons de cinza. A classe permite a aplicação de diversos efeitos de processamento, como inversão de cores, desfoque, foco e detecção de bordas.

## Funcionalidades

A classe `Imagem` fornece as seguintes funcionalidades:

- **Carregamento de Imagem**: Carrega uma imagem de um arquivo e converte para tons de cinza.
- **Exibição de Imagem**: Mostra a imagem em uma nova janela usando Tkinter.
- **Efeitos de Processamento**:
  - `invertida()`: Inverte as cores da imagem.
  - `borrada(n)`: Aplica um desfoque à imagem usando um kernel de tamanho `n`.
  - `focada(n)`: Aplica um efeito de foco à imagem, utilizando um kernel de desfoque de tamanho `n`.
  - `bordas()`: Detecta bordas na imagem usando o operador de Sobel.

## Instalação

Para utilizar este projeto, é necessário ter o Python 3 e as bibliotecas `PIL` (Pillow) e `tkinter` instaladas. Você pode instalar a biblioteca Pillow usando o pip:

```bash
pip install Pillow
```

## Uso

1. **Carregar uma imagem**:
   ```python
   imagem = Imagem.carregar('caminho/para/sua/imagem.png')
   ```

2. **Aplicar um efeito**:
   ```python
   imagem_borrada = imagem.borrada(5)
   imagem_borrada.mostrar()  # Mostra a imagem borrada
   ```

3. **Salvar a imagem processada**:
   ```python
   imagem_borrada.salvar('caminho/para/salvar/imagem_borrada.png')
   ```

## Exemplo

No bloco de código `if __name__ == "__main__":`, você pode adicionar testes ou experimentações com a classe `Imagem`. Por exemplo:

```python
if __name__ == "__main__":
    # Carrega uma imagem
    img = Imagem.carregar('caminho/para/sua/imagem.png')
    
    # Aplica efeitos
    img_invertida = img.invertida()
    img_borrada = img.borrada(5)
    img_bordas = img.bordas()
    
    # Mostra as imagens processadas
    img_invertida.mostrar()
    img_borrada.mostrar()
    img_bordas.mostrar()
```
