using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace ImageProcessing.Types
{
	public class Bitmap8
	{
		public BmpHeader Header;
		public BmpInfoHeader InfoHeader;
		public BmpPalette Palette;
		public BmpImageData ImageData;
		
		public Bitmap8()
		{
		}
		
		public Bitmap8(string path)
		{
			_read(path);
		}

		public byte[] GetBytes()
		{
			return Header.GetBytes()
				.Concat(InfoHeader.GetBytes())
				.Concat(Palette.GetBytes())
				.Concat(ImageData.GetBytes())
				.ToArray();
		}
		
		public IEnumerable<BmpPixel> GetPalette()
		{
			var bytes = Palette.GetBytes();
			var pixels = new List<BmpPixel>();
			for (var i = 0; i < bytes.Length; i += 4)
			{
				pixels.Add(new BmpPixel(bytes[i], bytes[i + 1], bytes[i + 2], bytes[i + 3]));
			}

			return pixels.ToArray();
		}
		
		private void _read(string path)
		{
			using (var reader = new BinaryReader(File.OpenRead(path)))
			{
				_readHeaders(reader);
				_readPalette(reader);
				_readBody(reader);
			}
		}
		
		private void _readHeaders(BinaryReader reader)
		{
			Header = new BmpHeader
			{
				Signature = reader.ReadBytes(2),
				FileSize = reader.ReadUInt32(),
				Reserved = reader.ReadBytes(4),
				DataOffset = reader.ReadUInt32()
			};

			InfoHeader = new BmpInfoHeader
			{
				InfoHeaderSize = reader.ReadUInt32(),
				Width = reader.ReadUInt32(),
				Height = reader.ReadUInt32(),
				Planes = reader.ReadUInt16(),
				BitCount = reader.ReadUInt16(),
				Compression = reader.ReadUInt32(),
				ImageSize = reader.ReadUInt32(),
				XPixelsPerMeter = reader.ReadUInt32(),
				YPixelsPerMeter = reader.ReadUInt32(),
				ColorUsed = reader.ReadUInt32(),
				ImportantColors = reader.ReadUInt32()
			};
		}
		
		private void _readPalette(BinaryReader reader)
		{
			Palette = new BmpPalette(reader.ReadBytes(BmpPalette.Size));
		}
		
		private void _readBody(BinaryReader reader)
		{
			ImageData = new BmpImageData(reader.ReadBytes((int) (reader.BaseStream.Length - Header.DataOffset)));
		}

		public class BmpHeader
		{
			public const int Size = 14;
			
			public byte[] Signature;		// 2 bytes
			public uint FileSize;			// 4 bytes
			public byte[] Reserved;			// 4 bytes
			public uint DataOffset;			// 4 bytes

			public IEnumerable<byte> GetBytes()
			{
				var result = new List<byte>();
				result.AddRange(Signature); // signature (BM)
				result.AddRange(BitConverter.GetBytes(FileSize));
				result.AddRange(Reserved); // reserved
				result.AddRange(BitConverter.GetBytes(DataOffset));
				return result.ToArray();
			}
		}
		
		public class BmpInfoHeader
		{
			public const int Size = 40;
			
			public uint InfoHeaderSize;		// 4 bytes
			public uint Width;				// 4 bytes
			public uint Height;				// 4 bytes
			public ushort Planes;			// 2 bytes
			public ushort BitCount;			// 2 bytes
			public uint Compression;		// 4 bytes
			public uint ImageSize;			// 4 bytes
			public uint XPixelsPerMeter;	// 4 bytes
			public uint YPixelsPerMeter;	// 4 bytes
			public uint ColorUsed;			// 4 bytes
			public uint ImportantColors;	// 4 bytes
			
			public IEnumerable<byte> GetBytes()
			{
				var result = new List<byte>();
				result.AddRange(BitConverter.GetBytes(InfoHeaderSize));
				result.AddRange(BitConverter.GetBytes(Width));
				result.AddRange(BitConverter.GetBytes(Height));
				result.AddRange(BitConverter.GetBytes(Planes));
				result.AddRange(BitConverter.GetBytes(BitCount));
				result.AddRange(BitConverter.GetBytes(Compression));
				result.AddRange(BitConverter.GetBytes(ImageSize));
				result.AddRange(BitConverter.GetBytes(XPixelsPerMeter));
				result.AddRange(BitConverter.GetBytes(YPixelsPerMeter));
				result.AddRange(BitConverter.GetBytes(ColorUsed));
				result.AddRange(BitConverter.GetBytes(ImportantColors));
				return result.ToArray();
			}
		}

		public class BmpPixel
		{
			public byte R { get; }
			public byte G { get; }
			public byte B { get; }
			public byte Reserved { get; }

			public BmpPixel(byte r, byte g, byte b, byte reserved)
			{
				R = r;
				G = g;
				B = b;
				Reserved = reserved;
			}
		}
		
		public class BmpPalette
		{
			public const int Size = 4 * 256;
			
			private readonly byte[] _bytes;

			public BmpPalette(byte[] bytes)
			{
				_bytes = bytes;
			}

			public byte[] GetBytes()
			{
				return _bytes;
			}
		}
		
		public class BmpImageData
		{
			private readonly byte[] _bytes;

			public BmpImageData(byte[] bytes)
			{
				_bytes = bytes;
			}

			public byte[] GetBytes()
			{
				return _bytes;
			}
		}
	}
}
