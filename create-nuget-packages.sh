#!/bin/bash

# clean
for folder in Scanbot.Xamarin.*
do
    rm -rf $folder/obj $folder/bin
done
msbuild xamarin-third-party-android-bindings.sln /p:Configuration=Release /t:Clean

# build
msbuild xamarin-third-party-android-bindings.sln /m:4 /p:Configuration=Release

# create nugets
NUGET_DIST_TARGET_DIR="./nuget-dist"
rm -rf $NUGET_DIST_TARGET_DIR
mkdir -p $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.Kotlin.StdLib/Scanbot.Xamarin.Kotlin.StdLib.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.Kotlin.StdLib.Jre7/Scanbot.Xamarin.Kotlin.StdLib.Jre7.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.Kotlin.StdLib.Jre8/Scanbot.Xamarin.Kotlin.StdLib.Jre8.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.Kotlin.StdLib.Jdk7/Scanbot.Xamarin.Kotlin.StdLib.Jdk7.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.Kotlin.StdLib.Jdk8/Scanbot.Xamarin.Kotlin.StdLib.Jdk8.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.JetBrains.Java.Annotations/Scanbot.Xamarin.JetBrains.Java.Annotations.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR

echo "NuGet results:"
ls -lah $NUGET_DIST_TARGET_DIR/*
