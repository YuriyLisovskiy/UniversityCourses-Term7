using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using ImageProcessing.Types;

namespace ImageProcessing.Tasks
{
	public static class DifferenceTask
	{
		private static Color _calcPixelDiff(Color left, Color right)
		{
			return Color.FromArgb(
				Math.Abs(right.R - left.R),
				Math.Abs(right.G - left.G),
				Math.Abs(right.B - left.B)
			);
		}

		private static Color _invertPixel(Color pixel)
		{
			return Color.FromArgb(255 - pixel.R, 255 - pixel.G, 255 - pixel.B);
		}

		private static HcvColor _rgbToHsv(Color color)
		{
			int max = Math.Max(color.R, Math.Max(color.G, color.B));
			int min = Math.Min(color.R, Math.Min(color.G, color.B));

			return new HcvColor
			{
				Hue = color.GetHue(),
				Saturation = (max == 0) ? 0 : 1d - (1d * min / max),
				Value = max / 255d
			};
		}

		private static Color _rgbFromHsv(HcvColor hcvColor)
		{
			var hi = Convert.ToInt32(Math.Floor(hcvColor.Hue / 60)) % 6;
			var f = hcvColor.Hue / 60 - Math.Floor(hcvColor.Hue / 60);

			hcvColor.Saturation = Math.Min(1, hcvColor.Saturation);
			
			hcvColor.Value *= 255;
			var v = Convert.ToInt32(hcvColor.Value);
			var p = Convert.ToInt32(hcvColor.Value * (1 - hcvColor.Saturation));
			var q = Convert.ToInt32(hcvColor.Value * (1 - f * hcvColor.Saturation));
			var t = Convert.ToInt32(hcvColor.Value * (1 - (1 - f) * hcvColor.Saturation));

			switch (hi)
			{
				case 0:
					return Color.FromArgb(255, v, t, p);
				case 1:
					return Color.FromArgb(255, q, v, p);
				case 2:
					return Color.FromArgb(255, p, v, t);
				case 3:
					return Color.FromArgb(255, p, q, v);
				case 4:
					return Color.FromArgb(255, t, p, v);
				default:
					return Color.FromArgb(255, v, p, q);
			}
		}
		
		public static void CreateDifference(string leftImage, string rightImage, string resultImage, string rImage, string gImage, string bImage, bool inv, bool log = true)
		{
			if (log)
			{
				Console.WriteLine("Обчислення різниці JPEG зображення та BMP (початкового)...");	
			}
			
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
							var diffPixel = _calcPixelDiff(left.GetPixel(x, y), right.GetPixel(x, y));

							var hasBadR = diffPixel.R != 0;
							var hasBadG = diffPixel.G != 0;
							var hasBadB = diffPixel.B != 0;

							const double intensify = 20;

							if (inv)
							{
								diffPixel = _invertPixel(diffPixel);
							}
							
							var hsvRgbPx = _rgbToHsv(diffPixel);
							hsvRgbPx.Saturation *= intensify;
							var diffPixelFinal = _rgbFromHsv(hsvRgbPx);
							
							var hsvRPx = _rgbToHsv(Color.FromArgb(diffPixel.R, zero, zero));
							hsvRPx.Saturation *= intensify;
							var rPx = _rgbFromHsv(hsvRPx);

							var hsvGPx = _rgbToHsv(Color.FromArgb(zero, diffPixel.G, zero));
							hsvGPx.Saturation *= intensify;
							var gPx = _rgbFromHsv(hsvGPx);

							var hsvBPx = _rgbToHsv(Color.FromArgb(zero, zero, diffPixel.B));
							hsvBPx.Saturation *= intensify;
							var bPx = _rgbFromHsv(hsvBPx);

							diff.SetPixel(x, y, diffPixelFinal);
							rBitmap.SetPixel(x, y, rPx);
							gBitmap.SetPixel(x, y, gPx);
							bBitmap.SetPixel(x, y, bPx);

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

					if (log)
					{
						Console.WriteLine("Загальні втрати:");
						Console.WriteLine($" - кількісні: {totalLostPixels}");
						Console.WriteLine($" - якісні: {totalLostPixels * 100 / (diff.Height * diff.Width)}");
						
						Console.WriteLine("Втрати по каналах:");
						
						Console.WriteLine($" - червоний (кількісні): {lostRedPixels}");
						Console.WriteLine($" - червоний (якісні): {lostRedPixels * 100 / (diff.Height * diff.Width)}%\n");
						
						Console.WriteLine($" - зелений (кількісні):  {lostGreenPixels}");
						Console.WriteLine($" - зелений (якісні):  {lostGreenPixels * 100 / (diff.Height * diff.Width)}%\n");
						
						Console.WriteLine($" - синій (кількісні):    {lostBluePixels}");
						Console.WriteLine($" - синій (якісні):    {lostBluePixels * 100 / (diff.Height * diff.Width)}%");
					}

					rBitmap.Save(rImage, ImageFormat.Bmp);
					gBitmap.Save(gImage, ImageFormat.Bmp);
					bBitmap.Save(bImage, ImageFormat.Bmp);
				}
			}
		}
	}
}
