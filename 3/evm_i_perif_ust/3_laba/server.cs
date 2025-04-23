using System;
using System.IO.Pipes;
using System.Text;
using System.Collections.Generic;
using System.Diagnostics;

public struct Data
{
    public string Value { get; set; }

    public Data(string value) : this()
    {
        Value = value;
    }
}

class PipeServer
{
    private static Queue<Data> ServerQueue = new Queue<Data>();
    private static NamedPipeServerStream pipeServer; // Поле для PipeServer

    static void Main()
    {
        pipeServer = new NamedPipeServerStream("testpipe", PipeDirection.InOut, 1);
        Console.WriteLine("NamedPipeServerStream object created.");
        Console.Write("Waiting for client connection...");


        //////////
        Process cmdProcess = new Process();

        cmdProcess.StartInfo.FileName = "cmd.exe";
        cmdProcess.StartInfo.Arguments = "/k client.exe";
        cmdProcess.StartInfo.UseShellExecute = true;
        cmdProcess.StartInfo.CreateNoWindow = false;
        cmdProcess.Start();

        pipeServer.WaitForConnection();

        Console.WriteLine("Client connected.");

        Console.WriteLine("Нажмите Home, если хотите начать вводить данные");
        Console.WriteLine("Нажмите Ctrl+C, если хотите прекратить вводить данные");
        Console.WriteLine("Введите exit, если хотите завершить программу");
        Console.CancelKeyPress += CtrlCFunc;

        while (true)
        {
            ConsoleKeyInfo key = Console.ReadKey();

            if (key.Key == ConsoleKey.Home)
            {
                while (true)
                {
                    Console.WriteLine("Добавьте элемент в очередь: ");
                    string input = Console.ReadLine();
                    if (input == "exit")
                    {
                        Environment.Exit(0);
                    }
                    ServerQueue.Enqueue(new Data(input));
                }
            }
            else 
            {
                Console.WriteLine("Неверно введённая клавиша");
            }
        }
    }

    public static void CtrlCFunc(object sender, ConsoleCancelEventArgs args)
    {
        Console.WriteLine("Прерывание добавления данных...");
        Console.WriteLine("Вывод элементов:");
        foreach (Data element in ServerQueue)
        {
            Console.WriteLine(element.Value);
        }

        string DataString = "";

        foreach (Data element in ServerQueue)
        {
            DataString += element.Value + "\n";
        }

        byte[] userDataBytes = Encoding.UTF8.GetBytes(DataString);
        pipeServer.Write(userDataBytes, 0, userDataBytes.Length);
        pipeServer.Flush();

        Console.WriteLine("User data sent to client!");
        args.Cancel = true;
        Environment.Exit(0);
    }
}
