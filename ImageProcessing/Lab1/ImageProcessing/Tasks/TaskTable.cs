using System;
using System.Collections.Generic;
using System.Linq;

namespace ImageProcessing.Tasks
{
	public class TaskTable
	{
		private readonly IEnumerable<Task> _tasks;
		private const ushort RawLength = 7;
		
		public TaskTable(IEnumerable<Task> tasks)
		{
			_tasks = tasks;
		}

		public void Draw()
		{
			DrawInfo(new []{"Назва методу", "Час кодування,", "Час декодування,", "Час читання,", "Час запису,", "Розмір,", "Різниця з"});
			DrawInfo(new []{"стиснення", "мікросекунд", "мікросекунд", "мікросекунд", "мікросекунд", "байтів", "оригіналом, байтів"});
			DrawLine();
			DrawInfo(new []{"Без стиснення (8)", null, null, null, null, $"{Utils.GetFileSizeInBytes(Images._inImage8Bit),-10:0,0}", null});
			DrawLine();
			DrawInfo(new []{"Без стиснення (24)", null, null, null, null, $"{Utils.GetFileSizeInBytes(Images._inImage24Bit),-10:0,0}", null});
			foreach (var task in _tasks)
			{
				DrawLine();
				DrawInfo(task.GetResult().ToArray());
			}
		}

		private static void DrawLine()
		{
			var array = new[]
			{
				"--------------------",
				"----------------",
				"------------------",
				"--------------",
				"--------------",
				"-----------",
				"--------------------"
			};
			DrawRaw(array, "|", "|", "+");
		}

		private static void DrawInfo(IReadOnlyList<object> array)
		{
			DrawRaw(array, "| ", "|", "| ");
		}
		
		private static void DrawRaw(IReadOnlyList<object> array, string begin, string end, string sep)
		{
			if (array.Count != RawLength)
			{
				throw new ArgumentException($"Invalid column length: {RawLength} is required, {array.Count} was given");
			}
			
			Console.WriteLine($"{begin}{array[0] ?? "—",-19}{sep}{array[1] ?? "—",-15}{sep}{array[2] ?? "—",-17}{sep}{array[3] ?? "—",-13}{sep}{array[4] ?? "—",-13}{sep}{array[5] ?? "—",-10:0,0}{sep}{array[6] ?? "—",-19:0,0}{end}");
		}
	}
}
