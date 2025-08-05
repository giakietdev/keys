@echo off
chcp 65001 >nul
title API Key Manager

echo.
echo ========================================
echo    🔑 API KEY MANAGER
echo ========================================
echo.

if "%1"=="" (
    echo Sử dụng:
    echo   run.bat menu          - Chạy menu tương tác
    echo   run.bat add -f avatar - Thêm key vào folder avatar
    echo   run.bat list -f avatar - Xem keys trong folder avatar
    echo   run.bat auto -c 5     - Tạo 5 keys cho tất cả folders
    echo   run.bat push          - Đẩy lên GitHub
    echo   run.bat sync          - Đồng bộ với remote repository
    echo   run.bat backup        - Tạo backup keys
    echo   run.bat restore -f backup.json - Khôi phục từ backup
    echo.
    echo Ví dụ:
    echo   run.bat menu
    echo   run.bat add -f avatar -k mykey123
    echo   run.bat auto -c 3
    echo   run.bat sync
    echo   run.bat backup
    echo.
    pause
    exit /b
)

python run.py %*

if errorlevel 1 (
    echo.
    echo ❌ Có lỗi xảy ra!
    echo Kiểm tra:
    echo - Python đã được cài đặt chưa?
    echo - Git đã được cài đặt chưa?
    echo - Repository đã được khởi tạo chưa?
    echo - Kết nối internet có ổn không?
    echo.
    pause
) 