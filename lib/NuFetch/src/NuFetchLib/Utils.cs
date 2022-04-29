using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using NuGet;

namespace NuFetchLib {
    public static class Utils {
        /// <summary>
        /// Method for getting the abosulte path
        /// </summary>
        /// <param name="folderPath">Folder path, can be relative or absolute</param>
        /// <returns>The determined absolute path from the input parameter</returns>
        public static string GetFullFolderPath( string folderPath ) {
            if ( folderPath == null ) {
                throw new ArgumentNullException( nameof( folderPath ) );
            }

            var finalFullPath = new StringBuilder( folderPath );

            // no need to do anything for absolute paths
            if ( Path.IsPathRooted( folderPath ) ) {
                return finalFullPath.ToString();
            }

            // convert relative paths to absolute path
            finalFullPath.Remove( 0, finalFullPath.Length );
            finalFullPath.Append( Path.Combine( AppDomain.CurrentDomain.BaseDirectory, folderPath ) );

            return finalFullPath.ToString();
        }

        public static void GetPackageAndDependencies( NuFetchOption appOptions ) {
            GetPackageAndDependencies( appOptions.PackageId, appOptions.PackageVersion, appOptions.ServerSource,
                                       GetFullFolderPath( appOptions.TargetFolder ), appOptions.OverwriteExistingFiles,
                                       appOptions.IncludePreRelease, appOptions.AllowUnlisted,
                                       appOptions.VersionTypeToDownload );
        }

        public static void FetchPackagesAndSaveFile(NuFetchOption appOptions) {
            Console.WriteLine("Fetching packages...");
            var dependenciesDictionary = GetDependenciesDictionary(appOptions);
            Console.WriteLine("Packages fetched succesfully! Writing output text file");


            var lines = dependenciesDictionary
                .Keys
                .OrderBy((key) => key)
                .Select((key) => string.Format("{0}@{1}", key, dependenciesDictionary[key]))
                .ToList();

            var fileName = string.Format("package_{0}_{1}.txt", appOptions.PackageId, appOptions.PackageVersion);
            var outputFolder = "lib/NuFetch/output";
            var filePath = string.Format("{0}/{1}", outputFolder, fileName);

            File.WriteAllLines(filePath, lines);
            Console.WriteLine(string.Format("Saved packages fetch results in {0}", filePath));
        }

        public static Dictionary<string, string> GetDependenciesDictionary(NuFetchOption appOptions)
        {
            return GetDependenciesDictionary(
                appOptions.PackageId,
                appOptions.PackageVersion,
                appOptions.ServerSource,
                appOptions.IncludePreRelease,
                appOptions.AllowUnlisted,
                appOptions.VersionTypeToDownload);
        }

        public static Dictionary<string, string> GetDependenciesDictionary(
            string packageId,
            string packageVersion,
            string sourceServer,
            bool includePrerelease,
            bool allowUnlisted,
            DependencyVersionTypeToDownload depVersionToDownload,
            List<string> skipPackages = null
        )
        {
            Console.WriteLine($"Entered GetDependenciesDictionary(" +
                $"packageId='{packageId}', " +
                $"packageVersion='{packageVersion}', " +
                $"sourceServer='{sourceServer}', " +
                $"includePrerelease={includePrerelease}, " +
                $"allowUnlisted={allowUnlisted}, " +
                $"depVersionToDownload={depVersionToDownload})");

            if (skipPackages == null)
            {
                skipPackages = new List<string>();
            }

            var repo = PackageRepositoryFactory.Default.CreateRepository(sourceServer);

            var package = repo.FindPackage(
                packageId,
                packageVersion == null ? null : new SemanticVersion(packageVersion),
                NullConstraintProvider.Instance,
                includePrerelease,
                allowUnlisted
            ) as DataServicePackage;

            if (package == null)
            {
                Console.WriteLine($"Package '{packageId} {packageVersion}' could not be found in the repository '{sourceServer}', or it could be converted as DataServicePackage");
                return null;
            }

            var outDictionary = new Dictionary<string, string>
            {
                { packageId, packageVersion }
            };

            var dependencySets = package.DependencySets.Where(dependencySet => dependencySet.Dependencies.Count > 0);
            foreach (var dependencySet in dependencySets) {
                foreach (var dependency in dependencySet.Dependencies) {
                    var dependencyVersion = depVersionToDownload == DependencyVersionTypeToDownload.Max
                                ? dependency.VersionSpec?.MaxVersion?.ToString()
                                : dependency.VersionSpec?.MinVersion?.ToString();

                    var dependencyHash = string.Format("{0}@{1}", dependency.Id, dependencyVersion);
                    if (skipPackages.Contains(dependencyHash)) {
                        continue;
                    }

                    skipPackages.Add(dependencyHash);

                    var dependencyDictionary = GetDependenciesDictionary(
                        dependency.Id,
                        dependencyVersion,
                        sourceServer,
                        includePrerelease,
                        allowUnlisted,
                        depVersionToDownload,
                        skipPackages
                    );
                    outDictionary = outDictionary
                        .Union(dependencyDictionary)
                        .GroupBy(g => g.Key)
                        .ToDictionary(pair => pair.Key, pair => pair.First().Value);
                }
            }

            return outDictionary;
        }

        public static void GetPackageAndDependencies( string packageId, string packageVersion, string sourceServer, string targetFolder, bool overwriteExistingFiles, bool includePrerelease, bool allowUnlisted, DependencyVersionTypeToDownload depVersionToDownload) {
            Console.WriteLine( $"Entered GetPackageAndDependencies(packageId='{packageId}', packageVersion='{packageVersion}', sourceServer='{sourceServer}', targetFolder='{targetFolder}', overwriteExistingFiles={overwriteExistingFiles}, includePrerelease={includePrerelease}, allowUnlisted={allowUnlisted}, depVersionToDownload={depVersionToDownload})" );

            var repo = PackageRepositoryFactory.Default.CreateRepository( sourceServer );
            var package = repo.FindPackage( packageId, packageVersion==null?null:new SemanticVersion(packageVersion),NullConstraintProvider.Instance, includePrerelease, allowUnlisted ) as DataServicePackage;

            if( package == null ) {
                Console.WriteLine( $"Package '{packageId} {packageVersion}' could not be found in the repository '{sourceServer}', or it could be converted as DataServicePackage" );
                
                return;
            }

            var finalPackagePath = Path.Combine( targetFolder, $"{package.Id}.{package.Version}.nupkg" );

            if( File.Exists( finalPackagePath ) && !overwriteExistingFiles ) {
                Console.WriteLine( $"Skipping '{finalPackagePath}'" );
                return;
            }

            if( !Directory.Exists( targetFolder ) ) {
                Directory.CreateDirectory( targetFolder );
            }

            using( var fs = File.Open( finalPackagePath, FileMode.Create ) ) {
                Console.WriteLine($"Downloading package '{package.Id}' from '{package.DownloadUrl}' ... ");
                var downloader = new PackageDownloader();
                downloader.DownloadPackage( package.DownloadUrl, package, fs );
                Console.WriteLine($"Package {package.Id} downloaded!");
            }

            foreach( var dset in package.DependencySets.Where( dset => dset.Dependencies.Count > 0 ) ) {
                Console.WriteLine( $"Processing dependency set: {dset.TargetFramework?.ToString() ?? "<default set>"} " );

                foreach( var dep in dset.Dependencies ) {
                    Console.WriteLine( $"Processing dependency '{dep.Id}'" );
                    var dependencyVersion = depVersionToDownload == DependencyVersionTypeToDownload.Max
                                                ? dep.VersionSpec?.MaxVersion?.ToString()
                                                : dep.VersionSpec?.MinVersion?.ToString();
                    GetPackageAndDependencies( dep.Id, dependencyVersion, sourceServer, targetFolder, overwriteExistingFiles, includePrerelease, allowUnlisted, depVersionToDownload );
                }
            }
            Console.WriteLine( "Exiting GetPackageAndDependencies" );
        }
    }
}