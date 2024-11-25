# Photography-Raw

@since 2024-11-24

@author gustavooliveira

## Objetivo

Converter de forma automática os arquivos raw da máquina fotográfica para o formato **tiff** (por padrão).


## Requisitos

A princípio será uma aplicação docker.

Utilizando python com pillow.

* Deverá ler um ponto de montagem **source** (cartão de memória).
* Pesquisar de forma recursiva o **source** procurando pelas extensões **raw**
* Criar pasta por data (yyyy/MM/dd/{raw,converted}).
* Copiar ou mover os arquivos para **target/yyyy/MM/dd/raw**.
* Converter as imagens e colocar em **target/yyyy/MM/dd/converted**.



