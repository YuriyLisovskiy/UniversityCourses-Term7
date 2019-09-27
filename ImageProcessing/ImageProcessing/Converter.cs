using System.Drawing;
using System.Drawing.Imaging;
using ImageProcessing.Compression;

namespace ImageProcessing
{
	public static class Converter
	{
		public static void BitmapToTiff(string inputFile, string outputFile)
		{
			using (var image = new Bitmap(inputFile))
			{
				image.Save(outputFile, Utils.GetEncoder(ImageFormat.Tiff), null);
			}
		}
	}
}
