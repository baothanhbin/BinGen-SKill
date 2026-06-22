# Golden File Examples

Use these as the closest file-shape references when generating a new project or refining scaffold output. These are not meant to be copied verbatim without renaming; they are meant to anchor structure and responsibility boundaries.

## app/MainActivity.kt

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
                    modifier = Modifier.fillMaxSize(),
                    appState = appState,
                    startDestination = if (isLoggedIn) HOME_ROUTE else LOGIN_ROUTE,
                )
            }
        }
    }
}
```

## app/navigation/MainNavHost.kt

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

## app/ui/MainApp.kt

```kotlin
@Composable
fun MainApp(
    appState: AppState,
    startDestination: String,
    modifier: Modifier = Modifier,
) {
    val currentDestination = appState.currentTopLevelDestination
    var bottomBarDestination by remember { mutableStateOf<TopLevelDestination?>(null) }

    if (currentDestination != null) {
        bottomBarDestination = currentDestination
    }

    Surface(modifier = modifier.fillMaxSize()) {
        Column {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxSize(),
            ) {
                MainNavHost(
                    modifier = Modifier.fillMaxSize(),
                    appState = appState,
                    startDestination = startDestination,
                )
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
        }
    }
}
```

## feature/home/HomeScreen.kt

```kotlin
@Composable
fun HomeRoute(
    onNavigateToLogin: () -> Unit,
    viewModel: HomeViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    HomeScreen(
        uiState = uiState,
        onNavigateToLogin = onNavigateToLogin,
    )
}

@Composable
fun HomeScreen(
    uiState: HomeUiState,
    onNavigateToLogin: () -> Unit,
) {
    HomeContent(
        title = uiState.title,
        onNavigateToLogin = onNavigateToLogin,
    )
}
```

## feature/login/LoginScreen.kt

```kotlin
@Composable
fun LoginRoute(
    onNavigateToHome: () -> Unit,
    viewModel: LoginViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LoginScreen(
        uiState = uiState,
        onContinue = onNavigateToHome,
    )
}
```

## core/data/AuthRepository.kt

```kotlin
interface AuthRepository {
    val isLoggedIn: Flow<Boolean>
    suspend fun getToken(): String?
}
```

## core/network/NetworkModule.kt

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    @Named("auth")
    fun provideAuthHttpClient(): HttpClient {
        return HttpClient(OkHttp) {
            defaultRequest {
                url(BuildConfig.API_BASE_URL)
            }
            install(ContentNegotiation) {
                json(Json { ignoreUnknownKeys = true })
            }
        }
    }
}
```

## Usage Rule

Before generating or rewriting any of these files:
- `MainActivity.kt`
- `MainNavHost.kt`
- `MainViewModel.kt`
- `HomeScreen.kt`
- `LoginScreen.kt`
- repository or network module files

read this file and keep the generated output close in structure, then rename packages, feature names, and callbacks to match the target project.
