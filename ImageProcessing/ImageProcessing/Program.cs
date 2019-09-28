using System;
using System.IO;
using ImageProcessing.Compression;

namespace ImageProcessing
{
	internal static class Program
	{
		private static string _inImage8Bit;
		private static string _inImage24Bit;
		
		private static string _cImageTiffLzw;
		private static string _dImageTiffLzw;
		
		private static string _c8BitImageRle;
		private static string _d8BitImageRle;
		
		private static string _cImageJpeg;
		private static string _dImageJpeg;

		private static string _getRootDirectory()
		{
			return Path.GetDirectoryName(
				       Path.GetDirectoryName(
					       Path.GetDirectoryName(Directory.GetCurrentDirectory()
					)
				)
			);
		}

		private static void _createDir(string dir)
		{
			if (!Directory.Exists(dir))
			{
				Directory.CreateDirectory(dir);
			}
		}

		private static void _prepare()
		{
			var rootDir = _getRootDirectory();
			
			var inputDir = rootDir + "/Input/";
			var outDir = rootDir + "/Output/";
			var compressedDir = outDir + "Compressed/";
			var decompressedDir = outDir + "Decompressed/";

			const string imageName = "images_5";
			
			_inImage8Bit = inputDir + $"8bit_{imageName}.bmp";
			_inImage24Bit = inputDir + $"24bit_{imageName}.bmp";
			
			_cImageTiffLzw = compressedDir + $"lzw_encoded_{imageName}.tiff";
			_dImageTiffLzw = decompressedDir + $"lzw_decoded_{imageName}.bmp";
			
			_c8BitImageRle = compressedDir + $"rle_encoded_8bit_{imageName}.bmp";
			_d8BitImageRle = decompressedDir + $"rle_decoded_8bit_{imageName}.bmp";
			
			_cImageJpeg = compressedDir + $"jpeg_encoded_{imageName}.jpeg";
			_dImageJpeg = decompressedDir + $"jpeg_decoded_{imageName}.bmp";
			
			_createDir(compressedDir);
			_createDir(decompressedDir);
		}
		
		private static void _rleTask()
		{
			var rle = new Rle(_inImage8Bit);
			rle.Compress(_c8BitImageRle);
		
			rle.SetInputFile(_c8BitImageRle);
			rle.Decompress(_d8BitImageRle);
		}

		private static void _lzwTask()
		{
			var lzw = new Lzw(_inImage24Bit);
			lzw.Compress(_cImageTiffLzw);
			
			lzw.SetInputFile(_cImageTiffLzw);
			lzw.Decompress(_dImageTiffLzw);
		}

		private static void _jpegTask()
		{
			var jpeg = new Jpeg(_inImage24Bit);
			jpeg.Compress(_cImageJpeg);
			
			jpeg.SetInputFile(_cImageJpeg);
			jpeg.Decompress(_dImageJpeg);
		}

		private static void Main()
		{
			Console.WriteLine("Preparing...");
			
			_prepare();

			Console.WriteLine("Rle task running...");
			_rleTask();
			
			Console.WriteLine("Lzw task running...");
			_lzwTask();
			
			Console.WriteLine("Jpeg task running...");
			_jpegTask();

			Console.WriteLine("Done.");
		}
	}
}
