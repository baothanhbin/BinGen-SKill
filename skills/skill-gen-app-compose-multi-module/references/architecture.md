# Architecture

## Goal
Create a new Android project that starts with the same structural conventions as `AgriDoctorAI`.

## Module Map
Use this module split by default:

```text
app/
build-logic/
gradle/
resources/
core/model/
core/theme/
core/ui/
core/network/
core/data/
core/database/
core/datastore/
core/alarm/
core/worker/
feature/home/
feature/login/
feature/<future-feature>/
```

## Responsibilities
- `app`: application shell, `NavHost`, app-level state, top-level navigation
- `build-logic`: convention plugins for app, module, feature, Hilt, Room, Compose
- `resources`: shared drawables, strings, fonts, raw assets
- `core:model`: API models, shared enums, DTOs, small cross-feature value objects
- `core:theme`: colors, typography, fonts, app theme
- `core:ui`: shared UI helpers, small cross-feature utilities, dialogs, state holders
- `core:network`: Ktor clients, network datasource, `BuildConfig.API_BASE_URL`
- `core:data`: repository contracts, implementations, DI bindings/provides
- `core:database`: Room database, DAOs, entities, converters, DB DI
- `core:datastore`: Proto DataStore wrappers and `.proto` files
- `core:alarm`: reminder/alarm scheduler and receivers
- `core:worker`: WorkManager workers, scheduler interfaces, and Hilt-backed background job wiring
- `feature:*`: UI, ViewModel, navigation, components, dialogs, sheets per feature

## Feature Structure
Default feature layout:

```text
feature/<name>/
  build.gradle.kts
  src/main/AndroidManifest.xml
  src/main/java/<package>/feature/<name>/
    <Feature>Screen.kt
    <Feature>ViewModel.kt
    navigation/
      <Feature>Navigation.kt
    component/
      <Feature>Content.kt
```

Add `dialog/` or `sheet/` only when needed.

## Naming
- module names: `:core:<name>`, `:feature:<name>`
- feature namespace: `<base-package>.feature.<name>`
- core namespace: `<base-package>.core.<name>`
- screen file: `<Feature>Screen.kt`
- viewmodel file: `<Feature>ViewModel.kt`
- navigation file: `<Feature>Navigation.kt`
- route wrapper: `<Feature>Route`
- navigation extension: `navigateTo<Feature>`
- nav graph registration: camelCase + `Screen`

## State and Compose Rules
- use Compose for all UI
- use `ViewModel` + `StateFlow` for durable screen state
- use `SharedFlow` for one-off navigation/events
- use `collectAsStateWithLifecycle()` by default in route level composables
- let `Route` wire `ViewModel`, state collection, and side effects
- let `Screen` receive UI-ready state and callbacks

## Data Rules
- put API DTOs in `core:model`
- put Ktor clients and datasource in `core:network`
- put repository contracts and impls in `core:data`
- put Room entities and DAOs in `core:database`
- put token/session persistence in `core:datastore`
- put WorkManager workers and enqueue policies in `core:worker`
- use Hilt for app-wide dependency wiring

## Build Rules
- use a version catalog in `gradle/libs.versions.toml`
- use `build-logic` convention plugins
- create these plugin ids:
  - `<slug>.compose.application`
  - `<slug>.compose.module`
  - `<slug>.feature`
  - `<slug>.module`
  - `<slug>.hilt`
  - `<slug>.room`

## New Project Defaults
For a fresh project, prefer cleaner defaults than legacy quirks:
- use `ViewModel` unless `Application` is truly needed
- avoid `feature -> feature` dependencies initially
- avoid destructive Room migration unless user explicitly accepts it
- keep routes and names consistent from the start
