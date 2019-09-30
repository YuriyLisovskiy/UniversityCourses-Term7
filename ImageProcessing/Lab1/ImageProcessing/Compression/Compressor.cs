using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace ImageProcessing.Compression
{
	public class Compressor
	{
		protected string InputFile;
		protected readonly ImageFormat Encoder;
		protected readonly ImageFormat Decoder;
		protected readonly EncoderValue CompressionAlgorithm;

		protected Compressor(
			string inputFile,
			ImageFormat encoder,
			ImageFormat decoder,
			EncoderValue compressionAlgorithm
		)
		{
			InputFile = inputFile;
			Encoder = encoder;
			Decoder = decoder;
			CompressionAlgorithm = compressionAlgorithm;
		}

		public void SetInputFile(string inputFile)
		{
			InputFile = inputFile;
		}

		public virtual void Compress(string outputFile)
		{
			using (var bitmap = new Bitmap(InputFile))
			{
				bitmap.Save(outputFile, Utils.GetEncoder(Encoder), new EncoderParameters(1)
				{
					Param = {[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Compression, (long) CompressionAlgorithm)}
				});
			}
		}

		public virtual void Decompress(string outputFile)
		{
			using (var stream = File.Open(InputFile, FileMode.Open))
			{
				using (var image = Image.FromStream(stream))
				{
					image.Save(outputFile, Utils.GetEncoder(Decoder), null);	
				}
			}
		}
	}
}
