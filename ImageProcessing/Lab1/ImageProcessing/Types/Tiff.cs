using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace ImageProcessing.Types
{
	public class Tiff
	{
		public Tiff(string path)
		{
			_read(path);
		}

		private void _read(string path)
		{
			using (var reader = new BinaryReader(File.OpenRead(path)))
			{
				
			}
		}
		
		public byte[] ToBytes()
		{
			return null;
		}

		public struct Header
		{
			public const int Size = 8;

			public ushort ByteOrder;	// 2 bytes |  Byte-order Identifier
			public ushort Version;		// 2 bytes | TIFF version number (always 2Ah)
			public uint FirstIfdOffset;	// 4 bytes | Offset of the first Image File Directory
			
			public byte[] GetBytes()
			{
				var result = new List<byte>();
				result.AddRange(BitConverter.GetBytes(ByteOrder));
				result.AddRange(BitConverter.GetBytes(Version));
				result.AddRange(BitConverter.GetBytes(FirstIfdOffset));
				return result.ToArray();
			}
		}
		
		public struct Tag
		{
			public ushort Id;		// 2 bytes | The tag identifier
			public ushort DataType;	// 2 bytes | The scalar type of the data items
			public uint DataCount;	// 4 bytes | The number of items in the tag data
			public uint DataOffset;	// 4 bytes | The byte offset to the data items
			
			public const ushort ByteType = 1;		// 8-bit unsigned integer
			public const ushort AsciiType = 2;		// 8-bit NULL-terminated string
			public const ushort ShortType = 3;		// 16-bit unsigned integer
			public const ushort LongType = 4;		// 32-bit unsigned integer
			public const ushort RationalType = 5;	// Two 32-bit unsigned integers
			public const ushort SByteType = 6;		// 8-bit signed integer
			public const ushort UndefineType = 7;	// 8-bit byte
			public const ushort SShortType = 5;		// 16-bit signed integer
			public const ushort SLongType = 9;		// 32-bit signed integer
			public const ushort SRationalType = 10;	// Two 32-bit signed integers
			public const ushort FloatType = 11;		// 4-byte single-precision IEEE oating-point value
			public const ushort DoubleType = 12;	// 8-byte single-precision IEEE oating-point value

			public const ushort Uncompressed = 1;
			public const ushort LzwCompressed = 5;
			
			public byte[] GetBytes()
			{
				var result = new List<byte>();
				result.AddRange(BitConverter.GetBytes(Id));
				result.AddRange(BitConverter.GetBytes(DataType));
				result.AddRange(BitConverter.GetBytes(DataCount));
				result.AddRange(BitConverter.GetBytes(DataOffset));
				return result.ToArray();
			}
		}
		
		public struct ImageFileDirectory
		{
			public ushort TagEntryCount;	// 2 bytes 			| Number of Tags in IFD
			public Tag[] TagList;			// 12 bytes per tag | Array of Tags
			public uint NextIfdOffset;		// 4 bytes			| Offset to next IFD
			
			public int Size()
			{
				return 2 + 12 * TagEntryCount + 4;
			}

			public bool TagExists(ushort tagId)
			{
				return TagList.Any(tag => tag.Id == tagId);
			}
			
			public byte[] GetBytes()
			{
				var result = new List<byte>();
				result.AddRange(BitConverter.GetBytes(TagEntryCount));
				foreach (var tag in TagList)
				{
					result.AddRange(tag.GetBytes());
				}
				result.AddRange(BitConverter.GetBytes(NextIfdOffset));
				return result.ToArray();
			}
		}
	}
}
