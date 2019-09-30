using System;
using System.Collections.Generic;
using System.Drawing.Imaging;
using System.IO;
using ImageProcessing.Types;

namespace ImageProcessing.Compression
{
	public class Rle : Compressor
	{
		public Rle(string inputFile) : base(
			inputFile,
			ImageFormat.Bmp,
			ImageFormat.Bmp,
			EncoderValue.CompressionRle
		)
		{
		}

		private static byte[] _encodeBitmap(Bitmap8 bmp)
		{
			if (bmp.InfoHeader.BitCount != 8)
			{
				throw new ArgumentException("The image must be in 8-bit pixel format", nameof(bmp));
			}

			var data = bmp.ImageData.GetBytes();
			var result = new List<byte>();
			var stride = bmp.InfoHeader.Width;
			while (stride % 4 != 0)
			{
				stride += 1;
			}
			
			for (var x = 0; x < bmp.InfoHeader.Height; x++)
			{
				byte? storedPixel = null;
				var curPixelRepetitions = 0;
				for (var y = 0; y < bmp.InfoHeader.Width; y++)
				{
					var curPixel = data[x * stride + y];
					if (!storedPixel.HasValue)
					{
						curPixelRepetitions = 1;
						storedPixel = curPixel;
					}
					else if (storedPixel.Value != curPixel || curPixelRepetitions == 255)
					{
						result.Add(Convert.ToByte(curPixelRepetitions));
						result.Add(storedPixel.Value);
						curPixelRepetitions = 1;
						storedPixel = curPixel;
					}
					else
					{
						curPixelRepetitions++;
					}
				}

				if (curPixelRepetitions > 0)
				{
					result.Add(Convert.ToByte(curPixelRepetitions));
					result.Add(storedPixel.Value);
				}

				if (x != bmp.InfoHeader.Height - 1)
				{
					result.Add(0x00);
					result.Add(0x00);
				}
				else
				{
					result.Add(0x00);
					result.Add(0x01);
					break;
				}
			}

			var compressedBmp = new Bitmap8
			{
				Header = bmp.Header,
				InfoHeader = bmp.InfoHeader,
				Palette = bmp.Palette,
				ImageData = new Bitmap8.BmpImageData(result.ToArray())
			};

			compressedBmp.Header.DataOffset = Bitmap8.BmpHeader.Size + Bitmap8.BmpInfoHeader.Size + Bitmap8.BmpPalette.Size;
			compressedBmp.Header.FileSize = compressedBmp.Header.DataOffset + (uint) result.Count;
			
			compressedBmp.InfoHeader.Compression = 0x0001;
			compressedBmp.InfoHeader.ImageSize = (uint) result.Count;
			compressedBmp.InfoHeader.ColorUsed = 256;

			return compressedBmp.GetBytes();
		}
		
		private static byte[] _decodeBitmap(Bitmap8 bmp)
		{
			if (bmp.InfoHeader.BitCount != 8)
			{
				throw new ArgumentException("The image must be in 8-bit pixel format", nameof(bmp));
			}

			var data = bmp.ImageData.GetBytes();
			var result = new List<byte>();
			var row = new List<byte>();

			for (var i = 0; i < data.Length; i += 2)
			{
				var repetitions = data[i];
				var pixel = data[i + 1];
				if (repetitions == 0)
				{
					while (row.Count % 4 != 0)
					{
						row.Add(0x00);
					}
					result.AddRange(row);
					row.Clear();
				}
				else
				{
					while (repetitions > 0)
					{
						row.Add(pixel);
						repetitions--;
					}
				}
			}

			var compressedBmp = new Bitmap8
			{
				Header = bmp.Header,
				InfoHeader = bmp.InfoHeader,
				Palette = bmp.Palette,
				ImageData = new Bitmap8.BmpImageData(result.ToArray())
			};
			
			compressedBmp.Header.DataOffset = Bitmap8.BmpHeader.Size + Bitmap8.BmpInfoHeader.Size + Bitmap8.BmpPalette.Size;
			compressedBmp.Header.FileSize = compressedBmp.Header.DataOffset + (uint) result.Count;
			
			compressedBmp.InfoHeader.Compression = 0x0000;
			compressedBmp.InfoHeader.ImageSize = (uint) result.Count;
			compressedBmp.InfoHeader.ColorUsed = 256;

			return compressedBmp.GetBytes();
		}
		
		public override void Compress(string outputFile)
		{
			var bitmap = new Bitmap8(InputFile);
			File.WriteAllBytes(outputFile, _encodeBitmap(bitmap));
		}
		
		public override void Decompress(string outputFile)
		{
			var bitmap = new Bitmap8(InputFile);
			File.WriteAllBytes(outputFile, _decodeBitmap(bitmap));
		}
	}
}
