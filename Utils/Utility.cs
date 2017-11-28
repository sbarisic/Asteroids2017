using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.IO;
using System.Net;
using System.Threading;

namespace Utils {
	public static class Utility {
		static string ExceptionsPath;

		public static void Init() {
			ExceptionsPath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "exceptions.txt");

			if (File.Exists(ExceptionsPath))
				File.Delete(ExceptionsPath);

			AppDomain.CurrentDomain.UnhandledException += UnhandledException;
		}

		public static void WriteError(object E) {
			string S = string.Format("{0}\n", E == null ? "null" : E.ToString());
			File.AppendAllText(ExceptionsPath, S);
			Console.Write(S);
			Console.ReadLine();
		}

		static void UnhandledException(object S, UnhandledExceptionEventArgs E) {
			WriteError(E);
		}

		// TODO: Port to python
		public static void FetchTextures(ICollection<object> Texs) {
			WebClient WC = new WebClient();

			if (!Directory.Exists("textures"))
				Directory.CreateDirectory("textures");

			foreach (var T in Texs) {
				string Name = T.ToString() + ".jpg";
				if (File.Exists("textures\\" + Name)) {
					//Console.WriteLine("Skipping {0}", Name);
					continue;
				}

				try {
					File.WriteAllBytes("textures\\" + Name,
						WC.DownloadData(("http://raw.githubusercontent.com/Calinou/quake-retexturing-project/master/" + Name).Replace("#", "%23")));
				} catch (Exception E) {
					Console.WriteLine("Not found: {0}", Name);
				}

				Thread.Sleep(500);
			}
		}
	}
}
