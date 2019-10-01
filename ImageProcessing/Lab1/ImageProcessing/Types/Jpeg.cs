using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace ImageProcessing.Types
{
	public class Jpeg
	{
		public JpgHeader Header;
		public JpgImageData ImageData;

		public Jpeg()
		{
		}
		
		public Jpeg(string path)
		{
			_read(path);
		}

		private void _read(string path)
		{
			using (var reader = new BinaryReader(File.OpenRead(path)))
			{
				_readHeader(reader);
				_readBody(reader);
			}
		}

		private void _readHeader(BinaryReader reader)
		{
			Header = new JpgHeader
			{
				Soi = reader.ReadBytes(2),
				App0 = reader.ReadBytes(2),
				Length = reader.ReadBytes(2),
				Identifier = reader.ReadBytes(5),
				Version = reader.ReadBytes(2),
				Units = reader.ReadByte(),
				XDensity = reader.ReadBytes(2),
				YDensity = reader.ReadBytes(2),
				XThumbnail = reader.ReadByte(),
				YThumbnail = reader.ReadByte()
			};
		}
		
		private void _readBody(BinaryReader reader)
		{
			var soi = BitConverter.ToUInt16(Header.Soi);

			ImageData = new JpgImageData(
				reader.ReadBytes((int) (reader.BaseStream.Length - BitConverter.ToInt16(Header.Soi)))
			);
		}
		
		public byte[] ToBytes()
		{
			return Header.GetBytes().Concat(ImageData.GetBytes()).ToArray();
		}
		
		public class JpgHeader
		{
			public const int Size = 20;
			
			public byte[] Soi;			// 2 bytes | Start of Image Marker
			public byte[] App0;			// 2 bytes | Application Use Marker
			public byte[] Length;		// 2 bytes | Length of APP0 Field
			public byte[] Identifier;	// 5 bytes | "JFIF" (zero terminated) Id String
			public byte[] Version;		// 2 bytes | JFIF Format Revision
			public byte Units;			// 1 byte  | Units used for Resolution
			public byte[] XDensity;		// 2 bytes | Horizontal Resolution
			public byte[] YDensity;		// 2 bytes | Vertical Resolution
			public byte XThumbnail;		// 1 byte  | Horizontal Pixel Count
			public byte YThumbnail;		// 1 byte  | Vertical Pixel Count

			public byte[] GetBytes()
			{
				var result = new List<byte>();
				result.AddRange(Soi);
				result.AddRange(App0);
				result.AddRange(Length);
				result.AddRange(Identifier);
				result.AddRange(Version);
				result.Add(Units);
				result.AddRange(XDensity);
				result.AddRange(YDensity);
				result.Add(XThumbnail);
				result.Add(YThumbnail);
				return result.ToArray();
			}
		}

		public class JpgImageData
		{
			private readonly byte[] _bytes;

			public JpgImageData(byte[] bytes)
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
