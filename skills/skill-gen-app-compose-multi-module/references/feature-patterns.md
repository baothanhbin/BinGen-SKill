# Feature Patterns

Use this file when creating or extending any `feature/*` module.

## Required File Map

Each feature should default to this structure:

```text
feature/<name>/
  build.gradle.kts
  src/main/AndroidManifest.xml
  src/main/java/<base-package>/feature/<name>/
    <Feature>Screen.kt
    <Feature>ViewModel.kt
    component/
      <Feature>Content.kt
    navigation/
      <Feature>Navigation.kt
```

Add `dialog/` or `sheet/` only when there is a real UI need.

## Default Responsibilities

- `<Feature>Navigation.kt`: route constant, `navigateTo<Feature>()`, and `NavGraphBuilder.<feature>Screen(...)`
- `<Feature>Screen.kt`: `Route` + `Screen` split
- `<Feature>ViewModel.kt`: UI state + one-off events + action handlers
- `component/<Feature>Content.kt`: reusable leaf content used by `Screen`

## Build File Rule

Feature modules should apply the feature convention plugin and keep direct dependencies small:

```kotlin
plugins {
    alias(libs.plugins.myapp-feature)
}

android {
    namespace = "com.example.myapp.feature.home"
}

dependencies {
    implementation(projects.core.theme)
    implementation(projects.core.data)
    implementation(projects.core.ui)
}
```

Do not add `feature -> feature` dependencies by default.

## Route Pattern

`Route` owns:
- `hiltViewModel()`
- `collectAsStateWithLifecycle()`
- event collection via `LaunchedEffect`

Example:

```kotlin
@Composable
internal fun HomeRoute(
    onNavigateToLogin: () -> Unit,
    viewModel: HomeViewModel = hiltViewModel(),
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(viewModel) {
        viewModel.events.collect { event ->
            when (event) {
                HomeEvent.NavigateToLogin -> onNavigateToLogin()
            }
        }
    }

    HomeScreen(
        uiState = uiState,
        onNavigateToLogin = viewModel::onNavigateToLoginClick,
        onRefresh = viewModel::refresh,
    )
}
```

## Screen Pattern

`Screen` should receive UI-ready state plus callbacks only:

```kotlin
@Composable
internal fun HomeScreen(
    uiState: HomeUiState,
    onNavigateToLogin: () -> Unit,
    onRefresh: () -> Unit,
) {
    HomeContent(
        title = uiState.title,
        onNavigateToLogin = onNavigateToLogin,
        onRefresh = onRefresh,
    )
}
```

## ViewModel Pattern

Default shape:

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val authRepository: AuthRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    private val _events = MutableSharedFlow<HomeEvent>()
    val events: SharedFlow<HomeEvent> = _events.asSharedFlow()

    fun refresh() {
        _uiState.update { state ->
            state.copy(title = "Updated home")
        }
    }

    fun onNavigateToLoginClick() {
        viewModelScope.launch {
            _events.emit(HomeEvent.NavigateToLogin)
        }
    }
}
```

Keep events in the `ViewModel`. Do not let composables decide navigation business rules directly.

## Navigation File Pattern

```kotlin
const val HOME_ROUTE = "home"

fun NavController.navigateToHome(
    navOptions: NavOptions? = null,
) {
    navigate(HOME_ROUTE, navOptions)
}

fun NavGraphBuilder.homeScreen(
    onNavigateToLogin: () -> Unit,
) {
    composable(
        route = HOME_ROUTE,
    ) {
        HomeRoute(
            onNavigateToLogin = onNavigateToLogin,
        )
    }
}
```

When the feature belongs to an auth flow such as `login`, `signup`, or `forgotpassword`, add the shared horizontal transitions from `core:ui/navigation`.

When the feature belongs to a modal/process flow such as `camera`, `processimage`, `settings`, or result screens, add the shared vertical transitions from `core:ui/navigation`.

## Starter Feature Rules

Use these concrete defaults when generating starter features:

- `login`: one primary action that emits an event to navigate to home
- `home`: one top-level destination and one example action that can navigate to login
- future generic features: show one coherent screen with title state, one content composable, and no cross-feature dependency unless explicitly requested
- auth-like starter screens should use staged `AnimatedVisibility` reveal for the form block and CTA block
- loading states should use the shared `core:ui/feedback/LoadingOverlay` instead of a one-off dialog in the feature

## Do Not Do

- Do not put repository calls directly in composables.
- Do not mix navigation graph registration into `Screen.kt`.
- Do not collapse `Route`, `Screen`, `ViewModel`, and navigation into a single file.
- Do not add `Application` injection into feature ViewModels unless unavoidable.
