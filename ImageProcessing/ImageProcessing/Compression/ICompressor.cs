namespace ImageProcessing.Compression
{
	public interface ICompressor
	{
		void Compress(string outputFile);
		void Decompress(string outputFile);
	}
}
