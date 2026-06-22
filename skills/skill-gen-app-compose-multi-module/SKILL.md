---
name: skill-gen-app-compose-multi-module
description: "Scaffold a brand-new Android project from zero so it follows a feature-first Compose multi-module structure with `app`, `core/*`, `feature/*`, `resources`, `build-logic`, Hilt, Room, Proto DataStore, Ktor networking, and per-feature navigation files. Use when Codex needs to create a new Android repo, starter architecture, or modular baseline similar to the AgriDoctorAI style rather than a generic clean-template project."
---

# Skill Gen App Compose Multi Module

## Overview
Use this skill when the user wants a completely new Android project that already starts with the same architectural shape, naming rules, and project layout as `AgriDoctorAI`.

This skill is intentionally opinionated toward compatibility with the `AgriDoctorAI` coding style, including its `app / core / feature / resources / build-logic` split, Compose-first UI, Hilt DI, Room, Proto DataStore, Ktor networking, and per-feature navigation files.

## Required Inputs
Collect or infer these before scaffolding:
- project name
- base package, for example `com.example.plantapp`
- short Gradle/plugin slug, for example `plantapp`
- whether to include sample starter features now or only baseline infrastructure
- whether auth, Room, DataStore, Ktor, and alarm/reminder support should be included immediately

If the user does not specify all of them, make reasonable defaults and state them while scaffolding.

## Workflow
1. Read `references/architecture.md` first.
2. Read `references/scaffold-spec.md` before creating files.
3. Read `references/app-shell-patterns.md` before generating or changing the `app` module.
4. Read `references/core-module-patterns.md` before generating or changing any `core/*` module.
5. Read `references/animation-patterns.md` and `references/golden-animation-examples.md` before generating navigation transitions, loading overlays, animated app chrome, auth reveal flows, or feature-specific motion.
5. Read `references/worker-patterns.md` and `references/golden-worker-examples.md` before generating `core:worker`, WorkManager wiring, sync jobs, retry jobs, or `App.kt` worker factory setup.
6. Read `references/feature-patterns.md` and `references/code-patterns.md` before generating feature code, Hilt modules, navigation files, repository wiring, DataStore wiring, Room wiring, or worker scheduler wiring.
7. Read `references/golden-file-examples.md` before generating or refining `MainActivity`, `MainNavHost`, starter feature files, repository files, or network module files.
8. Create the project skeleton by running `scripts/scaffold_project.py`.
9. After the scaffold finishes, inspect the generated tree and fill any project-specific gaps the user requested.
10. If the user asked for initial features, add one feature end-to-end first, then clone the pattern to the remaining features.
11. Validate the scaffold by reading `references/validation-checklist.md` and checking root Gradle files, module includes, namespaces, and at least one representative feature module.

## Execution Rules
- Prefer creating the real project files instead of only describing what to do.
- Keep module names in the form `:core:<name>` and `:feature:<name>`.
- Keep `Route` responsible for `ViewModel`, state collection, and side effects by default.
- Keep `Screen` focused on UI-ready state and callbacks.
- Keep reusable UI pieces in `component/`, with `dialog/` and `sheet/` only when needed.
- Keep reusable motion primitives in `core:ui`, especially navigation transitions and loading overlays.
- Keep repositories in `core:data`, Room in `core:database`, Proto DataStore in `core:datastore`, and Ktor access in `core:network`.
- Keep WorkManager workers, scheduler abstractions, and enqueue policies in `core:worker`.
- Avoid introducing domain/use-case layers unless the user explicitly wants a different architecture.
- Avoid `feature -> feature` dependencies in fresh scaffolds unless the requested flow clearly benefits from it.
- Default new code to `collectAsStateWithLifecycle()`, `StateFlow` for durable state, and `SharedFlow` for one-off events.
- Default structural navigation motion to the `AgriDoctorAI` pattern: horizontal half-slide for auth/linear form flows, vertical half-slide for modal/process/camera/result flows.
- Default auth and setup screens to staged `AnimatedVisibility` reveal rather than dropping all controls on screen at once.
- Avoid leaving placeholder-shaped app shell or feature files when the user expects a starter project that is ready to extend.
- Remove or rename any leftover project-specific naming from older examples unless the user explicitly wants it.
- Prefer Hilt-provided modules over global singleton objects when generating infra code for network, data, or persistence layers.
- If `core:worker` is part of the scaffold, wire `HiltWorkerFactory` in `app/App.kt` instead of leaving workers half-configured.

## Scaffolding Order
1. Create root Gradle files and `settings.gradle.kts`.
2. Create `gradle/libs.versions.toml`.
3. Create `build-logic` with convention plugins.
4. Create shared modules:
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
5. Create `app` shell with:
   - `App.kt`
   - `MainActivity.kt`
   - `MainViewModel.kt`
   - `navigation/AppState.kt`
   - `navigation/MainNavHost.kt`
   - `navigation/TopLevelDestination.kt`
6. Create starter feature modules if requested:
   - `feature/home`
   - `feature/login`
   - optional placeholder modules for future growth
7. Wire the initial navigation graph and top-level tabs.

## Script Usage
Run the scaffold script like this:

```powershell
python scripts/scaffold_project.py ^
  --project-name "MyPlantApp" ^
  --package "com.example.myplantapp" ^
  --slug "myplantapp" ^
  --features "home,login"
```

Optional flags:
- `--output "D:\work\MyPlantApp"`: scaffold into another folder; if omitted, scaffold into the current working directory
- `--minimal`: create only baseline modules and app shell without starter feature modules
- `--features "home,login,settings"`: create additional starter feature skeletons

## References
- Read `references/architecture.md` for the target architecture, dependency rules, naming, and module responsibilities.
- Read `references/scaffold-spec.md` for the exact scaffold phases, file map, and generated content expectations.
- Read `references/app-shell-patterns.md` for the required `app` module shape.
- Read `references/core-module-patterns.md` for infra module boundaries and DI expectations.
- Read `references/animation-patterns.md` for motion placement, transition selection, durations, and reveal patterns derived from `AgriDoctorAI`.
- Read `references/feature-patterns.md` for feature file map, route/screen/viewmodel split, and navigation defaults.
- Read `references/code-patterns.md` for the default implementation shape of `Route`, `Screen`, `ViewModel`, Hilt modules, repository wiring, DataStore wiring, Room wiring, and feature navigation.
- Read `references/worker-patterns.md` for `@HiltWorker`, `@AssistedInject`, scheduler abstraction, and `App.kt` WorkManager setup.
- Read `references/golden-file-examples.md` for the closest file-shape references of the most important starter files.
- Read `references/golden-animation-examples.md` for the closest file shapes of `ScreenTransitions`, `LoadingOverlay`, animated `MainApp`, staged auth reveal, and purposeful feature-local motion.
- Read `references/golden-worker-examples.md` for the closest starter file shapes of `SyncWorker`, scheduler bindings, and worker-ready `App.kt`.
- Read `references/validation-checklist.md` before declaring the scaffold complete.

## Output Expectations
- Produce a real scaffolded project, not just prose.
- Keep generated names internally consistent across packages, namespaces, routes, and Gradle accessors.
- State the assumptions you made if the user left parts unspecified.
- If the user later wants more features, extend the scaffold instead of rebuilding it.
- When extending the scaffold, follow the code patterns reference instead of inventing a new structure.
- Before finishing, inspect the generated output against the validation checklist and fix obvious weak spots instead of leaving them for the user.
