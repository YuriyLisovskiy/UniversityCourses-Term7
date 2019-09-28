using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace ImageProcessing.Compression
{
	public class Compressor : ICompressor
	{
		protected string _inputFile;
		protected readonly ImageFormat _encoder;
		protected readonly ImageFormat _decoder;
		protected readonly EncoderValue _compressionAlgorithm;

		protected Compressor(
			string inputFile,
			ImageFormat encoder,
			ImageFormat decoder,
			EncoderValue compressionAlgorithm
		)
		{
			_inputFile = inputFile;
			_encoder = encoder;
			_decoder = decoder;
			_compressionAlgorithm = compressionAlgorithm;
		}

		public void SetInputFile(string inputFile)
		{
			_inputFile = inputFile;
		}

		public virtual void Compress(string outputFile)
		{
			using (var bitmap = new Bitmap(_inputFile))
			{
				bitmap.Save(outputFile, Utils.GetEncoder(_encoder), new EncoderParameters(1)
				{
					Param = {[0] = new EncoderParameter(Encoder.Compression, (long) _compressionAlgorithm)}
				});
			}
		}

		public virtual void Decompress(string outputFile)
		{
			using (var stream = File.Open(_inputFile, FileMode.Open))
			{
				using (var image = Image.FromStream(stream))
				{
					image.Save(outputFile, Utils.GetEncoder(_decoder), null);	
				}
			}
		}
	}
}
