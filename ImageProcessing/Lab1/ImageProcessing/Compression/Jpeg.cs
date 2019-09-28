using System.Drawing;
using System.Drawing.Imaging;

namespace ImageProcessing.Compression
{
	public class Jpeg : Compressor
	{
		/*
		private string _inputFile;

		public Jpeg(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void SetInputFile(string inputFile)
		{
			_inputFile = inputFile;
		}
		*/
		
		public Jpeg(string inputFile) : base(
			inputFile,
			ImageFormat.Jpeg,
			ImageFormat.Bmp,
			EncoderValue.CompressionNone
		)
		{
		}

		public override void Compress(string outputFile)
		{
			using (var bitmap = new Bitmap(InputFile))
			{
				bitmap.Save(outputFile, Utils.GetEncoder(Encoder), new EncoderParameters(1)
				{
					Param = {[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Quality, 85L)}
				});
			}
		}

		/*
		public void Decompress(string outputFile)
		{
			using (var jpegStream = File.Open(_inputFile, FileMode.Open))
			{
				var jpeg = Image.FromStream(jpegStream);
				using (var image = new Bitmap(jpeg))
				{
					image.Save(outputFile, Utils.GetEncoder(ImageFormat.Bmp), null);
				}
			}
		}
		*/
	}
}
