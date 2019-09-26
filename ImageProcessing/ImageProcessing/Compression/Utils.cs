using System.Drawing.Imaging;
using System.Linq;

namespace ImageProcessing.Compression
{
	public class Utils
	{
		public static ImageCodecInfo GetEncoder(ImageFormat format)
		{
			var codecs = ImageCodecInfo.GetImageDecoders();
			return codecs.FirstOrDefault(codec => codec.FormatID == format.Guid);
		}
	}
}
