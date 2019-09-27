using System;
using System.IO;
using ImageProcessing.Compression;

namespace ImageProcessing
{
	internal static class Program
	{
		private static string Image8bit;
		private static string Image24bit;
		private static string ImageTiff;

		private static string ImageRle8Bit;
		private static string ImageDecoded8bit;
		private static string ImageJpeg;
		private static string ImageJpegDecoded;
		private static string ImageTiffLzw;
		private static string ImageTiffLzwDecoded;

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

		private static void Prepare()
		{
			var rootDirectory = _getRootDirectory();
			var inputDirectory = rootDirectory + "/Input/";
			var outputDirectory = rootDirectory + "/Output/";

			Image8bit = inputDirectory + "images_5_8bit.bmp";
			Image24bit = inputDirectory + "images_5.bmp";
			ImageTiff = inputDirectory + "images_5.tiff";

			ImageTiffLzw = outputDirectory + "images_5_lzw.tiff";
			ImageTiffLzwDecoded = outputDirectory + "images_5_decoded.tiff";
			ImageDecoded8bit = outputDirectory + "images_5_8bit_decoded.bmp";
			ImageRle8Bit = outputDirectory + "images_5_8bit_rle.bmp";
			ImageJpeg = outputDirectory + "images_5_se.jpeg";
			ImageJpegDecoded = outputDirectory + "images_5_jpeg_decoded.bmp";
			
			_prepare(outputDirectory);
		}
		
		private static void RleTask()
		{
			var rle = new Rle(Image8bit);
			rle.Compress(ImageRle8Bit);
		
			rle.SetInputFile(ImageRle8Bit);
			rle.Decompress(ImageDecoded8bit);
		}

		private static void LzwTask()
		{
			Converter.BitmapToTiff(Image24bit, ImageTiff);
		}

		private static void JpegTask()
		{
			var jpeg = new Jpeg(Image24bit);
			jpeg.Compress(ImageJpeg);
			
			jpeg.SetInputFile(ImageJpeg);
			jpeg.Decompress(ImageJpegDecoded);
		}

		private static void Main()
		{
			Console.WriteLine("Doing stuff...");
			
			Prepare();

			RleTask();
			LzwTask();
			JpegTask();

			Console.WriteLine("Done.");
		}
	}
}
