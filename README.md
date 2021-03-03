# cam-calibrate

## pré requisitos
* python > 3.6
* OpenCV > 3
* numpy

## como usar o programa
1. Na pasta raiz do projeto, execute o comando abaixo:

```console
python camcalibrate.py
```

2. Sua câmera será ativada e o programa procurará pelo padrão do xadrez. 
3. Após um número razoável de matches, pressione a tecla q
4. Os dados a seguir serão computados e mostrados no log
    * matriz P
    * matriz K
    * matriz R
    * vetor de translação
    * parâmetros de distorção 
    * RMSE da reprojeção