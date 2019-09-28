using ImageProcessing.Compression;

namespace ImageProcessing.Tasks
{
	public class LzwTask : Task
	{
		public LzwTask() : base("LZW")
		{
		}

		protected override void CompressionTask()
		{
			var lzw = new Lzw(Images._inImage24Bit);
			lzw.Compress(Images._cImageTiffLzw);
		}

		protected override void DecompressionTask()
		{
			var lzw = new Lzw(Images._cImageTiffLzw);
			lzw.Decompress(Images._dImageTiffLzw);
		}

		protected override long CompressedFileSize()
		{
			return Utils.GetFileSizeInBytes(Images._cImageTiffLzw);
		}

		protected override long OriginalFileSize()
		{
			return Utils.GetFileSizeInBytes(Images._inImage24Bit);
		}
	}
}
