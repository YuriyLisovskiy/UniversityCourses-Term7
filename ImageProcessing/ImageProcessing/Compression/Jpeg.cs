using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace ImageProcessing.Compression
{
	public class Jpeg : ICompressor
	{
		private string _inputFile;

		public Jpeg(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void SetInputFile(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void Compress(string outputFile)
		{
			var encoderParameters = new EncoderParameters(1)
			{
				Param = {[0] = new EncoderParameter(Encoder.Quality, 100L)}
			};

			using (var image = new Bitmap(_inputFile))
			{
				image.Save(outputFile, Utils.GetEncoder(ImageFormat.Jpeg), encoderParameters);
			}
		}

		public void Decompress(string outputFile)
		{
			using (var bmpStream = File.Open(_inputFile, FileMode.Open))
			{
				var jpeg = Image.FromStream(bmpStream);
				using (var image = new Bitmap(jpeg))
				{
					image.Save(outputFile, Utils.GetEncoder(ImageFormat.Bmp), null);
				}
			}
		}
	}
}
