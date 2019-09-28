using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace ImageProcessing.Types
{
	public class Bitmap
	{
		public Bitmap()
		{
		}
		
		public Bitmap(string path)
		{
			_read(path);
		}

		public Header header;
		public InfoHeader infoHeader;
		public Palette palette;
		public Image image;

		private void _read(string path)
		{
			using (var reader = new BinaryReader(File.OpenRead(path)))
			{
				header = new Header
				{
					Signature = reader.ReadBytes(2),
					FileSize = reader.ReadUInt32(),
					Reserved = reader.ReadBytes(4),
					DataOffset = reader.ReadUInt32()
				};
				
				infoHeader = new InfoHeader
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

				palette = new Palette
				{
					Bytes = reader.ReadBytes(Palette.Size)
				};

				image = new Image
				{
					Bytes = reader.ReadBytes((int) (reader.BaseStream.Length - header.DataOffset))
				};
			}
		}

		public byte[] ToBytes()
		{
			return header.ToBytes()
				.Concat(infoHeader.ToBytes())
				.Concat(palette.ToBytes())
				.Concat(image.ToBytes())
				.ToArray();
		}
		
		public struct Header
		{
			public const int Size = 14;
			
			// Total: 14 bytes
			public byte[] Signature;		// 2 bytes
			public uint FileSize;			// 4 bytes
			public byte[] Reserved;			// 4 bytes
			public uint DataOffset;			// 4 bytes

			public IEnumerable<byte> ToBytes()
			{
				//	var swap = BitConverter.IsLittleEndian;
				var result = new List<byte>();

				result.AddRange(Signature); // signature (BM)
				result.AddRange(BitConverter.GetBytes(FileSize));
				result.AddRange(Reserved); // reserved
				result.AddRange(BitConverter.GetBytes(DataOffset));

				return result.ToArray();
			}
		}
		
		public struct InfoHeader
		{
			public const int Size = 40;
			
			// Total: 40 bytes
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
            
            public IEnumerable<byte> ToBytes()
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

		public struct Palette
		{
			public const int Size = 4 * 256;
			public byte[] Bytes;

			public IEnumerable<byte> ToBytes()
			{
				return Bytes;
			}
		}

		public struct Image
		{
			public byte[] Bytes;

			public byte[] ToBytes()
			{
				return Bytes;
			}
		}
	}
}
