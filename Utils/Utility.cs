using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.IO;

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
	}
}
