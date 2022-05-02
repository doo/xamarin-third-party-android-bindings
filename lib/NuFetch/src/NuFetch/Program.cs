using System;
using System.Threading.Tasks;
using CommandLine;
using NuFetchLib;

namespace NuFetch {
    internal class Program {

        private static void Main( string[] args ) {
            MainAsync( args ).Wait();
        }

        private static async Task MainAsync( string[] args ) {
            await Task.Run( () => {
                Console.WriteLine( $"Entered MainAsync(string[] args='{string.Join( ", ", args )}')" );

                var appOptions = new NuFetchOption();
                var parseResult = Parser.Default.ParseArguments( args, appOptions );

                Console.WriteLine( $"arguments parsing was successful? {parseResult}" );

                if( !parseResult ) {
                    return;
                }


                if (appOptions.FetchOnly)
                {
                    Utils.FetchPackagesAndSaveFile(appOptions);
                }
                else {
                    Utils.GetPackageAndDependencies(appOptions);
                }

                Console.WriteLine( "Exiting MainAsync" );
            } );
        }
    }
}