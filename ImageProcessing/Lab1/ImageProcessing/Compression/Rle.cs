using System;
using System.Collections.Generic;
using System.Drawing.Imaging;
using System.IO;

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

		private static byte[] _encodeBitmap(Bmp bmp)
		{
			if (bmp.infoHeader.BitCount != 8)
			{
				throw new ArgumentException("The image must be in 8-bit pixel format", nameof(bmp));
			}

			var data = bmp.image.ToBytes();
			var result = new List<byte>();
			var stride = bmp.infoHeader.Width;
			while (stride % 4 != 0)
			{
				stride += 1;
			}
			
			for (var x = 0; x < bmp.infoHeader.Height; x++)
			{
				byte? storedPixel = null;
				var curPixelRepetitions = 0;
				for (var y = 0; y < bmp.infoHeader.Width; y++)
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

				if (x != bmp.infoHeader.Height - 1)
				{
					// End of Line Flag
					result.Add(0x00);
					result.Add(0x00);
				}
				else
				{
					// EOF flag
					result.Add(0x00);
					result.Add(0x01);
					break;
				}
			}

			var compressedBmp = new Bmp
			{
				header = bmp.header,
				infoHeader = bmp.infoHeader,
				palette = bmp.palette,
				image = new Bmp.Image
				{
					Bytes = result.ToArray()
				}
			};

			compressedBmp.header.DataOffset = Bmp.Header.Size + Bmp.InfoHeader.Size + Bmp.Palette.Size;
			compressedBmp.header.FileSize = compressedBmp.header.DataOffset + (uint) result.Count;
			
			compressedBmp.infoHeader.Compression = 0x0001;
			compressedBmp.infoHeader.ImageSize = (uint) result.Count;
			compressedBmp.infoHeader.ColorUsed = 256;

			return compressedBmp.ToBytes();
		}
		
		private static byte[] _decodeBitmap(Bmp bmp)
		{
			if (bmp.infoHeader.BitCount != 8)
			{
				throw new ArgumentException("The image must be in 8-bit pixel format", nameof(bmp));
			}

			var data = bmp.image.ToBytes();
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

			var compressedBmp = new Bmp
			{
				header = bmp.header,
				infoHeader = bmp.infoHeader,
				palette = bmp.palette,
				image = new Bmp.Image
				{
					Bytes = result.ToArray()
				}
			};
			
			compressedBmp.header.DataOffset = Bmp.Header.Size + Bmp.InfoHeader.Size + Bmp.Palette.Size;
			compressedBmp.header.FileSize = compressedBmp.header.DataOffset + (uint) result.Count;
			
			compressedBmp.infoHeader.Compression = 0x0000;
			compressedBmp.infoHeader.ImageSize = (uint) result.Count;
			compressedBmp.infoHeader.ColorUsed = 256;

			return compressedBmp.ToBytes();
		}
		
		public override void Compress(string outputFile)
		{
			var bitmap = new Bmp(InputFile);
			File.WriteAllBytes(outputFile, _encodeBitmap(bitmap));
		}
		
		public override void Decompress(string outputFile)
		{
			var bitmap = new Bmp(InputFile);
			File.WriteAllBytes(outputFile, _decodeBitmap(bitmap));
		}
	}
}
