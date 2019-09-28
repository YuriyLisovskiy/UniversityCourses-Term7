using System.IO;

namespace ImageProcessing.Tasks
{
	public static class Images
	{
		public static string _inImage8Bit;
		public static string _inImage24Bit;
		
		public static string _cImageTiffLzw;
		public static string _dImageTiffLzw;
		
		public static string _c8BitImageRle;
		public static string _d8BitImageRle;
		
		public static string _c24BitImageRle;
		public static string _d24BitImageRle;
		
		public static string _cImageJpeg;
		public static string _dImageJpeg;

		public static void Init()
		{
			var rootDir = _getRootDirectory();
			
			var inputDir = rootDir + "/Input/";
			if (!Directory.Exists(inputDir))
			{
				throw new DirectoryNotFoundException($"Directory does not exist: {inputDir}");
			}
			
			var outDir = rootDir + "/Output/";
			var compressedDir = outDir + "Compressed/";
			var decompressedDir = outDir + "Decompressed/";

			const string imageName = "images_5";
			
			_inImage8Bit = inputDir + $"8bit_{imageName}.bmp";
			_inImage24Bit = inputDir + $"24bit_{imageName}.bmp";
			if (!File.Exists(_inImage8Bit))
			{
				throw new FileNotFoundException($"File does not exist: {_inImage8Bit}");
			}
			
			if (!File.Exists(_inImage24Bit))
			{
				throw new FileNotFoundException($"File does not exist: {_inImage24Bit}");
			}
			
			_cImageTiffLzw = compressedDir + $"lzw_encoded_{imageName}.tiff";
			_dImageTiffLzw = decompressedDir + $"lzw_decoded_{imageName}.bmp";
			
			_c8BitImageRle = compressedDir + $"rle_encoded_8bit_{imageName}.bmp";
			_d8BitImageRle = decompressedDir + $"rle_decoded_8bit_{imageName}.bmp";
			
			_c24BitImageRle = compressedDir + $"rle_encoded_24bit_{imageName}.bmp";
			_d24BitImageRle = decompressedDir + $"rle_decoded_24bit_{imageName}.bmp";
			
			_cImageJpeg = compressedDir + $"jpeg_encoded_{imageName}.jpeg";
			_dImageJpeg = decompressedDir + $"jpeg_decoded_{imageName}.bmp";
			
			_createDir(compressedDir);
			_createDir(decompressedDir);
		}
		
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
	}
}
