# Third-Party Android Bindings for Xamarin

This repo contains Xamarin.Android bindings for some **third-party** Android libraries.

The Android SDK relies on various dependencies, as you can see when downloading the new .AAR packages using the update-android-dependencies script in the Xamarin SDK repo.

These dependencies need to be added to the Xamarin SDK, in order for it to work.

For this very reason, we have created this nuget package, to include all the Android libraries which are not directly correlated to Scanbot SDK, so that we can include them easily in our Android Xamarin Binding Library projects, and in the published Scanbot Xamarin SDK and Scanbot Xamarin Forms SDK nuget packages.

The dependencies are listed in three different places: 

a) **In the `Scanbot.Xamarin.SDK.Dependencies.nuspec` file:** 

These dependencies are published and mantained by 3rd parties (they are mostly Xamarin official binding libraries).

eg.
```xml
...
<dependency id="Xamarin.Android.ReactiveX.RxJava3.RxJava" version="3.0.1.1" />
<dependency id="Xamarin.Android.JetBrains.Kotlin_Android_Extensions_Runtime" version="1.5.20.1" />
<dependency id="Xamarin.Android.JetBrains.Kotlin_Parcelize_Runtime" version="1.5.20.1" />
<dependency id="Xamarin.AndroidX.Activity.Ktx" version="1.2.2" />
...
```

b) **Under Scanbot.Xamarin.SDK.Dependencies/Jars**

These are dependencies that we had to bind manually, by creating a binding library project with the jar files for each library.

We currently have:

```bash
commons-io
commons-lang
gson
javax.inject
kotlin-reflect
kotlinx-coroutines-rx3
```


You can see that these libraries are published with the Scanbot.Xamarin.SDK.Dependencies package, since the .nuspec file contains this line under the `<files>` tag:

```xml
<file src="bin/Release/Scanbot.Xamarin.SDK.Dependencies.dll" target="lib/MonoAndroid81" />
```

c) **As Binding Libraries Projects**

We used to have many binding library packages released separately, and they are still in the repository at the moment, as you can see (eg. Scanbot.Xamarin.Kotlin.StdLib projects).

You can see which packages are currently being shipped with the Scanbot.Xamarin.SDK.Dependencies nuget package, in the .nuspec file, under the `<files>` tag; at the moment, we only have ApwLibrary: 

```xml
<file src="../Scanbot.Xamarin.ApwLibrary/bin/Release/Scanbot.Xamarin.ApwLibrary.dll" target="lib/MonoAndroid81" />
```

**OLD PUBLISHED PACKAGES**

Current list of published bindings as seaprate NuGet packages **(OBSOLETE)**:
- [Scanbot.Xamarin.Kotlin.StdLib](https://www.nuget.org/packages/Scanbot.Xamarin.Kotlin.StdLib/)
- [Scanbot.Xamarin.Kotlin.StdLib.Jdk7](https://www.nuget.org/packages/Scanbot.Xamarin.Kotlin.StdLib.Jdk7/)
- [Scanbot.Xamarin.Kotlin.StdLib.Jdk8](https://www.nuget.org/packages/Scanbot.Xamarin.Kotlin.StdLib.Jdk8/)
- [Scanbot.Xamarin.Kotlin.StdLib.Jre7](https://www.nuget.org/packages/Scanbot.Xamarin.Kotlin.StdLib.Jre7/)
- [Scanbot.Xamarin.Kotlin.StdLib.Jre8](https://www.nuget.org/packages/Scanbot.Xamarin.Kotlin.StdLib.Jre8/)
- [Scanbot.Xamarin.JetBrains.Java.Annotations](https://www.nuget.org/packages/Scanbot.Xamarin.JetBrains.Java.Annotations/)


## Please note

This repo is **not about** bindings for the [Scanbot SDK](https://scanbot.io/sdk.html).

You can find the bindings for the Scanbot SDK for Xamarin as an universal NuGet package here: [`ScanbotSDK.Xamarin`](https://www.nuget.org/packages/ScanbotSDK.Xamarin/)


## License

The license for this repository is specified in the [LICENSE.md](LICENSE.md) file.

For licenses of third-party libraries please see the `THIRD-PARTY-NOTICES.txt` files in corresponding folders.
