#!/bin/bash

# clean
# for folder in Scanbot.Xamarin.*
# do
#     rm -rf $folder/obj $folder/bin
# done
# msbuild xamarin-third-party-android-bindings.sln /p:Configuration=Release /t:Clean

# # build
# msbuild xamarin-third-party-android-bindings.sln /m:4 /p:Configuration=Release

# create nugets
NUGET_DIST_TARGET_DIR="./nuget-dist"
rm -rf $NUGET_DIST_TARGET_DIR
mkdir -p $NUGET_DIST_TARGET_DIR

nuget pack Scanbot.Xamarin.SDK.Dependencies/Scanbot.Xamarin.SDK.Dependencies.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR

echo "NuGet results:"
ls -lah $NUGET_DIST_TARGET_DIR/*
