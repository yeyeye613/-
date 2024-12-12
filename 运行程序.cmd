if exist ".\venv\Scripts\activate.bat" (
    .\venv\Scripts\activate.bat
    echo  已经激活虚拟环境
    .\venv\Scripts\python.exe .\OpenWeb.py
)
) else (
    echo 未创建虚拟环境，回车创建
    pause
    echo 创建
    python -m venv venv
    echo 激活
    .\venv\Scripts\activate.bat
    python OpenWeb.py
)
