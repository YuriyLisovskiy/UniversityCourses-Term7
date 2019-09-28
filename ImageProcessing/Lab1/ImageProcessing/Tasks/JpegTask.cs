using ImageProcessing.Compression;

namespace ImageProcessing.Tasks
{
	public class JpegTask : Task
	{
		public JpegTask() : base("JPEG")
		{
		}

		protected override void CompressionTask()
		{
			var jpeg = new Jpeg(Images._inImage24Bit);
			jpeg.Compress(Images._cImageJpeg);
		}

		protected override void DecompressionTask()
		{
			var jpeg = new Jpeg(Images._cImageJpeg);
			jpeg.Decompress(Images._dImageJpeg);
		}

		protected override long CompressedFileSize()
		{
			return Utils.GetFileSizeInBytes(Images._cImageJpeg);
		}

		protected override long OriginalFileSize()
		{
			return Utils.GetFileSizeInBytes(Images._inImage24Bit);
		}
	}
}
