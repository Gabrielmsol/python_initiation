<#
Esse script é para colocar as coisas basicas
que você precisa para executar o programa sem erros.
Le a merda do README.md se tiver duvida.
#>


$pythonInstalled = $false
$pipInstalled = $false
$pythonPath = $null

# Checa se voce tem python
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion -match "Python 3") {
        $pythonInstalled = $true
    }
} catch {
    $pythonInstalled = $false
}

if (-not $pythonInstalled) {
    $possiblePaths = @(
        "C:\Program Files\Python*",
        "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python*",
        "C:\Dev\Programs\Python\Python32" # Esse é pra mim so, pra não instalar de novo...
    )

    foreach ($path in $possiblePaths) {
        $pythonDirs = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Where-Object { $_.PSIsContainer }
        foreach ($dir in $pythonDirs) {
            if (Test-Path "$($dir.FullName)\python.exe") {
                $pythonPath = "$($dir.FullName)\python.exe"
                $pythonInstalled = $true
                break
            }
        }
        if ($pythonInstalled) { break }
    }
}

if ($pythonInstalled) {
    Write-Host "Parabens voce tem python instalado!"

    # Checa se tem pip
    try {
        $pipVersion = pip --version 2>$null
        if ($pipVersion -match "pip") {
            $pipInstalled = $true
        }
    } catch {
        $pipInstalled = $false
    }

    if (-not $pipInstalled) {
        Write-Host "Mas não tem pip, que decepção."
        Start-Process -FilePath $pythonPath -ArgumentList "-m ensurepip" -Wait
        Write-Host "Pronto, instalei"
    } else {
        Write-Host "Parabens, ai tem pip!"
    }

    # Instala poetry
    try {
        $poetryVersion = poetry --version 2>$null
        if ($poetryVersion -match "Poetry") {
            Write-Host "Caralho, tem poetry, não esperava!"
        }
    } catch {
        Write-Host "Vo instalar poetry, fica quieto ai"
        Start-Process -FilePath $pythonPath -ArgumentList "-m pip install poetry" -Wait
        Write-Host "Pronto"
    }

    # Pegando o diretorio onde você enfiou meu script 
    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location -Path $scriptDirectory

    # Instala dependencias do python
    Write-Host "Ativando a bosta do env"
    Start-Process -FilePath "poetry" -ArgumentList "config virtualenvs.in-project true" -Wait
    Start-Process -FilePath "poetry" -ArgumentList "env activate" -Wait
    Write-Host "Ativado."
    Write-Host "Instalando dependencias do python"
    Start-Process -FilePath "poetry" -ArgumentList "install" -Wait
    Write-Host "Instalado"
    Write-Host "Pronto cabo, Agora roda poetry -run app.py"

} else {
    Write-Host "Que decepção, não tem python instalado seu merda, vou instalar pra ti."

    
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $installerPath = "$env:TEMP\python_installer.exe"


    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    Remove-Item -Path $installerPath -Force

    Write-Host "Instalei o python."

    Write-Host "Colocando o pip"
    Start-Process -FilePath "$env:ProgramFiles\Python3\python.exe" -ArgumentList "-m ensurepip" -Wait
    Write-Host "Parabens agora você tem pip."

    Write-Host "Instalando poetry"
    Start-Process -FilePath "$env:ProgramFiles\Python3\python.exe" -ArgumentList "-m pip install poetry" -Wait
    Write-Host "Poetry instalado"

    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    Set-Location -Path $scriptDirectory


    Write-Host "Ativando a bosta do env"
    Start-Process -FilePath "poetry" -ArgumentList "config virtualenvs.in-project true" -Wait
    Start-Process -FilePath "poetry" -ArgumentList "env activate" -Wait
    Write-Host "Ativado."
    Write-Host "Fazendo poetry usar a merda das dependencias do meu programa."
    Start-Process -FilePath "poetry" -ArgumentList "install" -Wait
    Write-Host "Instalado"
    Write-Host "Pronto cabo, Agora roda poetry -run app.py"
}

