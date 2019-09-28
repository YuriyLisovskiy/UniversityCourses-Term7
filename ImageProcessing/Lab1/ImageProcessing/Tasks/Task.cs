using System;
using System.Collections.Generic;

namespace ImageProcessing.Tasks
{
	public abstract class Task
	{
		protected string Name;
		private long _compressionTime;
		private long _decompressionTime;
		private long _compressedFileSize;
		private long _originalFileSize;
		
		protected Task(string name)
		{
			Name = name;
		}
		
		public void Run()
		{
			Console.WriteLine($"{Name} task running...");
			_compressionTime = Utils.MeasureInMicroseconds(CompressionTask);
			_decompressionTime = Utils.MeasureInMicroseconds(DecompressionTask);
			_compressedFileSize = CompressedFileSize();
			_originalFileSize = OriginalFileSize();
			Console.WriteLine("Done.\n");
		}

		public IEnumerable<object> GetResult()
		{
			return new object[]
			{
				Name, _compressionTime, _decompressionTime,
				_compressedFileSize, _originalFileSize - _compressedFileSize
			};
		}

		protected abstract void CompressionTask();
		protected abstract void DecompressionTask();
		protected abstract long CompressedFileSize();
		protected abstract long OriginalFileSize();
	}
}
