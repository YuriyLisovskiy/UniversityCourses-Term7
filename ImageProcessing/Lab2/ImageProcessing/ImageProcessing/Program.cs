using System.IO;

namespace ImageProcessing
{
	internal static class Program
	{
		private static string _imagePath;
		private static string _histogramPath;

		private static string GetProjectPath()
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

		private static void Init()
		{
			var root = GetProjectPath() + "/";
			var input = root + "Input/";
			if (!Directory.Exists(input))
			{
				throw new DirectoryNotFoundException($"Directory \"{input}\" does not exist");
			}
			
			var output = root + "Output/";
			_createDir(output);

			const string imageName = "image_1";
			
			_imagePath = input + $"{imageName}.bmp";
			_histogramPath = output + "image_histogram.txt";
		}
		
		private static void Main()
		{
			Init();
			
			var his = new Histogram(_imagePath);
			his.Calc();
			his.Write(_histogramPath);
		}
	}
}
