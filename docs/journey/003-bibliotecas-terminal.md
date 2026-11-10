# Uso de bibliotecas para estilizaçã, emoji e menus

Decidi desde o inicio usar bibliotecas para deixar o terminal agradável para não ter que estruturar isso depois por conta do tempo.

Vou usar:

- InquirerPy - ele substitui os inputs tradicionais por elementos visuais navegaveis
- rich - pra deixar o terminal mais apersentavel, ele usa esilos CSS-like
- emoji - pra ter compatiblidade com emiojis que eu usar

usei essas versões no requirements.txt
```txt
InquirerPy>=0.3.4
rich>=13.0.0
emoji>=2.10.0
```

e isntalei.

## InquirerPy
Pra usar ele eu importo o inquirer e o Choice, ao invés do input eu uso um metodo de inquirer que tem essa assinatura
```python
inquirer.select(
    message,
    choices:[Choice(value, name),default]
).execute()
```

vai aparecer a **message** pro user e ele vai ter uma lista de **choices**, cada **Choice** vai ter um **value** que será retornado e um **name** pro user saber o que escolher.

Como sse vai ser o mais usado decidi documentar ele, mas vi na documentação da biblioteca que tem **textarea**, **checkbox** e até **confirm** qu posso acabar usando também

## Rich

Pra usar ele eu tenho que importar um **Console** e um **Panel**, eu atribuo o COnsole a uma variavel e pra usar é só chamar ela e o print, como se usasse normal, da inclusive pra usar o print com f, formatado, só que neles eu posso colocar essas classes usando `[estilo]texto estilizado[/estilo]` (que ganha um escape com \[ e \]) ou usar um parametro `style` (que parece ser melhor para separar os estilos, a não ser que eles sejam para apenas um trecho), e colocando classes neles, como **bold** ou **yellow**, vou estar desenvolvendo com a ajuda da documentação dele também.

O Panel é pra desenhar um quadrado em volta do texto, eles podem ter `title` e `subtitle`, se chamado sem .fit() ele via esxtender pra toda a tela, ele também tem border_style que permite mudar o estilo da borda, e é bom que dá pra adicionar vários blocos de texto um depois do outro

Além disso posso acabar usando o Table (para tabelas) e o ask, que é um input simples.

Se uma estilização for muito repetitiva eu vi que tem como criar classes de estilo guardando em variaveis.

Estilos: https://rich.readthedocs.io/en/latest/style.html