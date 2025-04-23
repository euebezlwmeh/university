using System;
using System.IO.Pipes;
using System.Text;

public struct User
{
    public string Name;
    public string Hometown;
}

class PipeServer
{
    static void Main()
    {
        using (NamedPipeServerStream pipeServer = new NamedPipeServerStream("testpipe", PipeDirection.InOut, 1))
        {
            Console.WriteLine("NamedPipeServerStream object created.");
            Console.Write("Waiting for client connection...");
            pipeServer.WaitForConnection();

            Console.WriteLine("Client connected.");

            User newUser = new User();

            Console.WriteLine("Enter name: ");
            newUser.Name = Console.ReadLine();

            Console.WriteLine("Enter hometown: ");
            newUser.Hometown = Console.ReadLine();
            

            byte[] userDataBytes = Encoding.UTF8.GetBytes(newUser.Name + "," + newUser.Hometown);
            pipeServer.Write(userDataBytes, 0, userDataBytes.Length);
            pipeServer.Flush();

            Console.WriteLine("User data sent to client:");
            string result = string.Format("Name: {0}, Hometown: {1}", newUser.Name, newUser.Hometown);
            Console.WriteLine(result);
        }
    }
}
