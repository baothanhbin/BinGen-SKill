# Animation Patterns

Use this file when generating or refining motion in a new project scaffolded by this skill.

These patterns are grounded in `AgriDoctorAI`, not generic Compose advice. Keep motion short, purposeful, and centralized.

## Table of Contents
- Principles
- Navigation transitions
- App shell visibility
- Loading overlay
- Form reveal
- Purpose-built motion
- Placement rules

## Principles

- Centralize structural navigation transitions in `core:ui/navigation`, not scattered across feature files.
- Keep route-to-route motion fast. `AgriDoctorAI` uses `180ms` for navigation slides.
- Use `AnimatedVisibility` for staged reveal, app chrome visibility, validation hints, and overlays.
- Use `rememberInfiniteTransition` only for live feedback with clear meaning, such as scanning/progress.
- Prefer one consistent transition family per flow:
  - auth and linear form flows: horizontal half-slide
  - modal/process/camera/result flows: vertical half-slide

## Navigation transitions

Put shared transition helpers in `core/ui/navigation/ScreenTransitions.kt`.

Reference pattern from `AgriDoctorAI/core/ui/navigation/ScreenTransitions.kt`:

```kotlin
private const val HALF_SCREEN_DIVISOR = 2
private const val NAV_DURATION_MS = 180
private val navSlideSpec = tween<IntOffset>(
    durationMillis = NAV_DURATION_MS,
    easing = FastOutSlowInEasing,
)

fun AnimatedContentTransitionScope<NavBackStackEntry>.slideInFromRightHalf(): EnterTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideOutToLeftHalf(): ExitTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideInFromLeftHalf(): EnterTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideOutToRightHalf(): ExitTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideInFromBottomHalf(): EnterTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideOutToTopHalf(): ExitTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideInFromTopHalf(): EnterTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideOutToBottomHalf(): ExitTransition
```

Use horizontal transitions for:
- `login`
- `signup`
- `forgotpassword`
- `verificationotp`

Use vertical transitions for:
- `camera`
- `processimage`
- `settings`
- `lightmeter`
- `diagnoseresult`
- `diagnosefailed`

Feature navigation file example:

```kotlin
fun NavGraphBuilder.loginScreen(
    onNavigateToHome: () -> Unit,
) {
    composable(
        route = LOGIN_ROUTE,
        enterTransition = { slideInFromRightHalf() },
        exitTransition = { slideOutToLeftHalf() },
        popEnterTransition = { slideInFromLeftHalf() },
        popExitTransition = { slideOutToRightHalf() },
    ) {
        LoginRoute(onNavigateToHome = onNavigateToHome)
    }
}
```

## App shell visibility

Reference pattern from `AgriDoctorAI/app/ui/MainApp.kt`:

```kotlin
AnimatedVisibility(
    visible = currentDestination != null,
    enter = fadeIn(animationSpec = tween(durationMillis = 160)),
    exit = fadeOut(animationSpec = tween(durationMillis = 120)),
) {
    bottomBarDestination?.let { destination ->
        MainBottomNavBar(...)
    }
}
```

Use this for:
- bottom bar visibility
- small app chrome that depends on destination

Do not animate the entire `NavHost` just to show or hide chrome.

## Loading overlay

Reference pattern from `AgriDoctorAI/core/ui/feedback/LoadingOverlay.kt`:

```kotlin
AnimatedVisibility(
    visible = isVisible,
    enter = fadeIn(animationSpec = tween(durationMillis = 180)) +
        scaleIn(
            initialScale = 0.92f,
            animationSpec = tween(durationMillis = 180),
        ),
    exit = fadeOut(animationSpec = tween(durationMillis = 120)) +
        scaleOut(
            targetScale = 0.92f,
            animationSpec = tween(durationMillis = 120),
        ),
)
```

Use this shared component in `core:ui/feedback` instead of rebuilding slightly different loading dialogs in each feature.

## Form reveal

Reference pattern from `AgriDoctorAI/feature/login` and `feature/signup`:

```kotlin
AnimatedVisibility(
    visible = true,
    enter = fadeIn(animationSpec = tween(600, delayMillis = 600)),
    exit = fadeOut(animationSpec = tween(600)),
) { formBlock() }

AnimatedVisibility(
    visible = true,
    enter = fadeIn(animationSpec = tween(600, delayMillis = 800)),
    exit = fadeOut(animationSpec = tween(600)),
) { actionBlock() }
```

Button emphasis pattern:

```kotlin
val buttonScale = if (isFormValid && !isLoading) 1f else 0.98f
```

Use this when:
- introducing auth screens
- revealing multi-field forms
- emphasizing the primary CTA after the form block is on screen

Do not stack too many staggered sections. Two stages are usually enough:
- form fields
- primary CTA/footer action

## Purpose-built motion

Use feature-local motion when it carries meaning:

- scanning/process flow:
  - `rememberInfiniteTransition`
  - `animateFloat(0f, 1f)`
  - `infiniteRepeatable(tween(1200, LinearEasing), RepeatMode.Reverse)`
  - animated scan band using `graphicsLayer { translationY = ... }`
- segmented toggle:
  - `animateDpAsState`
  - `tween(durationMillis = 250, easing = LinearOutSlowInEasing)`
  - sliding selected indicator

Keep these animations inside the owning feature unless multiple features reuse the exact same component.

## Placement rules

- `core:ui/navigation`: navigation transition helpers
- `core:ui/feedback`: shared overlays and reusable UI feedback motion
- `app/ui`: app chrome visibility such as bottom bar/header shell
- `feature/*/Screen.kt`: screen reveal and feature-local motion
- `feature/*/component`: specialized animated leaf components like scan cards or segmented toggles

When adding animation to a new project, read this file first, then read `golden-animation-examples.md` for concrete file shapes.
