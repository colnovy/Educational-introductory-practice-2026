Программа на Python для поиска корней нелинейных уравнений методами бисекции, Ньютона и секущих. 
Включает пошаговый вывод итераций, сравнение скорости сходимости и визуализацию результатов.

- Установить Docker (Доступ: https://www.docker.com/products/docker-desktop/).
- После установки запустить Docker Desktop.

Открыть терминал (PowerShell, CMD или Terminal) в папке с файлом `equation-solver.tar` и выполнить:

docker load -i equation-solver.tar
docker run -it --rm -v $(pwd)/output:/app/output equation-solver
