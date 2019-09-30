using System.Drawing;
using System.Drawing.Imaging;

namespace ImageProcessing.Compression
{
	public class Jpeg : Compressor
	{
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
	}
}
