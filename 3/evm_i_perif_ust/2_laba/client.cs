using System;
using System.IO;
using System.IO.Pipes;
using System.Text;
using System.Windows.Forms;

class PipeClient
{
    [STAThread]
    static void Main(string[] args)
    {
        string path = "file.txt";

        using (NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "testpipe", PipeDirection.InOut))
        {
            Console.Write("Attempting to connect to pipe...");
            pipeClient.Connect();

            Console.WriteLine("Connected to pipe.");
            Console.WriteLine("There are currently {0} pipe server instances open.", pipeClient.NumberOfServerInstances);

            byte[] userDataBytes = new byte[1024];
            int bytesRead = pipeClient.Read(userDataBytes, 0, userDataBytes.Length);
            string userData = Encoding.UTF8.GetString(userDataBytes, 0, bytesRead);
            
            Clipboard.SetText(userData);
            File.WriteAllText(path, userData);
            Console.WriteLine("Received from server:");
            Console.WriteLine(userData);
        }
    }
}