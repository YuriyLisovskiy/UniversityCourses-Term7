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

		public static string _cImageJpeg;
		public static string _dImageJpeg;

		public static string _diffJpegBmpAll;
		public static string _diffJpegBmpAllInv;
		
		public static string _diffJpegBmpR;
		public static string _diffJpegBmpRInv;
		
		public static string _diffJpegBmpG;
		public static string _diffJpegBmpGInv;
		
		public static string _diffJpegBmpB;
		public static string _diffJpegBmpBInv;

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
			var differencesDir = outDir + "Differences/";

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

			_cImageJpeg = compressedDir + $"jpeg_encoded_{imageName}.jpeg";
			_dImageJpeg = decompressedDir + $"jpeg_decoded_{imageName}.bmp";

			_diffJpegBmpAll = differencesDir + "diff_jpeg_bmp.bmp";
			_diffJpegBmpAllInv = differencesDir + "inv_diff_jpeg_bmp.bmp";
			
			_diffJpegBmpR = differencesDir + "diff_jpeg_bmp_r.bmp";
			_diffJpegBmpRInv = differencesDir + "inv_diff_jpeg_bmp_r.bmp";
			
			_diffJpegBmpG = differencesDir + "diff_jpeg_bmp_g.bmp";
			_diffJpegBmpGInv = differencesDir + "inv_diff_jpeg_bmp_g.bmp";
			
			_diffJpegBmpB = differencesDir + "diff_jpeg_bmp_b.bmp";
			_diffJpegBmpBInv = differencesDir + "inv_diff_jpeg_bmp_b.bmp";
			
			_createDir(compressedDir);
			_createDir(decompressedDir);
			_createDir(differencesDir);
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
