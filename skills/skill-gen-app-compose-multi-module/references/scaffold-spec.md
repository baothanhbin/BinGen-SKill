# Scaffold Spec

## Purpose
This file defines what the scaffold script must generate for a new project baseline.

## Phase 1: Root Files
Generate:
- `settings.gradle.kts`
- `build.gradle.kts`
- `gradle.properties`
- `gradle/libs.versions.toml`
- `build-logic/settings.gradle.kts`
- `build-logic/convention/build.gradle.kts`
- `gradle/wrapper/gradle-wrapper.properties`

If the target folder is empty, it is acceptable for the scaffold to omit wrapper binaries and leave a note that the user should run the Gradle wrapper bootstrap later.

## Phase 2: Build Logic
Generate convention plugins equivalent in responsibility to the AgriDoctorAI repo:
- application compose plugin
- library compose plugin
- feature plugin
- base android module plugin
- Hilt plugin
- Room plugin

The generated plugin ids should use the user-provided slug.

## Phase 3: Shared Modules
Generate these modules with minimal but valid contents:
- `resources`
- `core:model`
- `core:theme`
- `core:ui`
- `core:network`
- `core:data`
- `core:database`
- `core:datastore`
- `core:alarm`

Each module should include:
- `build.gradle.kts`
- `consumer-rules.pro`
- `proguard-rules.pro`
- `src/main/AndroidManifest.xml`

## Phase 4: App Shell
Generate:
- `App.kt` with `@HiltAndroidApp`
- `MainActivity.kt`
- `MainViewModel.kt`
- `ui/MainApp.kt`
- `ui/MainBottomNavBar.kt`
- `navigation/AppState.kt`
- `navigation/MainNavHost.kt`
- `navigation/TopLevelDestination.kt`
- app `AndroidManifest.xml`
- `res/values/strings.xml`
- `res/values/themes.xml`
- `res/xml/network_security_config.xml`

## Phase 5: Starter Features
If not in `--minimal` mode, generate at least:
- `feature/home`
- `feature/login`

Each feature should include:
- `Screen.kt`
- `ViewModel.kt`
- `navigation/<Feature>Navigation.kt`
- `component/<Feature>Content.kt`

## Phase 6: Wiring
The generated project should already:
- include all modules in `settings.gradle.kts`
- use type-safe project accessors
- wire `home` and `login` in `MainNavHost`
- expose top-level destination for `home`
- compile conceptually as a modular Compose app

## Expected Quality
- files should be small but coherent
- generated code should not be placeholder gibberish
- namespaces, imports, plugin ids, and package names should all match the provided base package and slug
