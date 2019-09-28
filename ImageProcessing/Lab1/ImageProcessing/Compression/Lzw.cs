using System.Drawing.Imaging;

namespace ImageProcessing.Compression
{
	public class Lzw : Compressor
	{
		/*
		private string _inputFile;

		public Lzw(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void SetInputFile(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void Compress(string outputFile)
		{
			using (var image = new Bitmap(_inputFile))
			{
				var encoderInfo = Utils.GetEncoder(ImageFormat.Tiff);
                var encoder = Encoder.Compression;
                var parameters = new EncoderParameters(1)
                {
	                Param = {[0] = new EncoderParameter(encoder, (long) EncoderValue.CompressionLZW)}
                };
                image.Save(outputFile, encoderInfo, parameters);
			}
		}

		public void Decompress(string outputFile)
		{
			using (var tiffStream = File.Open(_inputFile, FileMode.Open))
			{
				var tiff = Image.FromStream(tiffStream);
				using (var image = new Bitmap(tiff))
				{
					image.Save(outputFile, Utils.GetEncoder(ImageFormat.Bmp), null);
				}
			}
		}
		*/
		public Lzw(string inputFile) : base(
			inputFile,
			ImageFormat.Tiff,
			ImageFormat.Bmp,
			EncoderValue.CompressionLZW
		)
		{
		}
	}
}
