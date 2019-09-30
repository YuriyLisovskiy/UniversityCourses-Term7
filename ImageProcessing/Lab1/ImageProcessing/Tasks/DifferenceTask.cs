using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

namespace ImageProcessing.Tasks
{
	public static class DifferenceTask
	{
		private static Color _calcPixelDiff(Color left, Color right, bool inv)
		{
			var r = Math.Abs(right.R - left.R);
			var g = Math.Abs(right.G - left.G);
			var b = Math.Abs(right.B - left.B);
			return inv ? Color.FromArgb(255 - r, 255 - g, 255 - b) : Color.FromArgb(r, g, b);
		}

		public static void CreateDifference(string leftImage, string rightImage, string resultImage, string rImage, string gImage, string bImage, bool inv)
		{
			Console.WriteLine("Обчислення різниці JPEG зображення та BMP (початкового)...");
			using (var left = new Bitmap(leftImage))
			using (var right = new Bitmap(rightImage))
			{
				if (right.Height != left.Height)
				{
					throw new InvalidDataException($"Heights are not equal: {right.Height} != {left.Height}");
				}
				
				if (right.Width != left.Width)
				{
					throw new InvalidDataException($"Widths are not equal: {right.Width} != {left.Width}");
				}

				using (var diff = new Bitmap(right.Width, right.Height, PixelFormat.Format24bppRgb))
				using (var rBitmap = new Bitmap(diff.Width, diff.Height, PixelFormat.Format24bppRgb))
				using (var gBitmap = new Bitmap(diff.Width, diff.Height, PixelFormat.Format24bppRgb))
				using (var bBitmap = new Bitmap(diff.Width, diff.Height, PixelFormat.Format24bppRgb))
				{
					var zero = inv ? 255 : 0;
					
					var totalLostPixels = 0;
					var lostRedPixels = 0;
					var lostGreenPixels = 0;
					var lostBluePixels = 0;
					for (var y = 0; y < right.Height; y++)
					{
						for (var x = 0; x < right.Width; x++)
						{
							var diffPixel = _calcPixelDiff(left.GetPixel(x, y), right.GetPixel(x, y), inv);
							diff.SetPixel(x, y, diffPixel);
							rBitmap.SetPixel(x, y, Color.FromArgb(diffPixel.R, zero, zero));
							gBitmap.SetPixel(x, y, Color.FromArgb(zero, diffPixel.G, zero));
							bBitmap.SetPixel(x, y, Color.FromArgb(zero, zero, diffPixel.B));
							
							var hasBadR = diffPixel.R != zero;
							var hasBadG = diffPixel.G != zero;
							var hasBadB = diffPixel.B != zero;
							
							if (hasBadR || hasBadG || hasBadB)
							{
								totalLostPixels++;
								if (hasBadR)
								{
									lostRedPixels++;
								}

								if (hasBadG)
								{
									lostGreenPixels++;
								}
						
								if (hasBadB)
								{
									lostBluePixels++;
								}
							}
						}
					}
					
					diff.Save(resultImage, ImageFormat.Bmp);
					
					Console.WriteLine($"Загальні втрати пікселів: {totalLostPixels}");
					
					rBitmap.Save(rImage, ImageFormat.Bmp);
					gBitmap.Save(gImage, ImageFormat.Bmp);
					bBitmap.Save(bImage, ImageFormat.Bmp);
					
					Console.WriteLine("Втрати по каналах:");
					Console.WriteLine($" - червоний: {lostRedPixels}");
					Console.WriteLine($" - зелений:  {lostGreenPixels}");
					Console.WriteLine($" - синій:    {lostBluePixels}");
				}
			}
		}
	}
}
