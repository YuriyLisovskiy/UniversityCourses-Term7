using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;

namespace ImageProcessing
{
	public class Histogram
	{
		private readonly Bitmap _bitmap;
		private Dictionary<uint, ulong> _dataR;
		private Dictionary<uint, ulong> _dataG;
		private Dictionary<uint, ulong> _dataB;

		private StreamWriter _file;
		
		public Histogram(string path)
		{
			_bitmap = new Bitmap(path);
		}

		public void Calc()
		{
			_initDictionaries();
			for (var y = 0; y < _bitmap.Height; y++)
			{
				for (var x = 0; x < _bitmap.Width; x++)
				{
					var color = _bitmap.GetPixel(x, y);
					_dataR[color.R]++;
					_dataG[color.G]++;
					_dataB[color.B]++;
				}
			}
		}

		public void Write(string path)
		{
			_file = new StreamWriter(path);
			_writeDict(_dataR);
			_writeDict(_dataG);
			_writeDict(_dataB);
			_file.Close();
		}

		private void _writeDict(IReadOnlyDictionary<uint, ulong> dict)
		{
			foreach (var (key, value) in dict)
			{
				_file.Write($"{key},{value}{(dict[key] == dict.Last().Value ? "" : ";")}");
			}
			
			_file.Write("\n");
		}

		private void _initDictionaries()
		{
			_dataR = new Dictionary<uint, ulong>();
			_dataG = new Dictionary<uint, ulong>();
			_dataB = new Dictionary<uint, ulong>();
			for (uint i = 0; i < 256; i++)
			{
				_dataR[i] = 0;
				_dataG[i] = 0;
				_dataB[i] = 0;
			}
		}
	}
}
