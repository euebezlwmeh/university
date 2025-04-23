# Лабораторная работа №2
Дополнить первое консольное приложение (сервер) разрабатываемое в лабораторной работе №1 очередью с данными на отправку. Добавление данных для отправки в очередь должно происходить до тех пор, пока не будет нажата комбинация клавиш Ctrl+C. Также при добавлении данных в очередь должен учитываться приоритет отправляемых данных. Полученные обратно от второго консольного приложения (клиент) данные должны сохраняться в буфер, который будет записываться в файл или выводиться на экран после нажатия комбинации клавиш Ctrl+C. В процессе разработки приложений потребуется воспользоваться некоторыми из следующих классов:
1. [Task](https://learn.microsoft.com/ru-ru/dotnet/api/system.threading.tasks.task?view=net-7.0)
2. [Thread](https://learn.microsoft.com/ru-ru/dotnet/api/system.threading.thread?view=net-7.0)
3. [ThreadPool](https://learn.microsoft.com/ru-ru/dotnet/api/system.threading.threadpool?view=net-7.0)
4. [Асинхронное программирование на основе Task](https://learn.microsoft.com/ru-ru/dotnet/standard/parallel-programming/task-based-asynchronous-programming)
5. [CancellationToken](https://learn.microsoft.com/ru-ru/dotnet/api/system.threading.cancellationtoken?view=net-7.0)
6. [CancellationTokenSource](https://learn.microsoft.com/ru-ru/dotnet/api/system.threading.cancellationtokensource?view=net-7.0)
7. [Queue](https://learn.microsoft.com/ru-ru/dotnet/api/system.collections.generic.queue-1?view=net-7.0)
8. [PriorityQueue](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.priorityqueue-2?view=net-7.0)
