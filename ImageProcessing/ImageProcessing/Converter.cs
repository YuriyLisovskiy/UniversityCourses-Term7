using System.Drawing;
using System.Drawing.Imaging;
using ImageProcessing.Compression;

namespace ImageProcessing
{
	public static class Converter
	{
		public static void BitmapToTiff(string inputFile, string outputFile)
		{
		//	var encoderParameters = new EncoderParameters(1)
		//	{
		//		Param = {[0] = new EncoderParameter(Encoder.Quality, 100L)}
		//	};

			using (var image = new Bitmap(inputFile))
			{
				image.Save(outputFile, Utils.GetEncoder(ImageFormat.Tiff), null);
			}
		}
	}
}
