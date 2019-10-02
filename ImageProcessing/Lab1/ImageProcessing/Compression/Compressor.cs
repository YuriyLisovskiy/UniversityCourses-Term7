using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using ImageProcessing.Tasks;
using Ut = ImageProcessing.Tasks.Utils;

namespace ImageProcessing.Compression
{
	public class Compressor
	{
		protected string InputFile;
		protected readonly ImageFormat Encoder;
		protected readonly ImageFormat Decoder;
		protected readonly EncoderValue CompressionAlgorithm;
		protected Stopwatch Stopwatch;

		public TimeResults Timing;

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
			Stopwatch = new Stopwatch();
			Timing = new TimeResults();
		}

		public void SetInputFile(string inputFile)
		{
			InputFile = inputFile;
		}

		protected virtual void Read(string inputFile)
		{
			Stopwatch.Restart();
			var f = File.Open(inputFile, FileMode.Open, FileAccess.Read);
			var buf = new byte[f.Length];
			f.Read(buf, 0, (int)f.Length);
			Stopwatch.Stop();
			f.Dispose();
			Timing.ReadingTime = Ut.TicksToMicroseconds(Stopwatch.ElapsedTicks);
		}
		
		protected virtual void Write(string outFile)
		{
			var istream = File.Open(outFile, FileMode.Open, FileAccess.Read);
			var buff = new byte[istream.Length];
			istream.Read(buff, 0, (int) istream.Length);
			
			Stopwatch.Restart();
			var ostream = File.Open(Images._tmpImage, FileMode.Create, FileAccess.Write);
			ostream.Write(buff, 0, (int) istream.Length);
			ostream.Dispose();
			Stopwatch.Stop();
			Timing.WritingTime = Ut.TicksToMicroseconds(Stopwatch.ElapsedTicks);
			
			istream.Dispose();
			File.Delete(Images._tmpImage);
		}

		public virtual void Compress(string outputFile)
		{
			Read(InputFile);
			var bitmap = new Bitmap(InputFile);
			
			Stopwatch.Restart();
			bitmap.Save(outputFile, Utils.GetEncoder(Encoder), new EncoderParameters(1)
			{
				Param = {[0] = new EncoderParameter(System.Drawing.Imaging.Encoder.Compression, (long) CompressionAlgorithm)}
			});
			Stopwatch.Stop();
			Timing.CompressionTime = Ut.TicksToMicroseconds(Stopwatch.ElapsedTicks);
			bitmap.Dispose();
			
			Write(outputFile);
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
