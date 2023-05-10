#!/bin/bash

# clean
for folder in Scanbot.MAUI.*
do
    rm -rf $folder/obj $folder/bin
done

nuget locals all -clear
dotnet msbuild -restore -maxCpuCount:4
dotnet msbuild maui-third-party-android-bindings.sln -maxCpuCount:4 -property:Configuration=Release -target:Clean
dotnet msbuild maui-third-party-android-bindings.sln -maxCpuCount:4 -property:Configuration=Release

# create nugets
NUGET_DIST_TARGET_DIR="./nuget-dist"
rm -rf $NUGET_DIST_TARGET_DIR
mkdir -p $NUGET_DIST_TARGET_DIR

nuget pack Scanbot.MAUI.SDK.Dependencies.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR

echo "NuGet results:"
ls -lah $NUGET_DIST_TARGET_DIR/*
