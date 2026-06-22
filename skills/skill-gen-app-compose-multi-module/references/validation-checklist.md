# Validation Checklist

Use this checklist after running the scaffold script and again after adding custom starter features.

## Structure

- root has `app`, `build-logic`, `gradle`, `resources`, `core/*`, and optional `feature/*`
- every module has `build.gradle.kts`, `consumer-rules.pro`, `proguard-rules.pro`, and `AndroidManifest.xml` where appropriate
- `settings.gradle.kts` includes every generated module exactly once

## Build Logic

- plugin ids use the user-provided slug
- UI modules use compose conventions
- non-UI modules do not use compose conventions unless there is real Compose code inside
- Hilt plugin is applied only where dependency injection is needed

## App Shell

- `App.kt` has `@HiltAndroidApp`
- `MainActivity` is `@AndroidEntryPoint`
- `MainViewModel` does not use `runBlocking` for initial state
- `MainNavHost` wires feature callbacks at the app level
- `MainApp` uses consistent app chrome visibility animation if bottom navigation exists

## Features

- each feature has `Screen`, `ViewModel`, `navigation`, and `component`
- `Route` owns `collectAsStateWithLifecycle()` and event collection
- `Screen` receives state + callbacks only
- feature navigation files own route constants and `navigateTo<Feature>()`
- auth/process features use shared transition helpers instead of bespoke animation code
- reusable loading motion lives in `core:ui/feedback`, not copied per feature

## Data + DI

- repositories live in `core:data`
- Hilt bindings live in `core:data/di`
- Room setup lives in `core:database`
- Proto DataStore setup lives in `core:datastore`
- Ktor client wiring lives in `core:network`

## Naming

- namespaces match the generated base package
- feature routes, file names, and module names all match the feature name
- no leftover domain-specific names from older projects, unless intentionally requested

## Smoke Test

At minimum, inspect:
- `app/build.gradle.kts`
- `app/navigation/MainNavHost.kt`
- one representative feature module
- one representative core infra module such as `core:data` or `core:network`

If the user asked for a real starter repo rather than just a skeleton, continue refining until these files look production-shaped rather than placeholder-shaped.
