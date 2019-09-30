using System.Drawing.Imaging;

namespace ImageProcessing.Compression
{
	public class Lzw : Compressor
	{
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
