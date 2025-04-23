using System;
using System.IO.Pipes;
using System.Text;

public struct User
{
    public string Name;
    public string Hometown;
};

class PipeClient
{
    static void Main(string[] args)
    {
        using (NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "testpipe", PipeDirection.InOut))
        {
            Console.Write("Attempting to connect to pipe...");
            pipeClient.Connect();

            Console.WriteLine("Connected to pipe.");
            // строка не работает на линуксе
            // Console.WriteLine("There are currently {0} pipe server instances open.", pipeClient.NumberOfServerInstances);

            byte[] userDataBytes = new byte[1024];
            int bytesRead = pipeClient.Read(userDataBytes, 0, userDataBytes.Length);
            string userData = Encoding.UTF8.GetString(userDataBytes, 0, bytesRead);

            string[] userDataParts = userData.Split(',');
            User receivedUser = new User();
            receivedUser.Name = userDataParts[0];
            receivedUser.Hometown = userDataParts[1];

            Console.WriteLine("Received from server:");
            string result = string.Format("Name: {0}\nHometown: {1}", receivedUser.Name, receivedUser.Hometown);
            Console.WriteLine(result);
        }
    }
}
