#!/bin/bash

# Create nugets
NUGET_DIST_TARGET_DIR="./nuget-dist"
rm -rf $NUGET_DIST_TARGET_DIR
mkdir -p $NUGET_DIST_TARGET_DIR
nuget pack Scanbot.Xamarin.SDK.Dependencies.nuspec -OutputDirectory $NUGET_DIST_TARGET_DIR

echo "NuGet results:"
ls -lah $NUGET_DIST_TARGET_DIR/*
