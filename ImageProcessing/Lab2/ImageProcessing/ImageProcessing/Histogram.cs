using System.Collections.Generic;
using System.Drawing;

namespace ImageProcessing
{
	public class Histogram
	{
		private Bitmap _bitmap;
		private Dictionary<uint, ulong> _dataR;
		private Dictionary<uint, ulong> _dataG;
		private Dictionary<uint, ulong> _dataB;
		
		public Histogram(Bitmap bmp)
		{
			_bitmap = bmp;
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
			// TODO: write data to files
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
