namespace ImageProcessing.Compression
{
	public interface ICompressor
	{
		void SetInputFile(string inputFile);
		void Compress(string outputFile);
		void Decompress(string outputFile);
	}
}
