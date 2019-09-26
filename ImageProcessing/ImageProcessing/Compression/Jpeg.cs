using System;
using System.Drawing;
using System.Drawing.Imaging;

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
			throw new NotImplementedException();
		}
	}
}
