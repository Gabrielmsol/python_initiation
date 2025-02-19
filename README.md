# Leitor 
Fica como presente de aniversario, pra ti.   
Le esse README pelo git hub mesmo.  
Pra baixar isso vai no botão ver escrito:   
<span style="color: green"><b> <>CODE </b></span>  
Ai clica em :  
**donwload zip**.

## Install
Abre o PowerShell como adm, neste folder aqui onde voce salvou.   
Agora la escreve :

```powershell
.\install.ps1
``` 

Vai instalar o basico e dar o set up do poetry inicial.

## Explicando Poetry
Poetry é um bom manager de packages do python.  
As coisas ficam bem organizadas com ele.  

### pyproject.toml 
É o package manager, 
bem simples bem legal. 

Comandos basicos 
- Inicia um projeto
```powershell
poetry init
```
- inicia um venv
```powershell
poetry shell
```
- Instala dependencias
```powershell
poetry install
```
- Roda o app
```powershell
poetry run
```

## Organização do App

- <details>
    <summary><strong>app/</strong></summary>

    - <details>
        <summary><strong>utils/</strong></summary>

        - email_utils.py  
        - excel_utils.py  
        - openai_util.py  
        - sharepoint_utils.py  

      </details>

    - \_\_init\_\_.py  

  </details>

- <details>
    <summary><strong>static/</strong></summary>

    - **etc/**
    - **excel_files/**

  </details>


- <details>
    <summary><strong>.env.example</strong></summary>  

    Basicamente uma maneira de manter seguro seus dados
    você vai fazer uma copia dessa file, apagar tudo e deixar como `.env` apenas.   
    Poe seus dados la e é isso.  

    </details>


- <details>
  <summary><strong>install.ps1</strong></summary>

  Nosso Script para instalar voce poder ver na seção [Install](#install)
  </details>  


- <details>
  <summary><strong>pyproject.toml</strong></summary>
    Organiza seus packages
  </details>

- **README.md** 
- **run.py**   

