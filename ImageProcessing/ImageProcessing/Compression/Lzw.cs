using System;

namespace ImageProcessing.Compression
{
	public class Lzw
	{
		private string _inputFile;

		public Lzw(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void SetInputFile(string inputFile)
		{
			_inputFile = inputFile;
		}

		public void Compress(string outputFile)
		{
			throw new NotImplementedException();
		}

		public void Decompress(string outputFile)
		{
			throw new NotImplementedException();
		}
	}
}
