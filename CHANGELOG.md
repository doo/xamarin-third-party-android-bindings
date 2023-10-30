
## CHANGES for Scanbot.NET.SDK.Dependencies.1.0.0-beta.4 1.0.0-beta.4

- ⚙  Changes:

  - Targeting .NET
  - Added support for Android 13


## CHANGES for Scanbot.Xamarin.SDK.Dependencies v3.4.1

- ⚙  Changes:

  - A problem with FormsAppCompatActivity emerged when using the new dependencies; after trying to manually add
    Xamarin.AndroidX.AppCompat 1.3.1 to the project (was 1.3.0), the issue was gone.

    For this reason, these two dependencies were updated in the Scanbot.Xamarin.SDK.Dependencies NuGet package:
    
    - Updated `Xamarin.AndroidX.Core` from 1.3.2.3 to **1.6.0**
    - Updated `Xamarin.AndroidX.AppCompat` from 1.2.0.7 to **1.3.1**

    Where the second one is AppCompat, and the first one is a peer dependency that comes with it, that we have to
    manually install in order to use the compatible version

  - Updated `Xamarin.AndroidX.Collection.Ktx` from 1.1.0 to **1.1.0.3**
  - Updated `Xamarin.AndroidX.ConstraintLayout` from 2.0.4.2 to **2.0.4.3**
  - Updated `Xamarin.AndroidX.Arch.Core.Runtime` from 2.1.0.8 to **2.1.0.11**
  - Updated `Xamarin.AndroidX.DynamicAnimation` from 1.0.0.7 to **1.0.0.10**
  - Updated `Xamarin.AndroidX.Lifecycle.Common` from 2.3.1 to **2.3.1.3**
  - Updated `Xamarin.AndroidX.Lifecycle.ViewModel.Ktx` from 2.3.1 to **2.3.1.3**
  - Updated `Xamarin.AndroidX.Lifecycle.LiveData.Core.Ktx` from 2.3.1 to **2.3.1.3**
  - Updated `Xamarin.AndroidX.Lifecycle.Process` from 2.2.0 to **2.2.0.4**
  - Updated `Xamarin.AndroidX.Lifecycle.Service` from 2.2.0 to **2.2.0.4**
  - Updated `Xamarin.AndroidX.Lifecycle.Extensions` from 2.2.0 to **2.2.0.10**
  - Updated `Xamarin.AndroidX.Lifecycle.Runtime.Ktx` from 2.2.0 to **2.3.1.3**


