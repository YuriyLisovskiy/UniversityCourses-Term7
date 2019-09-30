using System;
using System.Collections.Generic;
using ImageProcessing.Compression;

namespace ImageProcessing.Tasks
{
	public class Task
	{
		private readonly string _name;
		private long _compressionTime;
		private long _decompressionTime;
		private long _compressedFileSize;
		private long _originalFileSize;

		private readonly string _original;
		private readonly string _outCompressed;
		private readonly string _outDecompressed;
		private readonly Compressor _algorithm;
		
		public Task(string name, string original, string outCompressed, string outDecompressed, Compressor algorithm)
		{
			_name = name;
			_original = original;
			_outCompressed = outCompressed;
			_outDecompressed = outDecompressed;
			_algorithm = algorithm;
		}
		
		public void Run()
		{
			Console.WriteLine($"{_name} task running...");
			_compressionTime = Utils.MeasureInMicroseconds(_compressionTask);
			_decompressionTime = Utils.MeasureInMicroseconds(_decompressionTask);
			_compressedFileSize = Utils.GetFileSizeInBytes(_outCompressed);
			_originalFileSize = Utils.GetFileSizeInBytes(_original);
			Console.WriteLine("Done.");
		}

		public IEnumerable<object> GetResult()
		{
			return new object[]
			{
				_name, _compressionTime, _decompressionTime,
				_compressedFileSize, _originalFileSize - _compressedFileSize
			};
		}

		private void _compressionTask()
		{
			_algorithm.SetInputFile(_original);
			_algorithm.Compress(_outCompressed);
		}

		private void _decompressionTask()
		{
			_algorithm.SetInputFile(_outCompressed);
			_algorithm.Decompress(_outDecompressed);
		}
	}
}
