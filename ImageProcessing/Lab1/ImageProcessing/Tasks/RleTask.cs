using System.Data;
using ImageProcessing.Compression;

namespace ImageProcessing.Tasks
{
	public class RleTask : Task
	{
		public enum Bits
		{
			Bit8, Bit24
		}

		private readonly Bits _bits;

		public RleTask(Bits bits) : base("")
		{
			switch (bits)
			{
				case Bits.Bit8:
					Name = "RLE (8-bit)";
					break;
				case Bits.Bit24:
					Name = "RLE (24-bit)";
					break;
				default:
					throw new ConstraintException($"invalid bits: {bits}");
			}
			_bits = bits;
		}

		protected override void CompressionTask()
		{
			string inImg, outImg;
			if (_bits == Bits.Bit8)
			{
				inImg = Images._inImage8Bit;
				outImg = Images._c8BitImageRle;
			}
			else
			{
				inImg = Images._inImage24Bit;
				outImg = Images._c24BitImageRle;
			}
			
			var rle = new Rle(inImg);
			rle.Compress(outImg);
		}

		protected override void DecompressionTask()
		{
			string inImg, outImg;
			if (_bits == Bits.Bit8)
			{
				inImg = Images._c8BitImageRle;
				outImg = Images._d8BitImageRle;
			}
			else
			{
				inImg = Images._c24BitImageRle;
				outImg = Images._d24BitImageRle;
			}
			
			var rle = new Rle(inImg);
			rle.Decompress(outImg);
		}

		protected override long CompressedFileSize()
		{
			return Utils.GetFileSizeInBytes(_bits == Bits.Bit8 ? Images._c8BitImageRle : Images._c24BitImageRle);
		}

		protected override long OriginalFileSize()
		{
			return Utils.GetFileSizeInBytes(_bits == Bits.Bit8 ? Images._inImage8Bit : Images._inImage24Bit);
		}
	}
}
