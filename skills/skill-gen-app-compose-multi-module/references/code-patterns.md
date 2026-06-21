# Code Patterns

Use these patterns when extending the scaffold after the base project is generated. Treat them as the default shape unless the user explicitly asks for a different architecture.

## Table of Contents
- Feature route + screen split
- Feature ViewModel
- Feature navigation file
- Hilt repository wiring
- Room database wiring
- Proto DataStore wiring
- App-level navigation registration

## Feature route + screen split

Keep `Route` responsible for:
- obtaining the `ViewModel`
- collecting `StateFlow`
- collecting one-off `SharedFlow` events
- triggering navigation callbacks

Keep `Screen` responsible for:
- rendering already prepared UI state
- invoking callbacks from user interaction

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
        onLoginClick = viewModel::onLoginClick,
        onRefresh = viewModel::refresh,
    )
}

@Composable
internal fun HomeScreen(
    uiState: HomeUiState,
    onLoginClick: () -> Unit,
    onRefresh: () -> Unit,
) {
    Column {
        Text(text = uiState.title)
        Button(onClick = onRefresh) {
            Text("Refresh")
        }
        Button(onClick = onLoginClick) {
            Text("Login")
        }
    }
}
```

## Feature ViewModel

Default to:
- `@HiltViewModel`
- constructor injection
- `MutableStateFlow` for durable screen state
- `MutableSharedFlow` for one-off navigation or messages

Example:

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val sessionRepository: SessionRepository,
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

    fun onLoginClick() {
        viewModelScope.launch {
            _events.emit(HomeEvent.NavigateToLogin)
        }
    }
}

data class HomeUiState(
    val title: String = "Home",
)

sealed interface HomeEvent {
    data object NavigateToLogin : HomeEvent
}
```

## Feature navigation file

Each feature should own its route constant, navigation extension, and graph registration entry point.

Example:

```kotlin
const val HOME_ROUTE = "home"

fun NavController.navigateToHome() {
    navigate(HOME_ROUTE)
}

fun NavGraphBuilder.homeScreen(
    onNavigateToLogin: () -> Unit,
) {
    composable(route = HOME_ROUTE) {
        HomeRoute(
            onNavigateToLogin = onNavigateToLogin,
        )
    }
}
```

## Hilt repository wiring

Put repository contracts in `core:data` and bind them with Hilt modules there.

Example:

```kotlin
interface SessionRepository {
    suspend fun isLoggedIn(): Boolean
}

class DefaultSessionRepository @Inject constructor(
    private val sessionLocalDataSource: SessionLocalDataSource,
) : SessionRepository {
    override suspend fun isLoggedIn(): Boolean {
        return sessionLocalDataSource.getAccessToken().isNotBlank()
    }
}

@Module
@InstallIn(SingletonComponent::class)
abstract class SessionRepositoryModule {

    @Binds
    abstract fun bindSessionRepository(
        impl: DefaultSessionRepository,
    ): SessionRepository
}
```

## Room database wiring

Keep Room setup in `core:database`.

Example:

```kotlin
@Entity(tableName = "plant")
data class PlantEntity(
    @PrimaryKey val id: String,
    val name: String,
)

@Dao
interface PlantDao {
    @Query("SELECT * FROM plant")
    suspend fun getAll(): List<PlantEntity>
}

@Database(
    entities = [PlantEntity::class],
    version = 1,
    exportSchema = true,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun plantDao(): PlantDao
}

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideAppDatabase(
        @ApplicationContext context: Context,
    ): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app-database",
        ).build()
    }

    @Provides
    fun providePlantDao(
        database: AppDatabase,
    ): PlantDao = database.plantDao()
}
```

## Proto DataStore wiring

Keep DataStore setup in `core:datastore`.

Example:

```kotlin
class SessionLocalDataSource @Inject constructor(
    private val dataStore: DataStore<UserPreferences>,
) {
    suspend fun getAccessToken(): String {
        return dataStore.data.first().accessToken
    }
}

@Module
@InstallIn(SingletonComponent::class)
object DataStoreModule {

    @Provides
    @Singleton
    fun provideUserPreferencesDataStore(
        @ApplicationContext context: Context,
        serializer: UserPreferencesSerializer,
    ): DataStore<UserPreferences> {
        return DataStoreFactory.create(
            serializer = serializer,
            produceFile = { context.dataStoreFile("user_preferences.pb") },
        )
    }
}
```

## App-level navigation registration

Register feature navigation in `MainNavHost` and keep top-level destinations centralized.

Example:

```kotlin
@Composable
fun MainNavHost(
    navController: NavHostController,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = navController,
        startDestination = HOME_ROUTE,
        modifier = modifier,
    ) {
        homeScreen(
            onNavigateToLogin = navController::navigateToLogin,
        )
        loginScreen(
            onBack = navController::popBackStack,
        )
    }
}
```

## Usage Rule

Before generating or extending:
- feature code
- Hilt modules
- ViewModels
- navigation files
- repository implementations

read this file and follow its structure first, then adapt names to the target feature.
