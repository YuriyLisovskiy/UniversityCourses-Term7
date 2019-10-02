using System;
using System.Diagnostics;
using System.IO;

namespace ImageProcessing.Tasks
{
	public static class Utils
	{
		public static long TicksToMicroseconds(long ticks)
		{
			return ticks / 1000;
		}
		
		public static long MeasureInMicroseconds(Action action)
		{
			var stopwatch = new Stopwatch();
			stopwatch.Start();
			action();
			stopwatch.Stop();
			return TicksToMicroseconds(stopwatch.ElapsedTicks);
		}

		public static long GetFileSizeInBytes(string path)
		{
			return new FileInfo(path).Length;
		}
	}
}
