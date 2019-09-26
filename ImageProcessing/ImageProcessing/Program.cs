using System;
using System.IO;
using ImageProcessing.Compression;

namespace ImageProcessing
{
	internal static class Program
	{
		private const string InputImage8bit = "images_5_8bit.bmp";
		private const string InputImage24bit = "images_5.bmp";
		
		private const string OutputImageRle8Bit = "images_5_8bit_rle.bmp";
		private const string OutputImageJpeg = "images_5_se.jpeg";
		
		private static string _getRootDirectory()
		{
			return Path.GetDirectoryName(
				       Path.GetDirectoryName(
					       Path.GetDirectoryName(Directory.GetCurrentDirectory()
					)
				)
			);
		}

		private static void _prepare(string outputDirectory)
		{
			if (!Directory.Exists(outputDirectory))
			{
				Directory.CreateDirectory(outputDirectory);
			}
		}
		
		private static void Main()
		{
			Console.WriteLine("Converting...");
			
			var rootDirectory = _getRootDirectory();
			var inputDirectory = rootDirectory + "/Input/";
			var outputDirectory = rootDirectory + "/Output/";
			
			_prepare(outputDirectory);

		//	var rle = new Rle(inputDirectory + InputImage8bit);
		//	rle.Compress(outputDirectory + OutputImageRle8Bit);
		
		//	var rle = new Rle(outputDirectory + OutputImageRle8Bit);
		//	rle.Decompress(outputDirectory + InputImage8bit);
		
			var jpeg = new Jpeg(inputDirectory + InputImage24bit);
			jpeg.Compress(outputDirectory + OutputImageJpeg);
			
			Console.WriteLine("Done.");
		}
	}
}
