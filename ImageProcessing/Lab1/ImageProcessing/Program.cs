using System;
using ImageProcessing.Compression;
using ImageProcessing.Tasks;

namespace ImageProcessing
{
	internal static class Program
	{
		private static void Compression()
		{
			var tasks = new[]
			{
				new Task(
					"RLE",
					Images._inImage8Bit,
					Images._c8BitImageRle,
					Images._d8BitImageRle,
					new Rle(Images._inImage8Bit)
				),
				new Task(
					"LZW",
					Images._inImage24Bit,
					Images._cImageTiffLzw,
					Images._dImageTiffLzw,
					new Lzw(Images._inImage24Bit)
				),
				new Task(
					"JPEG",
					Images._inImage24Bit,
					Images._cImageJpeg,
					Images._dImageJpeg,
					new Jpeg(Images._inImage24Bit)
				)
			};

			foreach (var task in tasks)
			{
				task.Run();
			}
			
			var table = new TaskTable(tasks);
			table.Draw();
		}

		private static void PixelDifferences()
		{
			DifferenceTask.CreateDifference(
				Images._inImage24Bit,
				Images._cImageJpeg,
				Images._diffJpegBmpAll,
				Images._diffJpegBmpR,
				Images._diffJpegBmpG,
				Images._diffJpegBmpB,
				false
			);
		}
		
		private static void Main()
		{
			Console.WriteLine("Preparing...");
			Images.Init();
			Console.WriteLine("Done.\n");
			
			Compression();
			Console.WriteLine();
		
			PixelDifferences();
		}
	}
}
