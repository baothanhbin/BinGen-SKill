# Golden Animation Examples

Use these examples as the closest implementation shape when generating motion-heavy starter files.

## core/ui/navigation/ScreenTransitions.kt

```kotlin
private const val HALF_SCREEN_DIVISOR = 2
private const val NAV_DURATION_MS = 180
private val navSlideSpec = tween<IntOffset>(
    durationMillis = NAV_DURATION_MS,
    easing = FastOutSlowInEasing,
)

fun AnimatedContentTransitionScope<NavBackStackEntry>.slideInFromRightHalf(): EnterTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideOutToLeftHalf(): ExitTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideInFromBottomHalf(): EnterTransition
fun AnimatedContentTransitionScope<NavBackStackEntry>.slideOutToTopHalf(): ExitTransition
```

## core/ui/feedback/LoadingOverlay.kt

```kotlin
@Composable
fun LoadingOverlay(
    isVisible: Boolean,
    modifier: Modifier = Modifier,
) {
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
    ) {
        // overlay content
    }
}
```

## app/ui/MainApp.kt

```kotlin
val currentDestination = appState.currentTopLevelDestination
var bottomBarDestination by remember { mutableStateOf<TopLevelDestination?>(null) }

if (currentDestination != null) {
    bottomBarDestination = currentDestination
}

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

## feature/login/LoginScreen.kt

```kotlin
AnimatedVisibility(
    visible = true,
    enter = fadeIn(animationSpec = tween(600, delayMillis = 600)),
    exit = fadeOut(animationSpec = tween(600)),
) {
    Column {
        // form fields
    }
}

AnimatedVisibility(
    visible = true,
    enter = fadeIn(animationSpec = tween(600, delayMillis = 800)),
    exit = fadeOut(animationSpec = tween(600)),
) {
    val buttonScale = if (isFormValid && !isLoading) 1f else 0.98f
    Button(
        modifier = Modifier.scale(buttonScale),
        onClick = onLoginClick,
    ) {
        // CTA
    }
}
```

## feature/processimage/ImageCard.kt

```kotlin
val infinite = rememberInfiniteTransition(label = "scan_bar")
val offsetYFraction by infinite.animateFloat(
    initialValue = 0f,
    targetValue = 1f,
    animationSpec = infiniteRepeatable(
        animation = tween(durationMillis = 1200, easing = LinearEasing),
        repeatMode = RepeatMode.Reverse,
    ),
    label = "offsetYFraction",
)
```

Pair it with:
- a soft gradient scan band
- a bright center line
- a trailing gradient shadow

## feature/camera/SlidingSegmentedToggle.kt

```kotlin
val animatedOffset = animateDpAsState(
    targetValue = targetOffset,
    animationSpec = tween(durationMillis = 250, easing = LinearOutSlowInEasing),
    label = "seg_offset",
)
```

Use this for:
- two-state mode switchers
- pill-style tabs inside a feature

## Usage Rule

Before generating any of these files or adding motion to a new feature:
- read `animation-patterns.md`
- then use the closest example here
- keep durations and easing close to the examples unless the user asks for a different visual language
