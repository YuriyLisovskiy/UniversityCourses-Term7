using System;
using ImageProcessing.Tasks;

namespace ImageProcessing
{
	internal static class Program
	{
		private static void Main()
		{
			Console.WriteLine("Preparing...");
			Images.Init();
			Console.WriteLine("Done.\n");
			
			var tasks = new Task[]
			{
				new RleTask(RleTask.Bits.Bit8),
			//	new RleTask(RleTask.Bits.Bit24),
				new LzwTask(),
				new JpegTask()
			};

			foreach (var task in tasks)
			{
				task.Run();
			}
			
			var table = new TaskTable(tasks);
			table.Draw();
		}
	}
}
