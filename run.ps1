<#
.SYNOPSIS
启动机器人MCP服务

.DESCRIPTION
启动主服务并检查依赖是否安装
#>

# 检查虚拟环境
if (-not (Test-Path .venv)) {
    Write-Host "正在创建虚拟环境..."
    python -m venv .venv
}

# 激活虚拟环境
.\.venv\Scripts\activate

# 检查依赖
if (-not (Test-Path requirements.txt)) {
    Write-Host "找不到requirements.txt"
    exit 1
}

pip install -r requirements.txt

# 启动服务
Write-Host "启动机器人MCP服务..."
python -m src.main