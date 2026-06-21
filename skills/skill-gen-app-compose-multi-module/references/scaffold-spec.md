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
- `core:worker`

Each module should include:
- `build.gradle.kts`
- `consumer-rules.pro`
- `proguard-rules.pro`
- `src/main/AndroidManifest.xml`

`core:worker` expectations:
- include WorkManager dependencies
- include at least one example worker
- include a scheduler abstraction and one WorkManager-backed implementation
- keep worker DI inside the module, not in `feature/*`

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

App shell expectations:
- `MainActivity` should be `@AndroidEntryPoint`
- `MainActivity` should apply the app theme and render `MainApp`
- `MainViewModel` should aggregate app-level state only, not feature UI state
- `MainNavHost` should wire feature callbacks from the app layer
- `TopLevelDestination` should exist even if there is only one starter top-level destination at first

## Phase 5: Starter Features
If not in `--minimal` mode, generate at least:
- `feature/home`
- `feature/login`

Each feature should include:
- `Screen.kt`
- `ViewModel.kt`
- `navigation/<Feature>Navigation.kt`
- `component/<Feature>Content.kt`

Feature quality expectations:
- each feature must follow `Route` + `Screen` separation
- `ViewModel` should use `@HiltViewModel`
- navigation should live in the feature navigation file, not inside app shell files
- feature files should be coherent starter code, not random placeholders

## Phase 6: Wiring
The generated project should already:
- include all modules in `settings.gradle.kts`
- use type-safe project accessors
- wire `home` and `login` in `MainNavHost`
- expose top-level destination for `home`
- compile conceptually as a modular Compose app
- keep app shell and feature files aligned with the reference patterns

## Expected Quality
- files should be small but coherent
- generated code should not be placeholder gibberish
- namespaces, imports, plugin ids, and package names should all match the provided base package and slug
- generated files should avoid stale naming from previous domains or example apps
- generated infra should prefer Hilt wiring for repositories and shared services
- if a file is only a stub, it should still establish the correct structure for future extension
