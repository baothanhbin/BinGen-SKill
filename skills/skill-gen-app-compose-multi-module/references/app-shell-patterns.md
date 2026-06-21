# App Shell Patterns

Use this file when generating or changing the `app` module.

## Required File Map

```text
app/
  build.gradle.kts
  src/main/AndroidManifest.xml
  src/main/java/<base-package>/
    App.kt
    MainActivity.kt
    MainViewModel.kt
    navigation/
      AppState.kt
      MainNavHost.kt
      TopLevelDestination.kt
    ui/
      MainApp.kt
      MainBottomNavBar.kt
```

## App.kt

Keep it minimal:

```kotlin
@HiltAndroidApp
class App : Application()
```

Do not move feature startup logic into `App.kt`.

## MainActivity

Keep `MainActivity` responsible for:
- `@AndroidEntryPoint`
- obtaining `MainViewModel`
- selecting the initial route from app state
- applying `AppTheme`
- rendering `MainApp`

Prefer this shape:

```kotlin
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    private val mainViewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val isLoggedIn by mainViewModel.isLoggedIn.collectAsStateWithLifecycle()
            val appState = rememberAppState()

            AppTheme {
                MainApp(
                    appState = appState,
                    startDestination = if (isLoggedIn) HOME_ROUTE else LOGIN_ROUTE,
                )
            }
        }
    }
}
```

## MainViewModel

Keep it thin. It should aggregate app-level flows, not own feature UI state.

Good default:

```kotlin
@HiltViewModel
class MainViewModel @Inject constructor(
    authRepository: AuthRepository,
) : ViewModel() {
    val isLoggedIn: StateFlow<Boolean> = authRepository.isLoggedIn
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = false,
        )
}
```

Avoid synchronous `runBlocking` reads just to compute initial state.

## AppState

Keep shared app-level objects here:

```kotlin
class AppState(
    val navController: NavHostController,
    val locationStateHolder: LocationStateHolder,
)

@Composable
fun rememberAppState(): AppState {
    val navController = rememberNavController()
    val locationStateHolder = remember { LocationStateHolder() }
    return remember(navController, locationStateHolder) {
        AppState(
            navController = navController,
            locationStateHolder = locationStateHolder,
        )
    }
}
```

## MainNavHost

Keep all graph registration here.

Rules:
- `app` imports feature navigation extensions, not feature screens directly
- wire callbacks between features at the app level
- top-level destinations should be explicit

Example:

```kotlin
@Composable
fun MainNavHost(
    appState: AppState,
    startDestination: String,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = appState.navController,
        startDestination = startDestination,
        modifier = modifier,
    ) {
        loginScreen(
            onNavigateToHome = appState.navController::navigateToHome,
        )
        homeScreen(
            onNavigateToLogin = appState.navController::navigateToLogin,
        )
    }
}
```

## TopLevelDestination

Keep it centralized in `app/navigation`.

Example:

```kotlin
enum class TopLevelDestination(
    val route: String,
) {
    HOME(route = HOME_ROUTE),
}
```

## MainApp

Keep it as a simple composition root around `MainNavHost` and app chrome:

```kotlin
@Composable
fun MainApp(
    appState: AppState,
    startDestination: String,
    modifier: Modifier = Modifier,
) {
    MainNavHost(
        modifier = modifier,
        appState = appState,
        startDestination = startDestination,
    )
}
```

## MainBottomNavBar

If there is not yet a real multi-tab shell, keep this file tiny but intentional. Do not create fake complex bottom navigation until the user asks for it.
